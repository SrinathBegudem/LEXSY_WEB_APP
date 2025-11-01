'use client';

import { useState, useCallback, useEffect } from 'react';
import { Download, RefreshCw, CheckCircle2, AlertCircle } from 'lucide-react';
import { UploadZone } from '@/components/upload-zone';
import { ChatInterface } from '@/components/chat-interface';
import { DocumentPreview } from '@/components/document-preview';
import { ProgressTracker } from '@/components/progress-tracker';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { api, ApiError, setAuthToken, streamGroq, streamDocumentAI } from '@/lib/api';
import type {
  AppState,
  ChatMessage,
  Placeholder,
  UploadResponse,
  ChatResponse,
  PreviewResponse,
  CompleteResponse,
} from '@/lib/types';
import { Progress } from '@/components/ui/progress';
import { useAuth } from '@/hooks/useAuth';
import { LoginButton } from '@/components/auth/login-button';

export default function Home() {
  const { user, loading: authLoading, token } = useAuth();
  useEffect(() => {
    setAuthToken(token || null);
  }, [token]);

  const [state, setState] = useState<AppState>({
    sessionId: null,
    document: null,
    currentIndex: 0,
    progress: 0,
    isLoading: false,
    error: null,
    chatMessages: [],
    previewHtml: null,
    isComplete: false,
    downloadUrl: null,
  });

  const [initialMessage, setInitialMessage] = useState<string>('');
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);

  // Assistant tabs: 'doc' (document assistant) or 'ai' (generic Groq)
  const [assistantTab, setAssistantTab] = useState<'doc' | 'ai'>('doc');
  const [aiMessages, setAiMessages] = useState<ChatMessage[]>([]);
  const [aiLoading, setAiLoading] = useState<boolean>(false);

  const handleUpload = useCallback(async (file: File) => {
    setUploadedFile(file);
    setState((prev) => ({ ...prev, isLoading: true, error: null }));

    try {
      const response: UploadResponse = await api.uploadDocument(file);

      // Don't add initial message to chat history yet - it will be shown separately
      setInitialMessage(response.initial_message || '');

      setState({
        sessionId: response.session_id,
        document: {
          filename: response.filename,
          placeholders: response.placeholders,
          filledValues: {},
        },
        currentIndex: 0,
        progress: 0,
        isLoading: false,
        error: null,
        chatMessages: [], // Start with empty messages
        previewHtml: null,
        isComplete: false,
        downloadUrl: null,
      });

      // Load initial preview
      setTimeout(() => {
        loadPreview(response.session_id);
      }, 500);
    } catch (error) {
      const errorMessage =
        error instanceof ApiError ? error.message : 'Failed to upload document';
      setState((prev) => ({
        ...prev,
        isLoading: false,
        error: errorMessage,
      }));
      setUploadedFile(null);
    }
  }, []);

  const handleSendMessage = useCallback(
    async (message: string) => {
      if (!state.sessionId || state.isLoading) return;

      // Add user message immediately
      const userMessage: ChatMessage = {
        id: `msg-user-${Date.now()}`,
        role: 'user',
        content: message,
        timestamp: new Date(),
      };

      setState((prev) => ({
        ...prev,
        chatMessages: [...prev.chatMessages, userMessage],
        isLoading: true,
      }));

      try {
        const response: ChatResponse = await api.sendMessage(
          state.sessionId,
          message
        );

        const assistantMessage: ChatMessage = {
          id: `msg-assistant-${Date.now()}`,
          role: 'assistant',
          content: response.response,
          timestamp: new Date(),
          placeholderFilled: response.placeholder_filled,
        };

        const updatedFilledValues = response.filled_values;
        const newProgress = response.progress_percentage;
        const newCurrentIndex = response.current_progress;

        setState((prev) => ({
          ...prev,
          chatMessages: [...prev.chatMessages, assistantMessage],
          document: prev.document
            ? {
                ...prev.document,
                filledValues: updatedFilledValues,
              }
            : null,
          currentIndex: newCurrentIndex,
          progress: newProgress,
          isLoading: false,
          isComplete: response.all_filled,
          previewHtml: response.preview ?? prev.previewHtml,  // Use server-provided preview
        }));
      } catch (error) {
        const errorMessage =
          error instanceof ApiError
            ? error.message
            : 'Failed to send message. Please try again.';

        const errorChatMessage: ChatMessage = {
          id: `msg-error-${Date.now()}`,
          role: 'assistant',
          content: `Error: ${errorMessage}`,
          timestamp: new Date(),
        };

        setState((prev) => ({
          ...prev,
          chatMessages: [...prev.chatMessages, errorChatMessage],
          isLoading: false,
          error: errorMessage,
        }));
      }
    },
    [state.sessionId, state.isLoading]
  );

  // Document-aware AI chat handler with streaming
  const handleSendAIMessage = useCallback(
    async (message: string) => {
      if (aiLoading) return;

      const userMessage: ChatMessage = {
        id: `ai-user-${Date.now()}`,
        role: 'user',
        content: message,
        timestamp: new Date(),
      };

      const assistantId = `ai-assistant-${Date.now()}`;
      const assistantMessage: ChatMessage = {
        id: assistantId,
        role: 'assistant',
        content: '',
        timestamp: new Date(),
      };

      setAiMessages((prev) => [...prev, userMessage, assistantMessage]);
      setAiLoading(true);

      try {
        let accumulated = '';
        
        // If we have a document loaded, use document-aware AI
        if (state.document && state.sessionId) {
          await streamDocumentAI(
            message, 
            {
              sessionId: state.sessionId,
              filename: state.document.filename,
              placeholders: state.document.placeholders,
              filledValues: state.document.filledValues,
              previewHtml: state.previewHtml,
            },
            (chunk) => {
              accumulated += chunk;
              setAiMessages((prev) =>
                prev.map((m) => (m.id === assistantId ? { ...m, content: accumulated } : m))
              );
            }
          );
        } else {
          // Otherwise, use regular AI
          await streamGroq(message, (chunk) => {
            accumulated += chunk;
            setAiMessages((prev) =>
              prev.map((m) => (m.id === assistantId ? { ...m, content: accumulated } : m))
            );
          });
        }
      } catch (e) {
        const errText = e instanceof Error ? e.message : 'AI error';
        setAiMessages((prev) =>
          prev.map((m) => (m.id === assistantId ? { ...m, content: `Error: ${errText}` } : m))
        );
      } finally {
        setAiLoading(false);
      }
    },
    [aiLoading, state.document, state.sessionId, state.previewHtml]
  );

  const loadPreview = useCallback(async (sessionId: string) => {
    try {
      const preview: PreviewResponse = await api.getPreview(sessionId);
      setState((prev) => ({
        ...prev,
        previewHtml: preview.preview,
      }));
    } catch (error) {
      console.error('Failed to load preview:', error);
    }
  }, []);

  const handleComplete = useCallback(async () => {
    if (!state.sessionId || state.isLoading) return;

    setState((prev) => ({ ...prev, isLoading: true }));

    try {
      const response: CompleteResponse = await api.completeDocument(
        state.sessionId
      );

      setState((prev) => ({
        ...prev,
        isComplete: true,
        downloadUrl: response.download_url,
        isLoading: false,
      }));

      // Show success message
      const successMessage: ChatMessage = {
        id: `msg-success-${Date.now()}`,
        role: 'assistant',
        content: response.message,
        timestamp: new Date(),
      };

      setState((prev) => ({
        ...prev,
        chatMessages: [...prev.chatMessages, successMessage],
      }));
    } catch (error) {
      const errorMessage =
        error instanceof ApiError
          ? error.message
          : 'Failed to complete document. Please try again.';

      setState((prev) => ({
        ...prev,
        isLoading: false,
        error: errorMessage,
      }));
    }
  }, [state.sessionId, state.isLoading]);

  const handleDownload = useCallback(async () => {
    if (!state.downloadUrl) return;

    try {
      const filename = state.downloadUrl.split('/').pop() || 'document.docx';
      const blob = await api.downloadDocument(filename);

      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      const errorMessage =
        error instanceof ApiError
          ? error.message
          : 'Failed to download document. Please try again.';
      setState((prev) => ({ ...prev, error: errorMessage }));
    }
  }, [state.downloadUrl]);

  const handleFillFieldDirectly = useCallback(
    async (fieldKey: string, value: string) => {
      if (!state.sessionId || state.isLoading) return;

      setState((prev) => ({ ...prev, isLoading: true }));

      try {
        const response = await api.fillFieldDirectly(state.sessionId, fieldKey, value);

        // Update state with new preview and filled values
        setState((prev) => ({
          ...prev,
          previewHtml: response.preview,
          isLoading: false,
          currentIndex: response.next_index ?? prev.currentIndex,
          document: prev.document ? {
            ...prev.document,
            filledValues: response.filled_values || prev.document.filledValues,
          } : null,
          progress: response.progress_percentage || prev.progress,
        }));

        // Show success message if auto-filled
        if (response.auto_filled && response.auto_filled.length > 0) {
          console.log(`Auto-filled: ${response.auto_filled.join(', ')}`);
        }
      } catch (error) {
        const errorMessage =
          error instanceof ApiError ? error.message : 'Failed to fill field';
        setState((prev) => ({
          ...prev,
          isLoading: false,
          error: errorMessage,
        }));
        throw error; // Re-throw so component can handle it
      }
    },
    [state.sessionId, state.isLoading]
  );

  const handleEditField = useCallback(
    async (fieldKey: string, currentValue: string) => {
      if (!state.sessionId) return;

      // Prompt user for new value
      const newValue = prompt(`Edit field value:\n\nCurrent: ${currentValue}\n\nEnter new value:`, currentValue);
      
      if (newValue === null || newValue === currentValue) {
        return; // User cancelled or didn't change
      }

      setState((prev) => ({ ...prev, isLoading: true }));

      try {
        const response: PreviewResponse = await api.editField(
          state.sessionId,
          fieldKey,  // This is now the ID
          newValue
        );

        // Find the placeholder by ID first, then by key
        const placeholder = state.document?.placeholders.find((p) => p.id === fieldKey || p.key === fieldKey);
        const fieldName = placeholder?.name || 'Field';

        // Update state
        setState((prev) => ({
          ...prev,
          document: prev.document
            ? {
                ...prev.document,
                filledValues: response.filled_values,
              }
            : null,
          previewHtml: response.preview,
          currentIndex: response.current_index ?? prev.currentIndex,
          progress: response.progress_percentage,
          isLoading: false,
        }));

        // Add a message about the edit
        const editMessage: ChatMessage = {
          id: `msg-edit-${Date.now()}`,
          role: 'assistant',
          content: `✅ Updated **${fieldName}** to: "${newValue}"`,
          timestamp: new Date(),
        };

        setState((prev) => ({
          ...prev,
          chatMessages: [...prev.chatMessages, editMessage],
        }));
      } catch (error) {
        const errorMessage =
          error instanceof ApiError
            ? error.message
            : 'Failed to update field. Please try again.';

        setState((prev) => ({
          ...prev,
          isLoading: false,
          error: errorMessage,
        }));
      }
    },
    [state.sessionId, state.document]
  );

  const handleReset = useCallback(async () => {
    if (state.sessionId) {
      try {
        await api.resetSession(state.sessionId);
      } catch (error) {
        console.error('Failed to reset session:', error);
      }
    }

    setState({
      sessionId: null,
      document: null,
      currentIndex: 0,
      progress: 0,
      isLoading: false,
      error: null,
      chatMessages: [],
      previewHtml: null,
      isComplete: false,
      downloadUrl: null,
    });
    setInitialMessage('');
    setUploadedFile(null);
  }, [state.sessionId]);

  // Note: Auto-refresh removed - preview is now updated with each chat response
  // for better performance and to avoid race conditions

  const hasDocument = state.document !== null;

  return (
    <main className="min-h-screen flex flex-col bg-slate-50">
      {/* Premium Header */}
      <div className="border-b border-slate-200 bg-white sticky top-0 z-40 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3 sm:py-4">
          <div className="flex items-center justify-between gap-4">
            {/* Left: Logo and Company Name */}
            <div className="flex items-center gap-3 sm:gap-4 min-w-0 flex-shrink">
              <div>
                <h1 className="text-xl sm:text-2xl font-bold text-slate-900">
                  Lexsy
                </h1>
                <p className="text-xs text-slate-600 mt-0.5 hidden sm:block">
                  AI-powered document automation
                </p>
              </div>
              {user && (
                <div className="hidden lg:flex items-center gap-2 pl-3 border-l border-slate-200">
                  {user.photoURL && (
                    <img
                      src={user.photoURL}
                      alt={user.displayName || 'User'}
                      className="h-8 w-8 rounded-full border-2 border-blue-500"
                    />
                  )}
                  <div className="text-sm">
                    <p className="font-medium text-slate-900 truncate max-w-[150px]">
                      {user.displayName || 'User'}
                    </p>
                    <p className="text-xs text-slate-500 truncate max-w-[150px]">{user.email}</p>
                  </div>
                </div>
              )}
            </div>

            {/* Center: Document Name (when document is loaded) */}
            {state.document && (
              <div className="hidden md:flex flex-col items-center justify-center flex-1 min-w-0 px-4">
                <div className="text-sm font-semibold text-slate-900 truncate max-w-full text-center">
                  📄 {state.document.filename}
                </div>
                <div className="text-xs text-slate-600 mt-0.5">
                  {Object.keys(state.document.filledValues).length} / {state.document.placeholders.length} fields completed
                </div>
              </div>
            )}

            {/* Right: Login/Sign Out Button */}
            <div className="flex-shrink-0">
              <LoginButton />
            </div>
          </div>
          
          {/* Mobile Document Info (shown below header on mobile) */}
          {state.document && (
            <div className="md:hidden mt-3 pt-3 border-t border-slate-200">
              <div className="text-sm font-medium text-slate-900 truncate">
                📄 {state.document.filename}
              </div>
              <div className="text-xs text-slate-600 mt-1">
                {Object.keys(state.document.filledValues).length} / {state.document.placeholders.length} fields completed
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        <div className="max-w-full w-full flex-1 flex overflow-hidden">
          {/* Error Display */}
          {state.error && (
            <div className="fixed top-20 left-4 right-4 max-w-md mx-auto z-50 animate-slideInRight">
              <div className="bg-red-50 border border-red-200 rounded-lg shadow-lg">
                <div className="p-4 flex items-center gap-3">
                  <AlertCircle className="h-5 w-5 text-red-600 flex-shrink-0" />
                  <p className="text-sm text-red-800 flex-1">{state.error}</p>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setState((prev) => ({ ...prev, error: null }))}
                    className="ml-auto text-red-600 hover:text-red-700 hover:bg-red-100"
                  >
                    ✕
                  </Button>
                </div>
              </div>
            </div>
          )}

          {/* Auth-gated Hero or Upload */}
          {!hasDocument && (
            <div className="px-4 md:px-8 py-12 flex items-center justify-center w-full animate-fadeIn">
              <div className="max-w-4xl w-full">
                {!user ? (
                  <div className="text-center space-y-8">
                    <div className="space-y-4">
                      <h2 className="text-3xl md:text-4xl font-bold text-foreground">Fill legal docs in minutes</h2>
                      <p className="text-muted-foreground max-w-2xl mx-auto">
                        Sign in to start a guided, AI-assisted workflow for uploading a .docx template,
                        answering a few questions, and downloading a clean, completed contract.
                      </p>
                    </div>
                    <div className="flex items-center justify-center">
                      <LoginButton />
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
                      <Card className="p-4"><p className="text-sm text-slate-700">Smart placeholder detection</p></Card>
                      <Card className="p-4"><p className="text-sm text-slate-700">Inline preview & edits</p></Card>
                      <Card className="p-4"><p className="text-sm text-slate-700">Download ready .docx</p></Card>
                    </div>
                  </div>
                ) : (
                  <div className="max-w-2xl w-full">
                    <UploadZone
                      onUpload={handleUpload}
                      isLoading={state.isLoading}
                      uploadedFile={uploadedFile}
                    />
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Main Content - Fixed Sidebars with Scrollable Center */}
          {hasDocument && state.document && (
            <div className="flex-1 flex relative">
              {/* Smooth loading overlay during processing */}
              {state.isLoading && (
                <div className="pointer-events-none absolute inset-0 z-40 flex items-center justify-center bg-white/60 backdrop-blur-sm animate-fadeIn">
                  <div className="flex items-center gap-2 text-sm text-slate-700 bg-white border border-slate-300 px-4 py-2 rounded-full shadow-lg">
                    <span className="h-2 w-2 rounded-full bg-blue-600 animate-pulse"></span>
                    Processing...
                  </div>
                </div>
              )}
              {/* LEFT: Progress Tracker - FIXED POSITION */}
              <div className="hidden xl:block fixed left-0 top-[120px] bottom-[80px] w-72 z-30">
                <div className="h-full border-r border-slate-200 bg-white shadow-sm">
                  <div className="h-full overflow-y-auto overflow-x-hidden scrollbar-hide">
                    <ProgressTracker
                      placeholders={state.document.placeholders}
                      filledValues={state.document.filledValues}
                      currentIndex={state.currentIndex}
                      progress={state.progress}
                    />
                  </div>
                </div>
              </div>

              {/* CENTER: Document Preview - SCROLLABLE CONTENT */}
              <div className="flex-1 xl:ml-72 md:mr-[360px]">
                <div className="h-full overflow-y-auto overflow-x-hidden scrollbar-hide">
                  <div className="max-w-6xl mx-auto w-full p-4 sm:p-6 lg:p-8 transition-all duration-300">
                    <DocumentPreview
                      previewHtml={state.previewHtml}
                      isLoading={state.isLoading && !state.previewHtml}
                      onEditField={handleEditField}
                      sessionId={state.sessionId}
                      onFillField={handleFillFieldDirectly}
                      currentIndex={state.currentIndex}
                      placeholders={state.document?.placeholders || []}
                      filledValues={state.document?.filledValues || {}}
                    />
                  </div>
                </div>
              </div>

              {/* RIGHT: Assistant panel with tabs - FIXED POSITION */}
              <div className="hidden md:block fixed right-0 top-[130px] bottom-[76px] w-[340px] z-60">
                <div className="h-full bg-white border-l border-slate-200 shadow-lg">
                  <div className="border-b border-slate-200 p-2 flex gap-1">
                    <button
                      className={`flex-1 text-xs py-1.5 rounded-md transition-colors ${assistantTab === 'doc' ? 'bg-blue-100 text-blue-700 font-semibold' : 'text-slate-600 hover:bg-slate-100'}`}
                      onClick={() => setAssistantTab('doc')}
                    >
                      Doc Assistant
                    </button>
                    <button
                      className={`flex-1 text-xs py-1.5 rounded-md transition-colors ${assistantTab === 'ai' ? 'bg-blue-100 text-blue-700 font-semibold' : 'text-slate-600 hover:bg-slate-100'}`}
                      onClick={() => setAssistantTab('ai')}
                    >
                      AI
                    </button>
                  </div>
                  {assistantTab === 'doc' ? (
                    <ChatInterface
                      messages={state.chatMessages}
                      onSendMessage={handleSendMessage}
                      isLoading={state.isLoading}
                      disabled={state.isComplete}
                      initialMessage={initialMessage}
                      currentKey={state.document?.placeholders[state.currentIndex]?.id ?? state.document?.placeholders[state.currentIndex]?.key ?? null}
                      currentValue={
                        state.document?.placeholders[state.currentIndex]?.id
                          ? state.document?.filledValues[state.document.placeholders[state.currentIndex].id!] ?? ''
                          : state.document?.placeholders[state.currentIndex]?.key
                          ? state.document?.filledValues[state.document.placeholders[state.currentIndex].key] ?? ''
                          : ''
                      }
                    />
                  ) : (
                    <ChatInterface
                      messages={aiMessages}
                      onSendMessage={handleSendAIMessage}
                      isLoading={aiLoading}
                      disabled={false}
                      initialMessage={state.document 
                        ? `I can help you understand this document! Ask me to:\n• Summarize the document\n• Explain specific sections or fields\n• Answer legal questions about the content\n• Clarify any terms or clauses\n\nI have full access to your ${state.document.filename} and can help with both document-specific and general legal questions.`
                        : 'Ask me anything! Once you upload a document, I can help you understand it, answer questions about it, and provide legal guidance.'}
                    />
                  )}
                </div>
              </div>

              {/* MOBILE: Chat Fixed Window at Bottom (NO SCROLL) */}
              {(assistantTab === 'doc' ? state.chatMessages.length > 0 : aiMessages.length > 0) && (
                <div className="md:hidden fixed bottom-20 right-4 left-4 max-w-md h-[35vh] bg-white border border-slate-300 rounded-2xl flex flex-col shadow-2xl z-50 animate-slideInRight overflow-hidden min-h-0">
                  {assistantTab === 'doc' ? (
                    <ChatInterface
                      messages={state.chatMessages}
                      onSendMessage={handleSendMessage}
                      isLoading={state.isLoading}
                      disabled={state.isComplete}
                      initialMessage={initialMessage}
                      currentKey={state.document?.placeholders[state.currentIndex]?.id ?? state.document?.placeholders[state.currentIndex]?.key ?? null}
                      currentValue={
                        state.document?.placeholders[state.currentIndex]?.id
                          ? state.document?.filledValues[state.document.placeholders[state.currentIndex].id!] ?? ''
                          : state.document?.placeholders[state.currentIndex]?.key
                          ? state.document?.filledValues[state.document.placeholders[state.currentIndex].key] ?? ''
                          : ''
                      }
                    />
                  ) : (
                    <ChatInterface
                      messages={aiMessages}
                      onSendMessage={handleSendAIMessage}
                      isLoading={aiLoading}
                      disabled={false}
                      initialMessage={state.document 
                        ? `I can help you understand this document! Ask me to:\n• Summarize the document\n• Explain specific sections\n• Answer legal questions\n\nI have access to your ${state.document.filename}.`
                        : 'Ask me anything! I can help with general questions or, once you upload a document, answer questions about it.'}
                    />
                  )}
                </div>
              )}
            </div>
          )}
        </div>

        {/* Action Buttons Footer - Below main content */}
        {hasDocument && state.document && (
          <div className="border-t border-slate-200 bg-white shadow-lg">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3 sm:py-4 flex flex-col sm:flex-row gap-2 sm:gap-3">
              {state.isComplete && state.downloadUrl ? (
                <>
                  <Button
                    onClick={handleDownload}
                    className="flex-1 order-1 sm:order-none hover:shadow-lg transition-all duration-300"
                    size="lg"
                  >
                    <Download className="h-4 w-4 mr-2" />
                    Download Document
                  </Button>
                  <Button
                    onClick={handleReset}
                    variant="outline"
                    className="flex-1 order-2 sm:order-none transition-all duration-300"
                  >
                    <RefreshCw className="h-4 w-4 mr-2" />
                    Start New
                  </Button>
                </>
              ) : (
                <>
                  <Button
                    onClick={handleComplete}
                    disabled={
                      state.isLoading ||
                      state.progress < 100 ||
                      (state.document?.placeholders.length || 0) !==
                        Object.keys(state.document?.filledValues || {}).length
                    }
                    className="flex-1 order-1 sm:order-none hover:shadow-lg transition-all duration-300 disabled:opacity-50"
                    size="lg"
                  >
                    <CheckCircle2 className="h-4 w-4 mr-2" />
                    {state.isLoading ? 'Processing...' : 'Complete'}
                  </Button>
                  <Button
                    onClick={handleReset}
                    variant="outline"
                    className="flex-1 order-2 sm:order-none transition-all duration-300"
                    disabled={state.isLoading}
                  >
                    <RefreshCw className="h-4 w-4 mr-2" />
                    Reset
                  </Button>
                </>
              )}
            </div>
          </div>
        )}

        {/* Mobile Progress Bar - Shown only on small screens when document is open */}
        {hasDocument && state.document && (
          <div className="xl:hidden border-t border-slate-200 bg-white px-4 py-3">
            <div className="space-y-2">
              <div className="flex items-center justify-between text-xs">
                <span className="font-semibold text-slate-700">Progress</span>
                <span className="text-blue-600 font-bold">{state.progress.toFixed(0)}%</span>
              </div>
              <div className="relative h-2 bg-slate-200 rounded-full overflow-hidden">
                <div
                  className="absolute inset-y-0 left-0 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-full transition-all duration-500 ease-out"
                  style={{ width: `${state.progress}%` }}
                />
              </div>
              <div className="flex gap-2 text-xs text-slate-600">
                <span>{Object.keys(state.document.filledValues).length} completed</span>
                <span>•</span>
                <span>{state.document.placeholders.length - Object.keys(state.document.filledValues).length} remaining</span>
              </div>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}



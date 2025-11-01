'use client';

import { useEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { ScrollArea } from './ui/scroll-area';
import { Input } from './ui/input';
import { FileText, Check, X } from 'lucide-react';
import { Button } from './ui/button';

interface DocumentPreviewProps {
  previewHtml: string | null;
  isLoading?: boolean;
  onEditField?: (fieldKey: string, currentValue: string) => void;
  onFillField?: (fieldKey: string, value: string) => Promise<void>;
  sessionId?: string | null;
  currentIndex?: number | null;
  placeholders?: Array<{ id?: string; key: string; name: string }>; // For Tab navigation
  filledValues?: Record<string, string>; // To check which fields are filled
}

export function DocumentPreview({ 
  previewHtml, 
  isLoading = false,
  onEditField,
  onFillField,
  sessionId,
  currentIndex,
  placeholders = [],
  filledValues = {}
}: DocumentPreviewProps) {
  const previewRef = useRef<HTMLDivElement>(null);
  const [editingField, setEditingField] = useState<{
    key: string;
    value: string;
    element: HTMLElement;
    placeholder: string;
  } | null>(null);
  const [editValue, setEditValue] = useState('');
  const [isSaving, setIsSaving] = useState(false);
  
  // Auto-scroll to current field
  useEffect(() => {
    if (!previewRef.current || currentIndex === null || currentIndex === undefined) return;
    
    // Find the current placeholder element
    const currentField = previewRef.current.querySelector(`[data-index="${currentIndex}"]`);
    if (currentField) {
      currentField.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  }, [currentIndex]);
  
  // Event delegation for placeholder clicks - inline editing mode (Canva-like)
  useEffect(() => {
    if (!previewRef.current || (!onFillField && !onEditField)) return;

    const container = previewRef.current;
    
    const handleClick = (e: MouseEvent) => {
      const target = e.target as HTMLElement | null;
      if (!target) return;
      
      // Don't open edit if clicking on input/button
      if (target.closest('.inline-edit-wrapper')) return;

      // Clickable for ANY placeholder (filled/current/unfilled)
      const el = target.closest<HTMLElement>('[data-ph]');
      if (!el) {
        // Click outside - close editor
        if (editingField) {
          setEditingField(null);
          setEditValue('');
        }
        return;
      }

      // Single click to edit
      const fieldKey = el.getAttribute('data-ph') || el.getAttribute('data-key') || '';
      const currentValue = el.textContent?.trim() || '';
      const placeholder = el.getAttribute('data-name') || el.getAttribute('title') || 'Enter value';

      // If we have onFillField, use inline editing
      if (onFillField) {
        e.stopPropagation(); // Prevent event bubbling
        
        // Calculate position immediately
        const rect = el.getBoundingClientRect();
        const containerRect = previewRef.current?.getBoundingClientRect();
        
        if (!containerRect) return;
        
        // Calculate position relative to the document preview container
        const relativeLeft = rect.left - containerRect.left;
        const relativeTop = rect.top - containerRect.top;
        
        // Ensure editor stays within container boundaries
        const editorWidth = Math.max(rect.width, 280);
        const editorHeight = 120; // Approximate editor height
        
        // Constrain horizontal position
        let constrainedLeft = Math.max(10, relativeLeft);
        constrainedLeft = Math.min(constrainedLeft, containerRect.width - editorWidth - 10);
        
        // Constrain vertical position (prefer above, but below if no space)
        let constrainedTop = relativeTop - 80;
        if (constrainedTop < 10) {
          constrainedTop = relativeTop + rect.height + 10;
        }
        if (constrainedTop + editorHeight > containerRect.height - 10) {
          constrainedTop = containerRect.height - editorHeight - 10;
        }
        
        const position = {
          left: constrainedLeft,
          top: constrainedTop,
          minWidth: editorWidth,
          // Store original coords for reference
          rectLeft: relativeLeft,
          rectTop: relativeTop,
        };
        
        // Show editor immediately
        setEditorPosition(position);
        setEditingField({
          key: fieldKey,
          value: currentValue,
          element: el,
          placeholder: placeholder
        });
        setEditValue(currentValue);
        
        // Optionally scroll into view (but don't wait for it)
        el.scrollIntoView({ behavior: 'smooth', block: 'center' });
      } else if (onEditField) {
        // Fallback to modal/edit dialog
      onEditField(fieldKey, currentValue);
      }
    };

    // Close editor when clicking outside
    const handleOutsideClick = (e: MouseEvent) => {
      const target = e.target as HTMLElement;
      if (editingField && !target.closest('.inline-edit-wrapper') && 
          !target.closest('[data-ph]') && !target.closest('[data-key]')) {
        setEditingField(null);
        setEditValue('');
        setEditorPosition(null);
      }
    };

    container.addEventListener('click', handleClick);
    document.addEventListener('click', handleOutsideClick);
    
    return () => {
      container.removeEventListener('click', handleClick);
      document.removeEventListener('click', handleOutsideClick);
    };
  }, [previewHtml, onEditField, onFillField, editingField]);
  
  const findNextPlaceholder = (currentKey: string): HTMLElement | null => {
    if (!previewRef.current || !placeholders.length) return null;
    
    // Find current placeholder index
    const currentIdx = placeholders.findIndex(p => 
      (p.id === currentKey) || (p.key === currentKey)
    );
    
    if (currentIdx === -1) return null;
    
    // Find next unfilled placeholder
    for (let i = currentIdx + 1; i < placeholders.length; i++) {
      const ph = placeholders[i];
      const phId = ph.id || ph.key;
      const isFilled = phId in filledValues || ph.key in filledValues;
      
      if (!isFilled) {
        // Find element in DOM
        const el = previewRef.current.querySelector(
          `[data-ph="${phId}"], [data-key="${ph.key}"], [data-ph="${ph.key}"]`
        ) as HTMLElement;
        if (el) return el;
      }
    }
    
    // If no unfilled found after current, search from beginning
    for (let i = 0; i < currentIdx; i++) {
      const ph = placeholders[i];
      const phId = ph.id || ph.key;
      const isFilled = phId in filledValues || ph.key in filledValues;
      
      if (!isFilled) {
        const el = previewRef.current.querySelector(
          `[data-ph="${phId}"], [data-key="${ph.key}"], [data-ph="${ph.key}"]`
        ) as HTMLElement;
        if (el) return el;
      }
    }
    
    return null;
  };
  
  const handleSave = async () => {
    if (!editingField || !onFillField || !editValue.trim()) return;
    
    setIsSaving(true);
    try {
      await onFillField(editingField.key, editValue.trim());
      setEditingField(null);
      setEditValue('');
      setEditorPosition(null);
    } catch (error) {
      console.error('Error saving field:', error);
      // Keep editor open on error
    } finally {
      setIsSaving(false);
    }
  };
  
  const handleSaveAndNext = async () => {
    if (!editingField || !onFillField || !editValue.trim()) return;
    
    setIsSaving(true);
    try {
      await onFillField(editingField.key, editValue.trim());
      
      // Find next placeholder
      const nextEl = findNextPlaceholder(editingField.key);
      
      if (nextEl) {
        // Move to next field
        const fieldKey = nextEl.getAttribute('data-ph') || nextEl.getAttribute('data-key') || '';
        const currentValue = nextEl.textContent?.trim() || '';
        const placeholder = nextEl.getAttribute('data-name') || nextEl.getAttribute('title') || 'Enter value';
        
        // Scroll to next field
        nextEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
        
        // Smooth transition to next field
        // First update position to create smooth slide effect
        requestAnimationFrame(() => {
          const rect = nextEl.getBoundingClientRect();
          const newPosition = {
            left: rect.left,
            top: rect.top - 80,
            minWidth: Math.max(rect.width, 280),
            rectLeft: rect.left,
            rectTop: rect.top,
          };
          
          // Update position first for smooth transition
          setEditorPosition(newPosition);
          
          // Then update field after a brief moment for smoothness
          requestAnimationFrame(() => {
            setEditingField({
              key: fieldKey,
              value: currentValue,
              element: nextEl,
              placeholder: placeholder
            });
            setEditValue(currentValue);
            setIsSaving(false);
            
            // Focus input in next frame
            setTimeout(() => {
              const input = document.querySelector('.inline-edit-wrapper input') as HTMLInputElement;
              if (input) {
                input.focus();
                input.select();
              }
            }, 50);
          });
        });
      } else {
        // No next field - close editor
        setEditingField(null);
        setEditValue('');
        setEditorPosition(null);
        setIsSaving(false);
      }
    } catch (error) {
      console.error('Error saving field:', error);
      setIsSaving(false);
    }
  };
  
  const handleCancel = () => {
    setEditingField(null);
    setEditValue('');
  };
  
  const [editorPosition, setEditorPosition] = useState<{
    left: number;
    top: number;
    minWidth: number;
    rectLeft?: number;
    rectTop?: number;
  } | null>(null);
  const [mounted, setMounted] = useState(false);
  
  useEffect(() => {
    setMounted(true);
  }, []);
  
  // Update editor position when scrolling or resizing
  useEffect(() => {
    if (!editingField || !editorPosition) return;
    
    const updatePosition = () => {
      // Re-query the element to get fresh position
      const el = previewRef.current?.querySelector(
        `[data-ph="${editingField.key}"], [data-key="${editingField.key}"]`
      ) as HTMLElement;
      
      if (el && previewRef.current) {
        const rect = el.getBoundingClientRect();
        const containerRect = previewRef.current.getBoundingClientRect();
        
        // Calculate position relative to container
        const relativeLeft = rect.left - containerRect.left;
        const relativeTop = rect.top - containerRect.top;
        
        // Ensure editor stays within container boundaries
        const editorWidth = Math.max(rect.width, 280);
        const editorHeight = 120;
        
        // Constrain horizontal position
        let constrainedLeft = Math.max(10, relativeLeft);
        constrainedLeft = Math.min(constrainedLeft, containerRect.width - editorWidth - 10);
        
        // Constrain vertical position (prefer above, but below if no space)
        let constrainedTop = relativeTop - 80;
        if (constrainedTop < 10) {
          constrainedTop = relativeTop + rect.height + 10;
        }
        if (constrainedTop + editorHeight > containerRect.height - 10) {
          constrainedTop = containerRect.height - editorHeight - 10;
        }
        
        setEditorPosition(prev => {
          if (!prev) return null;
          
          return {
            ...prev,
            left: constrainedLeft,
            top: constrainedTop,
            rectLeft: relativeLeft,
            rectTop: relativeTop,
          };
        });
      }
    };
    
    // Use requestAnimationFrame for smooth updates
    const rafUpdate = () => {
      requestAnimationFrame(updatePosition);
    };
    
    // Update on scroll/resize with debouncing via RAF
    window.addEventListener('scroll', rafUpdate, true);
    window.addEventListener('resize', rafUpdate);
    
    // Also listen to scroll within the preview container
    const previewContainer = previewRef.current?.querySelector('[data-radix-scroll-area-viewport]');
    if (previewContainer) {
      previewContainer.addEventListener('scroll', rafUpdate, true);
    }
    
    return () => {
      window.removeEventListener('scroll', rafUpdate, true);
      window.removeEventListener('resize', rafUpdate);
      if (previewContainer) {
        previewContainer.removeEventListener('scroll', rafUpdate, true);
      }
    };
  }, [editingField, editorPosition]);
  // Loading state
  if (isLoading) {
    return (
      <Card className="border-slate-200 bg-white">
        <CardHeader className="border-b border-slate-200">
          <CardTitle className="flex items-center gap-2">
            <FileText className="h-5 w-5 text-primary" />
            Document Preview
          </CardTitle>
        </CardHeader>
        <CardContent className="flex items-center justify-center h-[400px]">
          <div className="text-center">
            <div className="inline-flex items-center justify-center w-12 h-12 rounded-full bg-primary/10 mb-3">
              <FileText className="h-6 w-6 text-primary animate-pulse" />
            </div>
            <p className="text-sm text-slate-600">Loading document...</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!previewHtml) {
    return (
      <Card className="border-slate-200 bg-white">
        <CardHeader className="border-b border-slate-200">
          <CardTitle className="flex items-center gap-2">
            <FileText className="h-5 w-5 text-primary" />
            Document Preview
          </CardTitle>
        </CardHeader>
        <CardContent className="flex items-center justify-center h-[400px]">
          <p className="text-sm text-slate-500">No document loaded</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2 mb-2">
        <div className="w-1 h-5 bg-primary rounded-full" />
        <h3 className="text-sm font-semibold text-slate-900">Document Preview</h3>
      </div>
      
      {/* Render the preview HTML with enhanced styling */}
    <Card className="border-2 border-gray-200 bg-white shadow-sm flex flex-col h-full relative">
      <CardContent className="flex-1 overflow-hidden p-0">
        <ScrollArea className="h-full w-full p-6">
          <div
            ref={previewRef}
            className="document-preview-content prose prose-sm max-w-none text-black"
            dangerouslySetInnerHTML={{ __html: previewHtml }}
            style={{
              backgroundColor: 'white',
              borderRadius: '8px',
              padding: '2rem',
              minHeight: '100%',
              color: '#333',
            }}
          />
          <style jsx global>{`
            .document-preview-content {
              font-family: 'Calibri', 'Arial', sans-serif;
              color: #333;
              background-color: white !important;
            }
            /* Remove ALL yellow/brown/beige colors from document preview */
            .document-preview-content .placeholder-current {
              background-color: #fee2e2 !important;
              color: #991b1b !important;
              padding: 4px 8px;
              border-radius: 4px;
              font-weight: 700;
              border: 2px solid #dc2626 !important;
              box-shadow: 0 0 8px rgba(220, 38, 38, 0.3);
              display: inline-block;
            }
            .document-preview-content .placeholder-filled {
              background-color: #d1fae5 !important;
              color: #065f46 !important;
              padding: 2px 6px;
              border-radius: 3px;
              font-weight: 600;
              border: 1px solid #6ee7b7 !important;
              transition: all 0.2s;
            }
            .document-preview-content .placeholder-filled:hover {
              background-color: #a7f3d0 !important;
              text-decoration: underline;
              cursor: pointer;
            }
            .document-preview-content .placeholder-current {
              cursor: pointer;
            }
            .document-preview-content .placeholder-unfilled {
              cursor: pointer;
              background-color: transparent !important;
              color: #666 !important;
              padding: 2px 6px;
              border-radius: 3px;
              font-weight: 500;
              border: 1px dashed #d1d5db !important;
              opacity: 0.6;
            }
            /* Override table backgrounds - no yellow/brown */
            .document-preview-content table th,
            .document-preview-content .document-table th {
              background-color: #f3f4f6 !important;
            }
            .document-preview-content table tr:nth-child(even),
            .document-preview-content .document-table tr:nth-child(even) {
              background-color: #ffffff !important;
            }
            /* Remove any inline styles with yellow/brown colors */
            .document-preview-content [style*="#ff"],
            .document-preview-content [style*="#FF"],
            .document-preview-content [style*="yellow"],
            .document-preview-content [style*="Yellow"],
            .document-preview-content [style*="rgb(255, 255"],
            .document-preview-content [style*="rgb(255,193"],
            .document-preview-content [style*="rgb(255,235"],
            .document-preview-content [style*="#f8d7da"],
            .document-preview-content [style*="#fafafa"],
            .document-preview-content [style*="#f5f5f5"] {
              background-color: transparent !important;
              color: #333 !important;
            }
          `}</style>
        </ScrollArea>
      </CardContent>
      
      {/* Inline Editor (Canva-like) - Positioned within document preview */}
      {mounted && editingField && editorPosition && (
        <div
          className="inline-edit-wrapper absolute z-[1000] bg-white border-2 border-blue-500 rounded-lg shadow-xl p-2 flex flex-col gap-2"
          style={{
            left: `${editorPosition.left}px`,
            top: `${editorPosition.top}px`,
            minWidth: `${editorPosition.minWidth}px`,
            maxWidth: '400px',
            opacity: 1,
            transform: 'translateY(0) scale(1)',
            transition: 'opacity 0.15s ease-out, transform 0.15s cubic-bezier(0.4, 0, 0.2, 1), left 0.2s cubic-bezier(0.4, 0, 0.2, 1), top 0.2s cubic-bezier(0.4, 0, 0.2, 1)',
            animation: 'slideInUp 0.2s ease-out',
          }}
          onClick={(e) => e.stopPropagation()}
          onMouseDown={(e) => e.stopPropagation()}
        >
          <style jsx global>{`
            @keyframes slideInUp {
              from {
                opacity: 0;
                transform: translateY(10px) scale(0.95);
              }
              to {
                opacity: 1;
                transform: translateY(0) scale(1);
              }
            }
          `}</style>
          <Input
            type="text"
            value={editValue}
            onChange={(e) => setEditValue(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter') {
                e.preventDefault();
                handleSave();
              } else if (e.key === 'Tab' && !e.shiftKey) {
                e.preventDefault();
                handleSaveAndNext();
              } else if (e.key === 'Escape') {
                handleCancel();
              }
            }}
            placeholder={editingField.placeholder}
            className="w-full"
            autoFocus
            disabled={isSaving}
          />
          <div className="flex items-center justify-between">
            <span className="text-xs text-gray-500">
              Press <kbd className="px-1.5 py-0.5 bg-gray-100 rounded text-xs font-mono">Tab</kbd> to save & next
            </span>
            <div className="flex gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={handleCancel}
                disabled={isSaving}
              >
                <X className="h-4 w-4 mr-1" />
                Cancel
              </Button>
              <Button
                size="sm"
                onClick={handleSave}
                disabled={isSaving || !editValue.trim()}
              >
                <Check className="h-4 w-4 mr-1" />
                {isSaving ? 'Saving...' : 'Save'}
              </Button>
            </div>
          </div>
        </div>
      )}
    </Card>
    </div>
  );
}


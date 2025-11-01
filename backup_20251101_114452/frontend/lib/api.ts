import type {
  UploadResponse,
  ChatResponse,
  PreviewResponse,
  CompleteResponse,
  ErrorResponse,
} from './types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5001';

// Optional auth token (Firebase) injected from UI
let AUTH_TOKEN: string | null = null;
export function setAuthToken(token: string | null) {
  AUTH_TOKEN = token;
}

function withAuth(headers: HeadersInit = {}): HeadersInit {
  if (AUTH_TOKEN) {
    return { ...headers, Authorization: `Bearer ${AUTH_TOKEN}` };
  }
  return headers;
}

class ApiError extends Error {
  constructor(
    public status: number,
    public error: string,
    message: string
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

async function handleResponse<T>(response: Response): Promise<T> {
  const contentType = response.headers.get('content-type');
  
  if (!response.ok) {
    if (contentType && contentType.includes('application/json')) {
      const errorData: ErrorResponse = await response.json();
      throw new ApiError(
        response.status,
        errorData.error || 'Unknown error',
        errorData.message || 'An error occurred'
      );
    }
    throw new ApiError(
      response.status,
      'Network error',
      `HTTP ${response.status}: ${response.statusText}`
    );
  }

  if (contentType && contentType.includes('application/json')) {
    return response.json();
  }

  return response.text() as Promise<T>;
}

export const api = {
  async uploadDocument(file: File): Promise<UploadResponse> {
    const formData = new FormData();
    formData.append('document', file);

    const response = await fetch(`${API_URL}/api/upload`, {
      method: 'POST',
      headers: withAuth(),
      body: formData,
    });

    return handleResponse<UploadResponse>(response);
  },

  async sendMessage(sessionId: string, message: string): Promise<ChatResponse> {
    const response = await fetch(`${API_URL}/api/chat`, {
      method: 'POST',
      headers: withAuth({ 'Content-Type': 'application/json' }),
      body: JSON.stringify({
        session_id: sessionId,
        message: message,
      }),
    });

    return handleResponse<ChatResponse>(response);
  },

  async getPreview(sessionId: string): Promise<PreviewResponse> {
    const response = await fetch(
      `${API_URL}/api/preview?session_id=${sessionId}`,
      {
        method: 'GET',
        headers: withAuth(),
      }
    );

    return handleResponse<PreviewResponse>(response);
  },

  async completeDocument(sessionId: string): Promise<CompleteResponse> {
    const response = await fetch(`${API_URL}/api/complete`, {
      method: 'POST',
      headers: withAuth({ 'Content-Type': 'application/json' }),
      body: JSON.stringify({
        session_id: sessionId,
      }),
    });

    return handleResponse<CompleteResponse>(response);
  },

  async downloadDocument(filename: string): Promise<Blob> {
    const response = await fetch(`${API_URL}/api/download/${filename}`, {
      method: 'GET',
      headers: withAuth(),
    });

    if (!response.ok) {
      const errorData: ErrorResponse = await response.json();
      throw new ApiError(
        response.status,
        errorData.error || 'Download failed',
        errorData.message || 'Unable to download file'
      );
    }

    return response.blob();
  },

  async resetSession(sessionId: string): Promise<void> {
    const response = await fetch(`${API_URL}/api/reset`, {
      method: 'POST',
      headers: withAuth({ 'Content-Type': 'application/json' }),
      body: JSON.stringify({
        session_id: sessionId,
      }),
    });

    if (!response.ok) {
      const errorData: ErrorResponse = await response.json();
      throw new ApiError(
        response.status,
        errorData.error || 'Reset failed',
        errorData.message || 'Unable to reset session'
      );
    }
  },

  async editField(
    sessionId: string,
    fieldKey: string,
    newValue: string
  ): Promise<PreviewResponse> {
    const response = await fetch(`${API_URL}/api/edit`, {
      method: 'POST',
      headers: withAuth({ 'Content-Type': 'application/json' }),
      body: JSON.stringify({
        session_id: sessionId,
        field_key: fieldKey,
        value: newValue,
      }),
    });

    return handleResponse<PreviewResponse>(response);
  },

  async healthCheck(): Promise<{ status: string }> {
    const response = await fetch(`${API_URL}/api/health`, { method: 'GET', headers: withAuth() });

    return handleResponse<{ status: string }>(response);
  },

  async checkSessionHealth(sessionId: string): Promise<{
    valid: boolean;
    session_id?: string;
    has_document?: boolean;
    placeholders_count?: number;
    filled_count?: number;
    last_accessed?: string;
    session_expired?: boolean;
    error?: string;
    message?: string;
  }> {
    const response = await fetch(`${API_URL}/api/session/health?session_id=${sessionId}`, {
      method: 'GET',
      headers: withAuth(),
    });

    return handleResponse(response);
  },

  async fillFieldDirectly(
    sessionId: string,
    fieldKey: string,
    value: string
  ): Promise<PreviewResponse & {
    success: boolean;
    message: string;
    auto_filled?: string[];
    next_index?: number | null;
  }> {
    const response = await fetch(`${API_URL}/api/fill`, {
      method: 'POST',
      headers: withAuth({ 'Content-Type': 'application/json' }),
      body: JSON.stringify({
        session_id: sessionId,
        field_key: fieldKey,
        value: value,
      }),
    });

    return handleResponse(response);
  },

  async getAllSessions(limit: number = 100): Promise<{
    success: boolean;
    sessions: Array<{
      session_id: string;
      filename: string;
      created_at: string;
      last_accessed_at: string;
      progress: number;
      status: string;
      placeholders_count: number;
      filled_count: number;
    }>;
    count: number;
  }> {
    const response = await fetch(`${API_URL}/api/sessions?limit=${limit}`, {
      method: 'GET',
      headers: withAuth(),
    });

    return handleResponse(response);
  },

  async getSessionHistory(sessionId: string, limit: number = 50): Promise<{
    success: boolean;
    session_id: string;
    history: Array<{
      timestamp: string;
      event_type: string;
      data: any;
    }>;
    count: number;
  }> {
    const response = await fetch(
      `${API_URL}/api/sessions/history?session_id=${sessionId}&limit=${limit}`,
      {
        method: 'GET',
        headers: withAuth(),
      }
    );

    return handleResponse(response);
  },

  async getSessionStats(): Promise<{
    success: boolean;
    stats: {
      total_sessions: number;
      active_sessions: number;
      completed_sessions: number;
      average_progress: number;
      total_placeholders: number;
      total_filled: number;
    };
  }> {
    const response = await fetch(`${API_URL}/api/sessions/stats`, {
      method: 'GET',
      headers: withAuth(),
    });

    return handleResponse(response);
  },
};

export { ApiError };

// Streaming Groq helper
export async function streamGroq(
  prompt: string,
  onDelta: (chunk: string) => void,
  model?: string
): Promise<string> {
  try {
    const response = await fetch(`${API_URL}/api/groq/stream`, {
      method: 'POST',
      headers: withAuth({ 'Content-Type': 'application/json', Accept: 'text/plain' }),
      body: JSON.stringify({ prompt, model }),
    });

    if (!response.ok || !response.body) {
      throw new Error(`HTTP ${response.status}`);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let finalText = '';
    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      const chunk = decoder.decode(value, { stream: true });
      if (chunk) {
        finalText += chunk;
        onDelta(chunk);
      }
    }
    return finalText;
  } catch (err) {
    // Fallback to non-streaming endpoint
    const response = await fetch(`${API_URL}/api/groq`, {
      method: 'POST',
      headers: withAuth({ 'Content-Type': 'application/json' }),
      body: JSON.stringify({ prompt, model }),
    });
    if (!response.ok) {
      const text = await response.text();
      throw new ApiError(response.status, 'Groq request failed', text || 'Request failed');
    }
    const data = await response.json();
    const text: string = data.text || '';
    if (text) onDelta(text);
    return text;
  }
}


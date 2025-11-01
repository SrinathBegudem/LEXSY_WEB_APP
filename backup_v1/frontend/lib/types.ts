export interface Placeholder {
  id?: string;  // NEW: unique occurrence id
  key: string;
  name: string;
  original: string;
  type: string;
  pattern_type?: string;
  location?: any;
  location_type?: string;
  position?: [number, number];
  context?: string;
  required?: boolean;
  suggestions?: string[];
  sequence?: number;
}

export interface UploadResponse {
  success: boolean;
  session_id: string;
  filename: string;
  placeholders_count: number;
  placeholders: Placeholder[];
  message: string;
  initial_message: string;
}

export interface ChatResponse {
  response: string;
  placeholder_filled: boolean;
  current_progress: number;
  total_placeholders: number;
  progress_percentage: number;
  all_filled: boolean;
  filled_values: Record<string, string>;
  current_placeholder?: Placeholder;
  preview?: string;  // NEW: fresh preview HTML from server
}

export interface PreviewResponse {
  preview: string;
  filled_count: number;
  total_count: number;
  progress_percentage: number;
  placeholders: Placeholder[];
  filled_values: Record<string, string>;
  current_index?: number | null;
}

export interface CompleteResponse {
  success: boolean;
  download_url: string;
  filename: string;
  message: string;
}

export interface ErrorResponse {
  error: string;
  message: string;
}

export interface AppState {
  sessionId: string | null;
  document: {
    filename: string | null;
    placeholders: Placeholder[];
    filledValues: Record<string, string>;
  } | null;
  currentIndex: number;
  progress: number;
  isLoading: boolean;
  error: string | null;
  chatMessages: ChatMessage[];
  previewHtml: string | null;
  isComplete: boolean;
  downloadUrl: string | null;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  placeholderFilled?: boolean;
}


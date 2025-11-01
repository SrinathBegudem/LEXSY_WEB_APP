'use client';

import { useCallback, useState } from 'react';
import { Upload, FileText, X } from 'lucide-react';
import { Card, CardContent } from './ui/card';
import { Button } from './ui/button';
import { cn } from '@/lib/utils';

interface UploadZoneProps {
  onUpload: (file: File) => void;
  isLoading?: boolean;
  uploadedFile?: File | null;
}

export function UploadZone({ onUpload, isLoading = false, uploadedFile }: UploadZoneProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const validateFile = (file: File): boolean => {
    const validExtensions = ['.docx', '.doc'];
    const fileExtension = '.' + file.name.split('.').pop()?.toLowerCase();
    
    if (!validExtensions.includes(fileExtension)) {
      setError('Please upload a .docx file. Other formats are not supported.');
      return false;
    }

    const maxSize = 10 * 1024 * 1024; // 10MB
    if (file.size > maxSize) {
      setError('File size exceeds 10MB limit. Please upload a smaller file.');
      return false;
    }

    setError(null);
    return true;
  };

  const handleFile = useCallback((file: File) => {
    if (validateFile(file)) {
      onUpload(file);
    }
  }, [onUpload]);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    const file = e.dataTransfer.files[0];
    if (file) {
      handleFile(file);
    }
  }, [handleFile]);

  const handleFileInput = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      handleFile(file);
    }
  }, [handleFile]);

  if (uploadedFile) {
    return (
      <Card className="border-2 border-primary/20 bg-gradient-to-br from-primary/5 to-secondary/5 backdrop-blur-sm">
        <CardContent className="p-6">
          <div className="flex items-center gap-4">
            <div className="rounded-lg bg-primary/10 p-3">
              <FileText className="h-8 w-8 text-primary" />
            </div>
            <div className="flex-1">
              <p className="font-semibold text-foreground">{uploadedFile.name}</p>
              <p className="text-sm text-black">
                {(uploadedFile.size / 1024).toFixed(2)} KB
              </p>
            </div>
            <Button
              variant="ghost"
              size="icon"
              onClick={() => window.location.reload()}
              className="text-black hover:text-foreground"
            >
              <X className="h-5 w-5" />
            </Button>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card
      className={cn(
        'border-2 border-dashed transition-all duration-300',
        isDragging
          ? 'border-primary bg-primary/5 scale-[1.02]'
          : 'border-muted-foreground/25 hover:border-primary/50 hover:bg-primary/5',
        isLoading && 'opacity-50 pointer-events-none'
      )}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
    >
      <CardContent className="p-12">
        <div className="flex flex-col items-center justify-center space-y-4 text-center">
          <div className="rounded-full bg-primary/10 p-6">
            <Upload className={cn(
              'h-12 w-12 text-primary transition-transform duration-300',
              isDragging && 'scale-110'
            )} />
          </div>
          
          <div className="space-y-2">
            <h3 className="text-xl  text-black font-semibold">
              {isDragging ? 'Drop your document here' : 'Upload Legal Document'}
            </h3>
            <p className="text-sm text-black  max-w-md">
              Drag and drop your .docx file here, or click to browse
            </p>
          </div>

          <div className="flex items-center gap-4">
            <Button
              variant="default"
              onClick={() => document.getElementById('file-input')?.click()}
              disabled={isLoading}
              className="px-6 text-white"
              style={{ color: '#ffffff' }}
            >
              {isLoading ? 'Uploading...' : 'Select File'}
            </Button>
            <input
              id="file-input"
              type="file"
              accept=".docx,.doc"
              onChange={handleFileInput}
              className="hidden"
              disabled={isLoading}
            />
          </div>

          <p className="text-xs text-black">
            Supported formats: .docx (Max 10MB)
          </p>

          {error && (
            <div className="mt-4 rounded-md bg-destructive/10 border border-destructive/20 p-3 w-full max-w-md">
              <p className="text-sm text-destructive">{error}</p>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}


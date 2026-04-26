import React, { useState, useRef } from 'react';
import { useTranslation } from 'react-i18next';
import { Upload, FileText, X } from 'lucide-react';

interface InputSectionProps {
  onSubmit: (file: File, desiredRole: string) => void;
  loading: boolean;
}

export default function InputSection({ onSubmit, loading }: InputSectionProps) {
  const { t } = useTranslation();
  const [file, setFile] = useState<File | null>(null);
  const [desiredRole, setDesiredRole] = useState('');
  const [dragActive, setDragActive] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (file && desiredRole.trim()) {
      onSubmit(file, desiredRole.trim());
    }
  };

  const isValid = file && desiredRole.trim().length > 0;

  return (
    <form onSubmit={handleSubmit} className="max-w-xl mx-auto">
      <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 md:p-8">
        <div className="mb-6">
          <label className="block text-sm font-semibold text-slate-700 mb-2">
            {t('input.uploadLabel')}
          </label>
          <div
            onClick={() => inputRef.current?.click()}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
            className={`relative border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-colors ${
              dragActive
                ? 'border-slate-900 bg-slate-50'
                : 'border-slate-300 hover:border-slate-400'
            }`}
          >
            <input
              ref={inputRef}
              type="file"
              accept=".pdf,.docx"
              onChange={handleFileChange}
              className="hidden"
            />
            {file ? (
              <div className="flex items-center justify-center gap-3">
                <FileText className="w-6 h-6 text-slate-700" />
                <span className="text-slate-700 font-medium">{file.name}</span>
                <button
                  type="button"
                  onClick={(e) => {
                    e.stopPropagation();
                    setFile(null);
                  }}
                  className="p-1 hover:bg-slate-200 rounded-full transition-colors"
                >
                  <X className="w-4 h-4 text-slate-500" />
                </button>
              </div>
            ) : (
              <div className="flex flex-col items-center gap-2">
                <Upload className="w-8 h-8 text-slate-400" />
                <span className="text-slate-500">{t('input.uploadPlaceholder')}</span>
                <span className="text-xs text-slate-400">PDF, DOCX</span>
              </div>
            )}
          </div>
        </div>

        <div className="mb-6">
          <label htmlFor="role" className="block text-sm font-semibold text-slate-700 mb-2">
            {t('input.roleLabel')}
          </label>
          <input
            id="role"
            type="text"
            value={desiredRole}
            onChange={(e) => setDesiredRole(e.target.value)}
            placeholder={t('input.rolePlaceholder')}
            className="w-full px-4 py-3 rounded-xl border border-slate-300 focus:border-slate-900 focus:ring-1 focus:ring-slate-900 outline-none transition-colors bg-white"
          />
        </div>

        <button
          type="submit"
          disabled={!isValid || loading}
          className={`w-full py-3 rounded-xl font-semibold text-white transition-colors ${
            isValid && !loading
              ? 'bg-slate-900 hover:bg-slate-800'
              : 'bg-slate-300 cursor-not-allowed'
          }`}
        >
          {loading ? t('input.submitting') : t('input.submit')}
        </button>
      </div>
    </form>
  );
}


import { useTranslation } from 'react-i18next';
import { Globe } from 'lucide-react';

interface HeaderProps {
  onLanguageSwitch: () => void;
}

export default function Header({ onLanguageSwitch }: HeaderProps) {
  const { t } = useTranslation();

  return (
    <header className="w-full bg-white border-b border-slate-200">
      <div className="max-w-5xl mx-auto px-4 h-16 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-slate-900 rounded-lg flex items-center justify-center">
            <span className="text-white font-bold text-sm">D</span>
          </div>
          <span className="font-bold text-slate-900 text-lg">Dhalee</span>
        </div>

        <button
          onClick={onLanguageSwitch}
          className="flex items-center gap-2 px-3 py-1.5 text-sm font-medium text-slate-700 bg-slate-100 rounded-lg hover:bg-slate-200 transition-colors"
        >
          <Globe className="w-4 h-4" />
          {t('language.switch')}
        </button>
      </div>
    </header>
  );
}

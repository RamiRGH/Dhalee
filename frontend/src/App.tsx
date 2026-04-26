import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import Header from './components/Header';
import InputSection from './components/InputSection';
import ProgressTracker from './components/ProgressTracker';
import RoadmapView from './components/RoadmapView';
import ReadinessReport from './components/ReadinessReport';

export type AnalysisResult = {
  extracted_skills: string[];
  skill_gaps: string[];
  market_requirements: string[];
  curated_resources: any[];
  learning_roadmap: any;
  coach_feedback: string;
  readiness_report: any;
};

export default function App() {
  const { t, i18n } = useTranslation();
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [progress, setProgress] = useState<{ agent: string; message: string }[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'roadmap' | 'report'>('roadmap');

  const changeLanguage = () => {
    const next = i18n.language === 'ar' ? 'en' : 'ar';
    i18n.changeLanguage(next);
    document.documentElement.dir = next === 'ar' ? 'rtl' : 'ltr';
    document.documentElement.lang = next;
  };

  const handleAnalyze = async (file: File, desiredRole: string) => {
    setLoading(true);
    setError(null);
    setResult(null);
    setProgress([]);

    const formData = new FormData();
    formData.append('cv_file', file);
    formData.append('desired_role', desiredRole);

    try {
      const response = await fetch('/api/analyze', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errText = await response.text();
        let message = errText;
        try {
          const parsed = JSON.parse(errText);
          message = parsed.detail || errText;
        } catch {}
        throw new Error(message);
      }

      const reader = response.body?.getReader();
      if (!reader) throw new Error('No response body');

      const decoder = new TextDecoder();
      let done = false;

      while (!done) {
        const { value, done: streamDone } = await reader.read();
        done = streamDone;
        if (!value) continue;

        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split('\n').filter((l) => l.trim());

        for (const line of lines) {
          try {
            const event = JSON.parse(line);
            if (event.type === 'progress') {
              setProgress((prev) => [...prev, { agent: event.agent, message: event.message }]);
            } else if (event.type === 'complete') {
              setResult(event.data);
            } else if (event.type === 'error') {
              throw new Error(event.message);
            }
          } catch (e) {
            // ignore malformed lines
          }
        }
      }
    } catch (err: any) {
      setError(err.message || t('results.error'));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50">
      <Header onLanguageSwitch={changeLanguage} />

      <main className="max-w-5xl mx-auto px-4 py-8">
        {!result && !loading && (
          <div className="text-center mb-10">
            <h1 className="text-4xl md:text-5xl font-extrabold text-slate-900 mb-4">
              {t('app.title')}
            </h1>
            <p className="text-xl text-slate-600 mb-2">{t('app.subtitle')}</p>
            <p className="text-slate-500">{t('app.tagline')}</p>
          </div>
        )}

        {!result && <InputSection onSubmit={handleAnalyze} loading={loading} />}

        {loading && <ProgressTracker steps={progress} />}

        {error && (
          <div className="mt-8 p-4 bg-red-50 border border-red-200 rounded-xl text-red-700 text-center">
            {error}
          </div>
        )}

        {result && (
          <div className="mt-8">
            <h2 className="text-3xl font-bold text-slate-900 mb-6 text-center">
              {t('results.title')}
            </h2>

            <div className="flex justify-center mb-8">
              <div className="inline-flex bg-white rounded-xl shadow-sm border border-slate-200 p-1">
                <button
                  onClick={() => setActiveTab('roadmap')}
                  className={`px-6 py-2 rounded-lg text-sm font-medium transition-colors ${
                    activeTab === 'roadmap'
                      ? 'bg-slate-900 text-white'
                      : 'text-slate-600 hover:bg-slate-100'
                  }`}
                >
                  {t('results.roadmapTab')}
                </button>
                <button
                  onClick={() => setActiveTab('report')}
                  className={`px-6 py-2 rounded-lg text-sm font-medium transition-colors ${
                    activeTab === 'report'
                      ? 'bg-slate-900 text-white'
                      : 'text-slate-600 hover:bg-slate-100'
                  }`}
                >
                  {t('results.reportTab')}
                </button>
              </div>
            </div>

            {activeTab === 'roadmap' && <RoadmapView roadmap={result.learning_roadmap} />}
            {activeTab === 'report' && <ReadinessReport report={result.readiness_report} />}

            <div className="mt-10 text-center">
              <button
                onClick={() => {
                  setResult(null);
                  setProgress([]);
                  setError(null);
                }}
                className="px-6 py-3 bg-slate-900 text-white rounded-xl font-medium hover:bg-slate-800 transition-colors"
              >
                {t('input.startOver')}
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

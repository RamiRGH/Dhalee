import { useTranslation } from 'react-i18next';
import { Loader2, CheckCircle2 } from 'lucide-react';

interface ProgressTrackerProps {
  steps: { agent: string; message: string }[];
}

const agentOrder = [
  'start',
  'skill_auditor',
  'market_scout',
  'content_curator',
  'roadmap_architect',
  'performance_coach',
  'talent_advocate',
];

export default function ProgressTracker({ steps }: ProgressTrackerProps) {
  const { t } = useTranslation();

  const lastAgent = steps.length > 0 ? steps[steps.length - 1].agent : '';

  return (
    <div className="max-w-xl mx-auto mt-8">
      <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 md:p-8">
        <h3 className="text-lg font-semibold text-slate-900 mb-6 text-center">
          {t('progress.title')}
        </h3>

        <div className="space-y-4">
          {agentOrder.map((agent) => {
            const isCompleted = steps.some((s) => s.agent === agent);
            const isActive = lastAgent === agent;

            return (
              <div key={agent} className="flex items-center gap-4">
                <div className="flex-shrink-0">
                  {isCompleted && !isActive ? (
                    <CheckCircle2 className="w-6 h-6 text-emerald-600" />
                  ) : isActive ? (
                    <Loader2 className="w-6 h-6 text-slate-900 animate-spin" />
                  ) : (
                    <div className="w-6 h-6 rounded-full border-2 border-slate-200" />
                  )}
                </div>
                <div className="flex-1">
                  <p
                    className={`text-sm font-medium ${
                      isActive
                        ? 'text-slate-900'
                        : isCompleted
                        ? 'text-slate-700'
                        : 'text-slate-400'
                    }`}
                  >
                    {t(`progress.${agent}`)}
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

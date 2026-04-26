import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { ChevronDown, ChevronUp, BookOpen } from 'lucide-react';

interface RoadmapViewProps {
  roadmap: any;
}

export default function RoadmapView({ roadmap }: RoadmapViewProps) {
  const { t } = useTranslation();
  const weeks = roadmap?.weeks || [];
  const [openWeek, setOpenWeek] = useState<number | null>(0);

  if (weeks.length === 0) {
    return (
      <div className="text-center text-slate-500 py-12">
        No roadmap data available.
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {weeks.map((week: any, idx: number) => {
        const isOpen = openWeek === idx;
        return (
          <div
            key={idx}
            className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden"
          >
            <button
              onClick={() => setOpenWeek(isOpen ? null : idx)}
              className="w-full flex items-center justify-between px-6 py-4 hover:bg-slate-50 transition-colors"
            >
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 bg-slate-900 text-white rounded-lg flex items-center justify-center text-sm font-bold">
                  {week.week_number || idx + 1}
                </div>
                <span className="font-semibold text-slate-900">
                  {t('results.week')} {week.week_number || idx + 1}
                </span>
              </div>
              {isOpen ? (
                <ChevronUp className="w-5 h-5 text-slate-500" />
              ) : (
                <ChevronDown className="w-5 h-5 text-slate-500" />
              )}
            </button>

            {isOpen && (
              <div className="px-6 pb-6 border-t border-slate-100">
                <div className="mt-4">
                  <h4 className="text-sm font-semibold text-slate-700 mb-2">
                    {t('results.skills')}
                  </h4>
                  <div className="flex flex-wrap gap-2">
                    {(week.focus_skills || []).map((skill: string, sidx: number) => (
                      <span
                        key={sidx}
                        className="px-3 py-1 bg-slate-100 text-slate-700 rounded-full text-xs font-medium"
                      >
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>

                <div className="mt-4">
                  <h4 className="text-sm font-semibold text-slate-700 mb-2">
                    {t('results.objectives')}
                  </h4>
                  <ul className="list-disc list-inside space-y-1">
                    {(week.objectives || []).map((obj: string, oidx: number) => (
                      <li key={oidx} className="text-sm text-slate-600">
                        {obj}
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="mt-4">
                  <h4 className="text-sm font-semibold text-slate-700 mb-2">
                    {t('results.resources')}
                  </h4>
                  <div className="space-y-2">
                    {(week.resources_to_use || []).map((res: any, ridx: number) => (
                      <a
                        key={ridx}
                        href={res.url || '#'}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center gap-2 p-3 bg-slate-50 rounded-lg hover:bg-slate-100 transition-colors group"
                      >
                        <BookOpen className="w-4 h-4 text-slate-400 group-hover:text-slate-600" />
                        <span className="text-sm text-slate-700 group-hover:text-slate-900">
                          {res.title || 'Resource'}
                        </span>
                      </a>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}

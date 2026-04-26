import { useTranslation } from 'react-i18next';
import { Star, TrendingUp, AlertCircle, MessageSquare } from 'lucide-react';

interface ReadinessReportProps {
  report: any;
}

export default function ReadinessReport({ report }: ReadinessReportProps) {
  const { t } = useTranslation();

  if (!report || Object.keys(report).length === 0) {
    return (
      <div className="text-center text-slate-500 py-12">
        No readiness report available.
      </div>
    );
  }

  const score = report.skill_alignment_score || 0;

  return (
    <div className="space-y-6">
      {/* Score Card */}
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
        <div className="flex items-center gap-3 mb-4">
          <Star className="w-5 h-5 text-amber-500" />
          <h3 className="text-lg font-semibold text-slate-900">
            {t('results.skillAlignment')}
          </h3>
        </div>
        <div className="flex items-center gap-4">
          <div className="w-20 h-20 rounded-full border-4 border-slate-900 flex items-center justify-center">
            <span className="text-2xl font-bold text-slate-900">{score}</span>
          </div>
          <div className="flex-1">
            <div className="w-full h-3 bg-slate-100 rounded-full overflow-hidden">
              <div
                className="h-full bg-slate-900 rounded-full transition-all"
                style={{ width: `${Math.min(score, 100)}%` }}
              />
            </div>
          </div>
        </div>
      </div>

      {/* Executive Summary */}
      {report.executive_summary && (
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
          <div className="flex items-center gap-3 mb-3">
            <MessageSquare className="w-5 h-5 text-slate-700" />
            <h3 className="text-lg font-semibold text-slate-900">
              {t('results.executiveSummary')}
            </h3>
          </div>
          <p className="text-slate-600 leading-relaxed">{report.executive_summary}</p>
        </div>
      )}

      {/* Strengths & Gaps */}
      <div className="grid md:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
          <div className="flex items-center gap-3 mb-4">
            <TrendingUp className="w-5 h-5 text-emerald-600" />
            <h3 className="text-lg font-semibold text-slate-900">
              {t('results.keyStrengths')}
            </h3>
          </div>
          <ul className="space-y-2">
            {(report.key_strengths || []).map((s: string, idx: number) => (
              <li key={idx} className="flex items-start gap-2 text-sm text-slate-600">
                <span className="w-1.5 h-1.5 bg-emerald-500 rounded-full mt-1.5 flex-shrink-0" />
                {s}
              </li>
            ))}
          </ul>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
          <div className="flex items-center gap-3 mb-4">
            <AlertCircle className="w-5 h-5 text-rose-600" />
            <h3 className="text-lg font-semibold text-slate-900">
              {t('results.remainingGaps')}
            </h3>
          </div>
          <ul className="space-y-2">
            {(report.remaining_gaps || []).map((g: string, idx: number) => (
              <li key={idx} className="flex items-start gap-2 text-sm text-slate-600">
                <span className="w-1.5 h-1.5 bg-rose-500 rounded-full mt-1.5 flex-shrink-0" />
                {g}
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Recruiter Pitch */}
      {report.recruiter_pitch && (
        <div className="bg-slate-900 rounded-xl shadow-sm p-6 text-white">
          <h3 className="text-lg font-semibold mb-3">{t('results.recruiterPitch')}</h3>
          <p className="text-slate-300 leading-relaxed">{report.recruiter_pitch}</p>
        </div>
      )}
    </div>
  );
}

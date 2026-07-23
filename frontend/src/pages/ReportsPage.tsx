import React, { useEffect, useState } from 'react';
import { FileText, Download, ShieldCheck, Award, Building2, Cpu } from 'lucide-react';
import { api } from '../api/client';
import { ConsortiumReport } from '../types';

export const ReportsPage: React.FC = () => {
  const [report, setReport] = useState<ConsortiumReport | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchReport = async () => {
      setLoading(true);
      try {
        const data = await api.getConsortiumReport();
        setReport(data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchReport();
  }, []);

  const handleExportCSV = () => {
    if (!report) return;
    const csvContent =
      'data:text/csv;charset=utf-8,' +
      'Version,Accuracy,Loss,F1 Score\n' +
      report.global_model_lineage
        .map((m) => `${m.version},${m.accuracy},${m.loss},${m.f1_score}`)
        .join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', 'consortium_report_summary.csv');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between glass-card p-6 rounded-2xl border-cyan-500/30">
        <div>
          <h1 className="text-2xl font-extrabold text-white">Consortium Analytics & Reports</h1>
          <p className="text-xs text-slate-400 mt-1">
            Executive Performance Summary, Differential Privacy Accounting & Model Lineage
          </p>
        </div>
        <button
          onClick={handleExportCSV}
          className="px-5 py-2.5 bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-400 hover:to-teal-500 text-white font-bold text-xs rounded-xl shadow-lg shadow-emerald-500/25 flex items-center space-x-2 transition"
        >
          <Download className="w-4 h-4" />
          <span>Export Consortium CSV</span>
        </button>
      </div>

      {/* Report Summary Card */}
      {report && (
        <div className="glass-card p-8 rounded-2xl space-y-6">
          <div className="border-b border-[#1e2d54] pb-6 flex items-center justify-between">
            <div>
              <span className="text-xs font-bold uppercase tracking-wider text-cyan-400">Official Consortium Audit Document</span>
              <h2 className="text-xl font-extrabold text-white mt-1">{report.title}</h2>
              <p className="text-xs text-slate-400 mt-0.5">Generated: {new Date(report.generated_at).toLocaleString()}</p>
            </div>
            <div className="p-3 bg-cyan-500/10 text-cyan-400 rounded-2xl border border-cyan-500/20">
              <FileText className="w-8 h-8" />
            </div>
          </div>

          {/* Key Metric Highlights */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
              <p className="text-xs text-slate-400 uppercase font-semibold">Participating Hospital Consortium</p>
              <p className="text-xl font-extrabold text-white mt-1">{report.total_participating_hospitals} Hospital Edge Nodes</p>
            </div>
            <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
              <p className="text-xs text-slate-400 uppercase font-semibold">Executed Training Rounds</p>
              <p className="text-xl font-extrabold text-cyan-400 mt-1">{report.total_rounds_executed} Aggregation Rounds</p>
            </div>
            <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
              <p className="text-xs text-slate-400 uppercase font-semibold">Peak Model Diagnostic Accuracy</p>
              <p className="text-xl font-extrabold text-emerald-400 mt-1">{(report.best_global_accuracy * 100).toFixed(1)}%</p>
            </div>
          </div>

          {/* Differential Privacy Guarantee Box */}
          <div className="p-5 bg-indigo-500/10 rounded-2xl border border-indigo-500/20 space-y-2">
            <div className="flex items-center space-x-2 text-sm font-bold text-indigo-400">
              <ShieldCheck className="w-5 h-5" />
              <span>Differential Privacy Compliance Guarantee</span>
            </div>
            <p className="text-xs text-slate-300 leading-relaxed">
              {report.differential_privacy_summary.guarantee}.
              Clip Norm $C = {report.differential_privacy_summary.clip_norm}$, Noise Multiplier $\sigma = {report.differential_privacy_summary.noise_multiplier}$, $\delta = {report.differential_privacy_summary.delta}$.
              Patient EHR data zero-exposure verification certified.
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

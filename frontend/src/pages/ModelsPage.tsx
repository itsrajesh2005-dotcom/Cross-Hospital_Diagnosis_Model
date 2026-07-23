import React, { useEffect, useState } from 'react';
import { Boxes, Download, Award, ShieldCheck, HardDrive } from 'lucide-react';
import { api } from '../api/client';
import { GlobalModel } from '../types';

export const ModelsPage: React.FC = () => {
  const [models, setModels] = useState<GlobalModel[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchModels = async () => {
      setLoading(true);
      try {
        const data = await api.getGlobalModels();
        setModels(data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchModels();
  }, []);

  const handleDownload = (modelId: string, version: str) => {
    window.open(`/api/v1/models/${modelId}/download`, '_blank');
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between glass-card p-6 rounded-2xl border-cyan-500/30">
        <div>
          <h1 className="text-2xl font-extrabold text-white">Global Model Registry</h1>
          <p className="text-xs text-slate-400 mt-1">
            Aggregated PyTorch Weights (.pt), Semantic Versioning & Diagnostic Lineage
          </p>
        </div>
      </div>

      <div className="glass-card rounded-2xl overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="bg-[#111c38]/80 text-xs font-semibold text-slate-400 uppercase border-b border-[#1e2d54]">
              <tr>
                <th className="px-6 py-4">Version & Artifact</th>
                <th className="px-6 py-4">Accuracy %</th>
                <th className="px-6 py-4">F1 Score</th>
                <th className="px-6 py-4">S3 Object Path</th>
                <th className="px-6 py-4">Created Timestamp</th>
                <th className="px-6 py-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#1e2d54]">
              {models.map((m) => (
                <tr key={m.id} className="hover:bg-slate-800/40 transition">
                  <td className="px-6 py-4">
                    <div className="flex items-center space-x-3">
                      <div className="p-2.5 bg-indigo-500/10 text-indigo-400 rounded-xl border border-indigo-500/20">
                        <Boxes className="w-5 h-5" />
                      </div>
                      <div>
                        <p className="font-mono font-bold text-cyan-400 text-sm">{m.version}</p>
                        <p className="text-[10px] text-slate-400">Diagnostic PyTorch Classifier</p>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <span className="font-extrabold text-emerald-400 text-sm">
                      {(m.accuracy * 100).toFixed(1)}%
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <span className="font-semibold text-slate-200 text-xs">
                      {m.f1_score.toFixed(4)}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center space-x-1.5 text-xs text-slate-400 font-mono">
                      <HardDrive className="w-3.5 h-3.5 text-slate-500" />
                      <span className="truncate max-w-[200px]">{m.s3_storage_path}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-xs text-slate-400">
                    {new Date(m.created_at).toLocaleString()}
                  </td>
                  <td className="px-6 py-4 text-right">
                    <button
                      onClick={() => handleDownload(m.id, m.version)}
                      className="px-4 py-2 bg-slate-800 hover:bg-cyan-500/20 text-cyan-400 hover:text-cyan-300 font-bold text-xs rounded-xl border border-slate-700 hover:border-cyan-500/30 flex items-center space-x-1.5 ml-auto transition"
                    >
                      <Download className="w-3.5 h-3.5" />
                      <span>Download Weights</span>
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

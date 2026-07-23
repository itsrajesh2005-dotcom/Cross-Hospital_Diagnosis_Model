import React, { useState } from 'react';
import { Play, X, Sliders, ShieldCheck } from 'lucide-react';

interface RoundControlModalProps {
  isOpen: boolean;
  onClose: () => void;
  onStart: (minClients: number, targetAccuracy: number) => Promise<void>;
}

export const RoundControlModal: React.FC<RoundControlModalProps> = ({
  isOpen,
  onClose,
  onStart,
}) => {
  const [minClients, setMinClients] = useState(2);
  const [targetAccuracy, setTargetAccuracy] = useState(0.95);
  const [loading, setLoading] = useState(false);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await onStart(minClients, targetAccuracy);
      onClose();
    } catch (err) {
      console.error('Failed to start round:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
      <div className="bg-[#111c38] border border-[#1e2d54] rounded-2xl w-full max-w-lg overflow-hidden shadow-2xl animate-in fade-in zoom-in-95 duration-200">
        <div className="p-6 border-b border-[#1e2d54] flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-cyan-500/10 text-cyan-400 rounded-xl border border-cyan-500/20">
              <Play className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-white">Trigger Federated Training Round</h2>
              <p className="text-xs text-slate-400">Initiate FedAvg aggregation cycle across hospital nodes</p>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white p-1 rounded-lg">
            <X className="w-5 h-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-5">
          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
              Minimum Required Hospital Clients
            </label>
            <div className="flex items-center space-x-4">
              <input
                type="range"
                min="1"
                max="10"
                value={minClients}
                onChange={(e) => setMinClients(Number(e.target.value))}
                className="w-full accent-cyan-400 bg-slate-800 rounded-lg cursor-pointer"
              />
              <span className="px-3 py-1 bg-slate-800 text-cyan-400 font-bold rounded-lg border border-slate-700">
                {minClients} Nodes
              </span>
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
              Consortium Target Accuracy (%)
            </label>
            <div className="flex items-center space-x-4">
              <input
                type="range"
                min="80"
                max="99"
                value={Math.round(targetAccuracy * 100)}
                onChange={(e) => setTargetAccuracy(Number(e.target.value) / 100)}
                className="w-full accent-emerald-400 bg-slate-800 rounded-lg cursor-pointer"
              />
              <span className="px-3 py-1 bg-slate-800 text-emerald-400 font-bold rounded-lg border border-slate-700">
                {Math.round(targetAccuracy * 100)}%
              </span>
            </div>
          </div>

          <div className="p-4 bg-slate-900/60 rounded-xl border border-slate-800 space-y-2">
            <div className="flex items-center space-x-2 text-xs font-semibold text-cyan-400">
              <ShieldCheck className="w-4 h-4" />
              <span>Security & DP Enforcements</span>
            </div>
            <p className="text-[11px] text-slate-400 leading-relaxed">
              Hospital patient datasets remain strictly local. Participating nodes receive global weights, train for local DP-SGD epochs ($\ell_2$-norm clip $C=1.0$), and transmit encrypted parameter updates.
            </p>
          </div>

          <div className="flex justify-end space-x-3 pt-2">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2.5 rounded-xl text-sm font-medium text-slate-400 hover:bg-slate-800"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="px-5 py-2.5 rounded-xl text-sm font-bold text-white bg-gradient-to-r from-cyan-500 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 shadow-lg shadow-cyan-500/25 transition disabled:opacity-50"
            >
              {loading ? 'Initiating Round...' : 'Launch Training Round'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

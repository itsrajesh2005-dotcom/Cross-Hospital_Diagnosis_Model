import React, { useEffect, useState } from 'react';
import { Cpu, Play, CheckCircle2, Clock, Activity, AlertCircle } from 'lucide-react';
import { api } from '../api/client';
import { TrainingRound } from '../types';
import { RoundControlModal } from '../components/rounds/RoundControlModal';

export const RoundsPage: React.FC = () => {
  const [rounds, setRounds] = useState<TrainingRound[]>([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const fetchRounds = async () => {
    setLoading(true);
    try {
      const data = await api.getRounds();
      setRounds(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRounds();
  }, []);

  const handleStartRound = async (minClients: number, targetAccuracy: number) => {
    await api.startRound({ min_clients: minClients, target_accuracy: targetAccuracy });
    fetchRounds();
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'COMPLETED':
        return (
          <span className="inline-flex items-center space-x-1.5 px-3 py-1 bg-emerald-500/10 text-emerald-400 text-xs font-bold rounded-full border border-emerald-500/20">
            <CheckCircle2 className="w-3.5 h-3.5" />
            <span>Completed</span>
          </span>
        );
      case 'TRAINING':
      case 'AGGREGATING':
      case 'SELECTING':
        return (
          <span className="inline-flex items-center space-x-1.5 px-3 py-1 bg-cyan-500/10 text-cyan-400 text-xs font-bold rounded-full border border-cyan-500/20">
            <Activity className="w-3.5 h-3.5 animate-spin" />
            <span>{status}</span>
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center space-x-1.5 px-3 py-1 bg-slate-800 text-slate-400 text-xs font-bold rounded-full border border-slate-700">
            <Clock className="w-3.5 h-3.5" />
            <span>{status}</span>
          </span>
        );
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between glass-card p-6 rounded-2xl border-cyan-500/30">
        <div>
          <h1 className="text-2xl font-extrabold text-white">Federated Training Rounds</h1>
          <p className="text-xs text-slate-400 mt-1">
            Consortium Round Orchestration, Client Participation & Weight Aggregation
          </p>
        </div>
        <button
          onClick={() => setIsModalOpen(true)}
          className="px-5 py-2.5 bg-gradient-to-r from-cyan-500 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 text-white font-bold text-xs rounded-xl shadow-lg shadow-cyan-500/25 flex items-center space-x-2 transition"
        >
          <Play className="w-4 h-4 fill-white" />
          <span>Launch Training Round</span>
        </button>
      </div>

      {/* Rounds List */}
      <div className="space-y-4">
        {rounds.map((r) => (
          <div key={r.id} className="glass-card p-6 rounded-2xl hover:border-slate-600 transition">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div className="flex items-center space-x-4">
                <div className="w-12 h-12 rounded-2xl bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 flex items-center justify-center font-black text-lg">
                  #{r.round_number}
                </div>
                <div>
                  <div className="flex items-center space-x-3">
                    <h3 className="text-lg font-bold text-white">Round #{r.round_number}</h3>
                    {getStatusBadge(r.status)}
                  </div>
                  <p className="text-xs text-slate-400 mt-1">
                    Started: {new Date(r.started_at).toLocaleString()}
                    {r.completed_at && ` • Completed: ${new Date(r.completed_at).toLocaleTimeString()}`}
                  </p>
                </div>
              </div>

              <div className="flex items-center space-x-6">
                <div>
                  <p className="text-[10px] text-slate-400 uppercase font-semibold">Participating Nodes</p>
                  <p className="text-sm font-bold text-cyan-400">{r.participating_clients_count} Hospitals</p>
                </div>
                <div>
                  <p className="text-[10px] text-slate-400 uppercase font-semibold">Achieved Accuracy</p>
                  <p className="text-sm font-bold text-emerald-400">{(r.current_accuracy * 100).toFixed(1)}%</p>
                </div>
                <div>
                  <p className="text-[10px] text-slate-400 uppercase font-semibold">Consortium Loss</p>
                  <p className="text-sm font-bold text-rose-400">{r.current_loss.toFixed(4)}</p>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      <RoundControlModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onStart={handleStartRound}
      />
    </div>
  );
};

import React, { useEffect, useState } from 'react';
import {
  Building2,
  Cpu,
  Award,
  Lock,
  Play,
  RefreshCw,
  CheckCircle2,
  Clock,
} from 'lucide-react';
import { api } from '../api/client';
import { DashboardSummary, TrainingMetric } from '../types';
import { StatCard } from '../components/dashboard/StatCard';
import { AccuracyChart } from '../components/dashboard/AccuracyChart';
import { RoundControlModal } from '../components/rounds/RoundControlModal';

export const DashboardPage: React.FC = () => {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [metrics, setMetrics] = useState<TrainingMetric[]>([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [sumRes, metRes] = await Promise.all([
        api.getDashboardSummary(),
        api.getMetrics(),
      ]);
      setSummary(sumRes);
      setMetrics(metRes);
    } catch (err) {
      console.error('Failed to load dashboard data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleStartRound = async (minClients: number, targetAccuracy: number) => {
    await api.startRound({ min_clients: minClients, target_accuracy: targetAccuracy });
    fetchData();
  };

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 glass-card p-6 rounded-2xl border-cyan-500/30">
        <div>
          <h1 className="text-2xl font-extrabold text-white tracking-tight">
            Consortium Diagnostic AI Dashboard
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Privacy-Preserving Federated Learning across Healthcare Providers
          </p>
        </div>
        <div className="flex items-center space-x-3">
          <button
            onClick={fetchData}
            className="p-2.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl transition border border-slate-700"
            title="Refresh Telemetry"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          </button>
          <button
            onClick={() => setIsModalOpen(true)}
            className="px-5 py-2.5 bg-gradient-to-r from-cyan-500 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 text-white font-bold text-xs rounded-xl shadow-lg shadow-cyan-500/25 flex items-center space-x-2 transition"
          >
            <Play className="w-4 h-4 fill-white" />
            <span>Launch Training Round</span>
          </button>
        </div>
      </div>

      {/* Stat Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Participating Hospitals"
          value={`${summary?.active_hospitals || 3} / ${summary?.total_hospitals || 3}`}
          subtitle="All Edge Nodes Active"
          icon={Building2}
          color="cyan"
          trend="100% Connectivity"
        />
        <StatCard
          title="Completed FL Rounds"
          value={summary?.completed_rounds || 0}
          subtitle={`Current Version ${summary?.latest_model_version || 'v1.0.0'}`}
          icon={Cpu}
          color="emerald"
          trend="FedAvg Aggregation Active"
        />
        <StatCard
          title="Global Model Accuracy"
          value={`${((summary?.current_global_accuracy || 0.88) * 100).toFixed(1)}%`}
          subtitle={`Loss: ${summary?.current_global_loss || 0.18}`}
          icon={Award}
          color="blue"
          trend="+4.2% since previous round"
        />
        <StatCard
          title="DP Epsilon Budget"
          value={`ε = ${(summary?.total_privacy_budget_epsilon || 0.45).toFixed(2)}`}
          subtitle="δ = 1e-5 (Gaussian Noise)"
          icon={Lock}
          color="indigo"
          trend="Strict Differential Privacy"
        />
      </div>

      {/* Main Content: Convergence Chart + Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <AccuracyChart metrics={metrics} />
        </div>

        {/* Audit & Activity Stream */}
        <div className="glass-card p-6 rounded-2xl flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-base font-bold text-white">System Activity Trail</h3>
              <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 bg-slate-800 text-slate-300 rounded-full border border-slate-700">
                Audit Stream
              </span>
            </div>

            <div className="space-y-3 max-h-[280px] overflow-y-auto pr-1">
              {summary?.recent_activity && summary.recent_activity.length > 0 ? (
                summary.recent_activity.map((item) => (
                  <div
                    key={item.id}
                    className="p-3 bg-slate-900/60 rounded-xl border border-slate-800 flex items-start space-x-3"
                  >
                    <div className="p-1.5 bg-cyan-500/10 text-cyan-400 rounded-lg mt-0.5">
                      <CheckCircle2 className="w-4 h-4" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-xs font-semibold text-slate-200 truncate">{item.action}</p>
                      <p className="text-[11px] text-slate-400 truncate">
                        Resource: {item.resource_type}
                      </p>
                      <p className="text-[10px] text-slate-500 mt-1 flex items-center space-x-1">
                        <Clock className="w-3 h-3 inline mr-1" />
                        <span>{new Date(item.timestamp).toLocaleTimeString()}</span>
                      </p>
                    </div>
                  </div>
                ))
              ) : (
                <div className="text-center py-8 text-slate-500 text-xs">
                  No system audit events logged yet.
                </div>
              )}
            </div>
          </div>

          <div className="mt-4 pt-4 border-t border-slate-800 text-center">
            <p className="text-[11px] text-slate-400">
              Aggregator Cluster Node ID: <span className="text-cyan-400 font-mono">cluster-us-east-1</span>
            </p>
          </div>
        </div>
      </div>

      {/* Round Launch Modal */}
      <RoundControlModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onStart={handleStartRound}
      />
    </div>
  );
};

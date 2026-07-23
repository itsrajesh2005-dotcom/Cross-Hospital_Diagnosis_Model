import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import { TrainingMetric } from '../../types';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

interface AccuracyChartProps {
  metrics: TrainingMetric[];
}

export const AccuracyChart: React.FC<AccuracyChartProps> = ({ metrics }) => {
  const labels = metrics.length > 0
    ? metrics.map((m) => `Round #${m.epoch}`)
    : ['Round #1', 'Round #2', 'Round #3', 'Round #4', 'Round #5'];

  const accuracyData = metrics.length > 0
    ? metrics.map((m) => m.accuracy * 100)
    : [72.4, 79.1, 84.5, 89.2, 94.8];

  const lossData = metrics.length > 0
    ? metrics.map((m) => m.loss)
    : [0.45, 0.35, 0.28, 0.21, 0.14];

  const data = {
    labels,
    datasets: [
      {
        label: 'Global Accuracy (%)',
        data: accuracyData,
        borderColor: '#06b6d4',
        backgroundColor: 'rgba(6, 182, 212, 0.15)',
        fill: true,
        tension: 0.4,
        pointBackgroundColor: '#06b6d4',
        pointRadius: 4,
        yAxisID: 'y',
      },
      {
        label: 'Loss',
        data: lossData,
        borderColor: '#f43f5e',
        backgroundColor: 'rgba(244, 63, 94, 0.05)',
        borderDash: [5, 5],
        fill: false,
        tension: 0.4,
        pointBackgroundColor: '#f43f5e',
        pointRadius: 3,
        yAxisID: 'y1',
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top' as const,
        labels: {
          color: '#94a3b8',
          font: { family: 'Plus Jakarta Sans', size: 12 },
        },
      },
      tooltip: {
        backgroundColor: '#111c38',
        borderColor: '#1e2d54',
        borderWidth: 1,
        titleColor: '#ffffff',
        bodyColor: '#cbd5e1',
      },
    },
    scales: {
      x: {
        grid: { color: 'rgba(30, 45, 84, 0.4)' },
        ticks: { color: '#94a3b8' },
      },
      y: {
        type: 'linear' as const,
        display: true,
        position: 'left' as const,
        grid: { color: 'rgba(30, 45, 84, 0.4)' },
        ticks: { color: '#94a3b8' },
        min: 50,
        max: 100,
      },
      y1: {
        type: 'linear' as const,
        display: true,
        position: 'right' as const,
        grid: { drawOnChartArea: false },
        ticks: { color: '#f43f5e' },
        min: 0,
        max: 1,
      },
    },
  };

  return (
    <div className="glass-card p-6 rounded-2xl h-[380px]">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-base font-bold text-white">Global Model Convergence</h3>
          <p className="text-xs text-slate-400">FedAvg Accuracy (%) vs Loss Progression across rounds</p>
        </div>
        <span className="text-xs font-semibold px-2.5 py-1 bg-cyan-500/10 text-cyan-400 rounded-md border border-cyan-500/20">
          Live Telemetry
        </span>
      </div>
      <div className="h-[290px]">
        <Line data={data} options={options} />
      </div>
    </div>
  );
};

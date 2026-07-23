import React from 'react';
import { LucideIcon } from 'lucide-react';

interface StatCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: LucideIcon;
  trend?: string;
  color?: 'cyan' | 'emerald' | 'blue' | 'indigo';
}

export const StatCard: React.FC<StatCardProps> = ({
  title,
  value,
  subtitle,
  icon: Icon,
  trend,
  color = 'cyan',
}) => {
  const colorMap = {
    cyan: 'from-cyan-500/20 to-cyan-500/5 text-cyan-400 border-cyan-500/30',
    emerald: 'from-emerald-500/20 to-emerald-500/5 text-emerald-400 border-emerald-500/30',
    blue: 'from-blue-500/20 to-blue-500/5 text-blue-400 border-blue-500/30',
    indigo: 'from-indigo-500/20 to-indigo-500/5 text-indigo-400 border-indigo-500/30',
  };

  return (
    <div className="glass-card p-5 rounded-2xl relative overflow-hidden group hover:border-slate-600 transition-all duration-300">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">{title}</p>
          <h3 className="text-2xl font-extrabold text-white mt-1">{value}</h3>
          {subtitle && <p className="text-xs text-slate-400 mt-1">{subtitle}</p>}
        </div>
        <div className={`p-3 rounded-xl bg-gradient-to-br border ${colorMap[color]} shadow-lg`}>
          <Icon className="w-6 h-6" />
        </div>
      </div>
      {trend && (
        <div className="mt-3 flex items-center space-x-1.5 text-xs text-emerald-400 font-medium">
          <span>{trend}</span>
        </div>
      )}
    </div>
  );
};

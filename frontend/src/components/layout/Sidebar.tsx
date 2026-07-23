import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  Building2,
  Cpu,
  Boxes,
  ShieldAlert,
  FileText,
  Activity,
  HeartPulse,
} from 'lucide-react';

export const Sidebar: React.FC = () => {
  const navItems = [
    { label: 'Overview', icon: LayoutDashboard, path: '/' },
    { label: 'Hospitals', icon: Building2, path: '/hospitals' },
    { label: 'FL Rounds', icon: Cpu, path: '/rounds' },
    { label: 'Model Registry', icon: Boxes, path: '/models' },
    { label: 'Audit & Compliance', icon: ShieldAlert, path: '/audit' },
    { label: 'Consortium Reports', icon: FileText, path: '/reports' },
  ];

  return (
    <aside className="w-64 bg-[#0b1329] border-r border-[#1e2d54] flex flex-col justify-between h-screen sticky top-0 z-40">
      <div>
        {/* Brand Header */}
        <div className="h-16 px-6 flex items-center space-x-3 border-b border-[#1e2d54]">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-cyan-500/20">
            <HeartPulse className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="font-bold text-sm text-white tracking-tight leading-tight">Cross-Hospital</h1>
            <p className="text-[11px] text-cyan-400 font-semibold tracking-wider uppercase">Diagnosis Model</p>
          </div>
        </div>

        {/* Navigation Links */}
        <nav className="p-4 space-y-1.5">
          {navItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center space-x-3 px-4 py-3 rounded-xl text-sm font-medium transition-all ${
                  isActive
                    ? 'bg-gradient-to-r from-cyan-500/20 to-indigo-500/10 text-cyan-400 border border-cyan-500/30 shadow-md shadow-cyan-500/10'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
                }`
              }
            >
              <item.icon className="w-5 h-5" />
              <span>{item.label}</span>
            </NavLink>
          ))}
        </nav>
      </div>

      {/* Footer System Health Badge */}
      <div className="p-4 border-t border-[#1e2d54]">
        <div className="bg-[#111c38] p-3 rounded-xl border border-[#1e2d54] flex items-center space-x-3">
          <div className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-ping"></div>
          <div>
            <p className="text-xs font-semibold text-slate-200">Aggregator Cluster</p>
            <p className="text-[10px] text-emerald-400">100% Operational</p>
          </div>
        </div>
      </div>
    </aside>
  );
};

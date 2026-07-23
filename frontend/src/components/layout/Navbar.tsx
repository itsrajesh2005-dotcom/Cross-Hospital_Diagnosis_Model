import React from 'react';
import { ShieldCheck, Activity, Bell, User } from 'lucide-react';

export const Navbar: React.FC = () => {
  return (
    <header className="h-16 bg-[#111c38]/90 backdrop-blur-md border-b border-[#1e2d54] px-6 flex items-center justify-between sticky top-0 z-30">
      <div className="flex items-center space-x-4">
        <div className="flex items-center space-x-2 bg-emerald-500/10 text-emerald-400 px-3 py-1 rounded-full text-xs font-semibold border border-emerald-500/20">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          <span>HIPAA & GDPR Privacy Compliant</span>
        </div>
        <div className="hidden md:flex items-center space-x-2 text-xs text-slate-400 bg-slate-800/60 px-3 py-1 rounded-full border border-slate-700">
          <Activity className="w-3.5 h-3.5 text-cyan-400" />
          <span>Encryption: DP-SGD + TLS 1.3</span>
        </div>
      </div>

      <div className="flex items-center space-x-4">
        <button className="relative p-2 text-slate-300 hover:text-white rounded-lg hover:bg-slate-800 transition">
          <Bell className="w-5 h-5" />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-cyan-400 rounded-full"></span>
        </button>

        <div className="flex items-center space-x-3 border-l border-[#1e2d54] pl-4">
          <div className="w-9 h-9 rounded-full bg-gradient-to-tr from-cyan-500 to-indigo-600 flex items-center justify-center font-bold text-white shadow-lg">
            <User className="w-5 h-5" />
          </div>
          <div className="hidden lg:block text-left">
            <p className="text-xs font-semibold text-slate-200">Dr. Sarah Jenkins</p>
            <p className="text-[10px] text-slate-400 uppercase tracking-wider">Lead Consortium Auditor</p>
          </div>
        </div>
      </div>
    </header>
  );
};

import React, { useEffect, useState } from 'react';
import { ShieldAlert, Terminal, Clock, User, Filter } from 'lucide-react';
import { api } from '../api/client';
import { AuditLog } from '../types';

export const AuditPage: React.FC = () => {
  const [logs, setLogs] = useState<AuditLog[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAuditLogs = async () => {
      setLoading(true);
      try {
        const data = await api.getAuditLogs();
        setLogs(data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchAuditLogs();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between glass-card p-6 rounded-2xl border-cyan-500/30">
        <div>
          <h1 className="text-2xl font-extrabold text-white">Audit & Compliance Trail</h1>
          <p className="text-xs text-slate-400 mt-1">
            HIPAA Data Access Compliance, System Security Events & Model Training Audit Logs
          </p>
        </div>
      </div>

      <div className="glass-card rounded-2xl overflow-hidden">
        <div className="p-4 bg-[#111c38]/90 border-b border-[#1e2d54] flex items-center justify-between">
          <div className="flex items-center space-x-2 text-xs font-semibold text-slate-300">
            <Filter className="w-4 h-4 text-cyan-400" />
            <span>Filter Security Audit Events</span>
          </div>
          <span className="text-xs font-mono text-cyan-400">{logs.length} Log Entries</span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="bg-[#111c38]/80 text-xs font-semibold text-slate-400 uppercase border-b border-[#1e2d54]">
              <tr>
                <th className="px-6 py-4">Action Event</th>
                <th className="px-6 py-4">Resource Type</th>
                <th className="px-6 py-4">IP Address</th>
                <th className="px-6 py-4">Details JSON</th>
                <th className="px-6 py-4">Timestamp</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#1e2d54]">
              {logs.map((l) => (
                <tr key={l.id} className="hover:bg-slate-800/40 transition">
                  <td className="px-6 py-4">
                    <span className="font-mono font-bold text-xs px-2.5 py-1 bg-cyan-500/10 text-cyan-400 rounded-md border border-cyan-500/20">
                      {l.action}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-xs font-semibold text-slate-200">
                    {l.resource_type}
                  </td>
                  <td className="px-6 py-4 font-mono text-xs text-slate-400">
                    {l.ip_address}
                  </td>
                  <td className="px-6 py-4">
                    <code className="text-[11px] font-mono text-slate-400 bg-slate-900 px-2 py-1 rounded border border-slate-800 max-w-xs truncate block">
                      {JSON.stringify(l.details)}
                    </code>
                  </td>
                  <td className="px-6 py-4 text-xs text-slate-400 flex items-center space-x-1.5 mt-2">
                    <Clock className="w-3.5 h-3.5 text-slate-500" />
                    <span>{new Date(l.created_at).toLocaleString()}</span>
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

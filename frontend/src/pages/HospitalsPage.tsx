import React, { useEffect, useState } from 'react';
import { Building2, Plus, ShieldCheck, Activity, MapPin, Database, CheckCircle2 } from 'lucide-react';
import { api } from '../api/client';
import { Hospital } from '../types';

export const HospitalsPage: React.FC = () => {
  const [hospitals, setHospitals] = useState<Hospital[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [name, setName] = useState('');
  const [code, setCode] = useState('');
  const [sampleCount, setSampleCount] = useState(1200);

  const fetchHospitals = async () => {
    setLoading(true);
    try {
      const data = await api.getHospitals();
      setHospitals(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHospitals();
  }, []);

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.registerHospital({
        name,
        code,
        dataset_sample_count: sampleCount,
        location: 'Consortium Node',
      });
      setShowModal(false);
      setName('');
      setCode('');
      fetchHospitals();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between glass-card p-6 rounded-2xl border-cyan-500/30">
        <div>
          <h1 className="text-2xl font-extrabold text-white">Hospital Node Management</h1>
          <p className="text-xs text-slate-400 mt-1">
            Registered Edge Consortium Healthcare Nodes & Dataset Metadata
          </p>
        </div>
        <button
          onClick={() => setShowModal(true)}
          className="px-5 py-2.5 bg-gradient-to-r from-cyan-500 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 text-white font-bold text-xs rounded-xl shadow-lg shadow-cyan-500/25 flex items-center space-x-2 transition"
        >
          <Plus className="w-4 h-4" />
          <span>Register Hospital Node</span>
        </button>
      </div>

      {/* Hospitals Table */}
      <div className="glass-card rounded-2xl overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="bg-[#111c38]/80 text-xs font-semibold text-slate-400 uppercase border-b border-[#1e2d54]">
              <tr>
                <th className="px-6 py-4">Hospital Name & Code</th>
                <th className="px-6 py-4">Status & Heartbeat</th>
                <th className="px-6 py-4">On-Premise Dataset</th>
                <th className="px-6 py-4">Location</th>
                <th className="px-6 py-4">Verification</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#1e2d54]">
              {hospitals.map((h) => (
                <tr key={h.id} className="hover:bg-slate-800/40 transition">
                  <td className="px-6 py-4">
                    <div className="flex items-center space-x-3">
                      <div className="p-2.5 bg-cyan-500/10 text-cyan-400 rounded-xl border border-cyan-500/20">
                        <Building2 className="w-5 h-5" />
                      </div>
                      <div>
                        <p className="font-bold text-white text-sm">{h.name}</p>
                        <p className="text-xs font-mono text-cyan-400">{h.code}</p>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center space-x-2">
                      <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
                      <span className="text-xs font-bold text-emerald-400">{h.status}</span>
                    </div>
                    <p className="text-[11px] text-slate-400 mt-0.5">
                      Last active: {new Date(h.last_heartbeat).toLocaleTimeString()}
                    </p>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center space-x-2 text-slate-200 font-semibold text-xs">
                      <Database className="w-4 h-4 text-cyan-400" />
                      <span>{h.dataset_sample_count.toLocaleString()} Diagnostic Samples</span>
                    </div>
                    <p className="text-[10px] text-slate-400">Isolated Local Storage</p>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center space-x-1.5 text-xs text-slate-300">
                      <MapPin className="w-3.5 h-3.5 text-slate-400" />
                      <span>{h.location}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <span className="inline-flex items-center space-x-1.5 px-3 py-1 bg-emerald-500/10 text-emerald-400 text-xs font-bold rounded-full border border-emerald-500/20">
                      <CheckCircle2 className="w-3.5 h-3.5" />
                      <span>Verified Node</span>
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Registration Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
          <div className="bg-[#111c38] border border-[#1e2d54] rounded-2xl w-full max-w-md p-6 space-y-4">
            <h2 className="text-lg font-bold text-white">Register Edge Hospital Node</h2>
            <form onSubmit={handleRegister} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">Hospital Name</label>
                <input
                  type="text"
                  required
                  placeholder="e.g., Mayo Clinic Medical Center"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:border-cyan-400"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">Node Identifier Code</label>
                <input
                  type="text"
                  required
                  placeholder="e.g., HOSP_MAYO"
                  value={code}
                  onChange={(e) => setCode(e.target.value.toUpperCase())}
                  className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-sm font-mono text-cyan-400 focus:outline-none focus:border-cyan-400"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">Local Diagnostic Samples</label>
                <input
                  type="number"
                  value={sampleCount}
                  onChange={(e) => setSampleCount(Number(e.target.value))}
                  className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:border-cyan-400"
                />
              </div>
              <div className="flex justify-end space-x-2 pt-2">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="px-4 py-2 rounded-xl text-xs font-medium text-slate-400 hover:bg-slate-800"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 rounded-xl text-xs font-bold text-white bg-cyan-500 hover:bg-cyan-400"
                >
                  Register Node
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

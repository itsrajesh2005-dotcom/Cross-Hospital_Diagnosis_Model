import axios from 'axios';
import {
  Hospital,
  TrainingRound,
  GlobalModel,
  TrainingMetric,
  AuditLog,
  DashboardSummary,
  ConsortiumReport,
} from '../types';

const API_BASE = '/api/v1';

export const api = {
  // Dashboard
  getDashboardSummary: async (): Promise<DashboardSummary> => {
    const res = await axios.get(`${API_BASE}/dashboard/summary`);
    return res.data;
  },

  // Hospitals
  getHospitals: async (): Promise<Hospital[]> => {
    const res = await axios.get(`${API_BASE}/hospitals`);
    return res.data;
  },

  registerHospital: async (payload: { name: string; code: string; dataset_sample_count: number; location?: string }) => {
    const res = await axios.post(`${API_BASE}/hospitals/register-node`, payload);
    return res.data;
  },

  // Federated Rounds
  getRounds: async (): Promise<TrainingRound[]> => {
    const res = await axios.get(`${API_BASE}/rounds`);
    return res.data;
  },

  startRound: async (payload: { min_clients: number; target_accuracy: number }): Promise<TrainingRound> => {
    const res = await axios.post(`${API_BASE}/rounds/start`, payload);
    return res.data;
  },

  // Model Registry
  getGlobalModels: async (): Promise<GlobalModel[]> => {
    const res = await axios.get(`${API_BASE}/models/global`);
    return res.data;
  },

  getLatestGlobalModel: async (): Promise<GlobalModel> => {
    const res = await axios.get(`${API_BASE}/models/global/latest`);
    return res.data;
  },

  // Metrics
  getMetrics: async (): Promise<TrainingMetric[]> => {
    const res = await axios.get(`${API_BASE}/metrics/training`);
    return res.data;
  },

  // Audit Logs
  getAuditLogs: async (): Promise<AuditLog[]> => {
    const res = await axios.get(`${API_BASE}/audit/logs`);
    return res.data;
  },

  // Reports
  getConsortiumReport: async (): Promise<ConsortiumReport> => {
    const res = await axios.get(`${API_BASE}/reports/summary`);
    return res.data;
  },
};

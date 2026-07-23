export interface Hospital {
  id: string;
  name: string;
  code: string;
  endpoint_url?: string;
  dataset_sample_count: number;
  status: 'ACTIVE' | 'OFFLINE' | 'TRAINING' | 'ERROR';
  last_heartbeat: string;
  location: string;
  is_verified: boolean;
  created_at: string;
}

export interface TrainingRound {
  id: string;
  round_number: number;
  status: 'IDLE' | 'SELECTING' | 'TRAINING' | 'AGGREGATING' | 'COMPLETED' | 'FAILED';
  target_accuracy: number;
  min_clients: number;
  participating_clients_count: number;
  current_accuracy: number;
  current_loss: number;
  started_at: string;
  completed_at?: string;
}

export interface GlobalModel {
  id: string;
  round_id: string;
  version: string;
  s3_storage_path: string;
  accuracy: number;
  loss: number;
  f1_score: number;
  metrics_summary: Record<string, any>;
  created_at: string;
}

export interface TrainingMetric {
  id: string;
  round_id: string;
  epoch: number;
  loss: number;
  accuracy: number;
  val_loss: number;
  val_accuracy: number;
  timestamp: string;
}

export interface AuditLog {
  id: string;
  user_id?: string;
  action: string;
  resource_type: string;
  resource_id?: string;
  ip_address: string;
  details: Record<string, any>;
  created_at: string;
}

export interface DashboardSummary {
  total_hospitals: number;
  active_hospitals: number;
  total_rounds: number;
  completed_rounds: number;
  current_global_accuracy: number;
  current_global_loss: number;
  total_privacy_budget_epsilon: number;
  latest_model_version: string;
  recent_activity: Array<{
    id: string;
    action: string;
    resource_type: string;
    timestamp: string;
    details: Record<string, any>;
  }>;
}

export interface ConsortiumReport {
  title: string;
  generated_at: string;
  total_participating_hospitals: number;
  total_rounds_executed: number;
  best_global_accuracy: number;
  differential_privacy_summary: Record<string, any>;
  hospitals_summary: Array<Record<string, any>>;
  global_model_lineage: Array<Record<string, any>>;
}

from typing import List, Dict, Any
from pydantic import BaseModel


class DashboardSummary(BaseModel):
    total_hospitals: int
    active_hospitals: int
    total_rounds: int
    completed_rounds: int
    current_global_accuracy: float
    current_global_loss: float
    total_privacy_budget_epsilon: float
    latest_model_version: str
    recent_activity: List[Dict[str, Any]]


class ConsortiumReport(BaseModel):
    title: str
    generated_at: str
    total_participating_hospitals: int
    total_rounds_executed: int
    best_global_accuracy: float
    differential_privacy_summary: Dict[str, Any]
    hospitals_summary: List[Dict[str, Any]]
    global_model_lineage: List[Dict[str, Any]]

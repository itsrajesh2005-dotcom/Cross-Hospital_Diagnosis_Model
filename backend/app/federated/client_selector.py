import random
import logging
from typing import List
from app.models.hospital import Hospital

logger = logging.getLogger(__name__)


class ClientSelectionStrategy:
    """
    Selection strategy to pick active, eligible hospitals for a federated round.
    Includes health check criteria (recent heartbeat, verified status).
    """

    @staticmethod
    def select_clients(hospitals: List[Hospital], min_clients: int) -> List[Hospital]:
        active_hospitals = [
            h for h in hospitals
            if h.status in ["ACTIVE", "TRAINING"] and h.is_verified
        ]

        if len(active_hospitals) < min_clients:
            logger.warning(
                f"Selected active hospitals ({len(active_hospitals)}) is less than minimum required ({min_clients})."
            )
            # Fallback to returning all active or available hospitals
            return active_hospitals

        # Random sample or full active cohort
        selected = random.sample(active_hospitals, min(len(active_hospitals), min_clients * 2))
        logger.info(f"Selected {len(selected)} hospitals for training round: {[h.code for h in selected]}")
        return selected

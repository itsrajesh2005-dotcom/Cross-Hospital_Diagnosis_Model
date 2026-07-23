import io
import time
import logging
import requests
from typing import Optional

from hospital_node.config import node_config
from hospital_node.client.trainer import LocalTrainer, DiagnosticClassifier
from hospital_node.client.model_encryptor import ModelEncryptor

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | NodeAgent | %(message)s")


class HospitalNodeAgent:
    """
    Autonomous Hospital Edge Node Agent.
    Periodically checks aggregator server status, registers, sends health heartbeats,
    polls active federated rounds, executes local DP-SGD training, and uploads updates.
    """

    def __init__(
        self,
        name: Optional[str] = None,
        code: Optional[str] = None,
        sample_count: Optional[int] = None
    ):
        self.aggregator_url = node_config.AGGREGATOR_URL
        self.name = name or node_config.HOSPITAL_NAME
        self.code = code or node_config.HOSPITAL_CODE
        self.sample_count = sample_count or node_config.DATASET_SIZE
        self.trainer = LocalTrainer(sample_count=self.sample_count, clip_norm=node_config.CLIP_NORM)
        self.api_key: Optional[str] = None
        self.completed_round_ids = set()

    def register(self) -> bool:
        url = f"{self.aggregator_url}/hospitals/register-node"
        payload = {
            "name": self.name,
            "code": self.code,
            "dataset_sample_count": self.sample_count,
            "location": "Consortium Edge Node"
        }
        try:
            res = requests.post(url, json=payload, timeout=15)
            if res.status_code in [200, 201]:
                data = res.json()
                self.api_key = data.get("api_key")
                logger.info(f"Registered node successfully with aggregator. Code: {self.code}")
                return True
            elif res.status_code == 409:
                logger.info(f"Node '{self.code}' is already registered with central aggregator.")
                return True
            else:
                logger.warning(f"Failed to register node: {res.status_code} - {res.text}")
                return False
        except Exception as e:
            logger.warning(f"Registration request retry note ({self.code}): {e}")
            return False

    def send_heartbeat(self):
        url = f"{self.aggregator_url}/hospitals/{self.code}/heartbeat"
        payload = {"status": "ACTIVE", "dataset_sample_count": self.sample_count}
        try:
            requests.post(url, json=payload, timeout=15)
        except Exception as e:
            logger.debug(f"Heartbeat skipped: {e}")

    def poll_and_train_step(self):
        # Fetch active rounds
        url = f"{self.aggregator_url}/rounds"
        try:
            res = requests.get(url, timeout=15)
            if res.status_code != 200:
                return

            rounds = res.json()
            active_rounds = [r for r in rounds if r["status"] == "TRAINING" and r["id"] not in self.completed_round_ids]

            if not active_rounds:
                return

            target_round = active_rounds[0]
            round_id = target_round["id"]
            round_num = target_round["round_number"]

            logger.info(f"===> Starting Federated Training for Round #{round_num} (ID: {round_id}) <===")

            # Download latest global model if available
            latest_model_url = f"{self.aggregator_url}/models/global/latest"
            try:
                m_res = requests.get(latest_model_url, timeout=15)
                if m_res.status_code == 200:
                    model_id = m_res.json()["id"]
                    dl_url = f"{self.aggregator_url}/models/{model_id}/download"
                    dl_res = requests.get(dl_url, timeout=30)
                    if dl_res.status_code == 200:
                        global_state = ModelEncryptor.decode_and_deserialize(
                            ModelEncryptor.serialize_and_encode(
                                torch.load(io.BytesIO(dl_res.content))
                            )
                        )
                        self.trainer.set_weights(global_state)
                        logger.info("Successfully synced latest Global Model weights.")
            except Exception as e:
                logger.info(f"Starting round with initial model weights.")

            # Execute Local Epochs with DP Gradient Clipping
            logger.info(f"Executing {node_config.LOCAL_EPOCHS} local epochs on {self.sample_count} diagnostic samples...")
            updated_weights, loss, accuracy = self.trainer.train_epochs(
                epochs=node_config.LOCAL_EPOCHS, batch_size=node_config.BATCH_SIZE
            )

            logger.info(f"Local training complete. Local Accuracy: {accuracy * 100:.2f}%, Local Loss: {loss:.4f}")

            # Encode and Submit
            weights_b64 = ModelEncryptor.serialize_and_encode(updated_weights)
            submit_url = f"{self.aggregator_url}/rounds/{round_id}/submit-update"
            submit_payload = {
                "hospital_code": self.code,
                "sample_count": self.sample_count,
                "local_loss": loss,
                "local_accuracy": accuracy,
                "dp_epsilon": 0.45,
                "dp_delta": node_config.DP_DELTA,
                "weights_b64": weights_b64
            }

            sub_res = requests.post(submit_url, json=submit_payload, timeout=30)
            if sub_res.status_code in [200, 201]:
                logger.info(f"Successfully submitted local update for Round #{round_num}!")
                self.completed_round_ids.add(round_id)
            else:
                logger.error(f"Failed to submit update: {sub_res.status_code} - {sub_res.text}")

        except Exception as e:
            logger.warning(f"Polling step note: {e}")

    def run_forever(self, interval_seconds: int = 5):
        logger.info(f"Starting Hospital Node Agent for '{self.name}' ({self.code})...")
        self.register()
        while True:
            self.send_heartbeat()
            self.poll_and_train_step()
            time.sleep(interval_seconds)

import time
import os
import sys
import threading

# Ensure root import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from hospital_node.client.node_agent import HospitalNodeAgent


def run_node(name: str, code: str, sample_count: int):
    agent = HospitalNodeAgent(name=name, code=code, sample_count=sample_count)
    agent.run_forever(interval_seconds=6)


if __name__ == "__main__":
    print("Launching Simulated Edge Hospital Nodes...")
    nodes = [
        ("St. Jude Children's Research Hospital", "HOSP_STJUDE", 1500),
        ("Mayo Clinic Diagnostic Center", "HOSP_MAYO", 2200),
        ("Johns Hopkins Medicine", "HOSP_JOHNS_HOPKINS", 1800),
    ]

    threads = []
    for name, code, samples in nodes:
        t = threading.Thread(target=run_node, args=(name, code, samples), daemon=True)
        t.start()
        threads.append(t)
        time.sleep(2)

    print("✅ All 3 Hospital Edge Node agents running in background!")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping simulated hospital nodes.")

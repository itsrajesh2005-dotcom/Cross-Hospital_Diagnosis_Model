from hospital_node.client.node_agent import HospitalNodeAgent

if __name__ == "__main__":
    agent = HospitalNodeAgent()
    agent.run_forever(interval_seconds=5)

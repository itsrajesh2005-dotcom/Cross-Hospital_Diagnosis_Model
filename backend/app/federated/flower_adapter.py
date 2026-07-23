import logging
from typing import List, Tuple, Dict, Optional, Union
import flwr as fl
from flwr.common import Parameters, Scalar, FitRes, NDArrays, parameters_to_ndarrays, ndarrays_to_parameters

logger = logging.getLogger(__name__)


class CrossHospitalFedAvgStrategy(fl.server.strategy.FedAvg):
    """
    Flower framework (flwr) strategy adapter for Cross-Hospital FedAvg aggregation.
    Extends standard Flower FedAvg with custom metrics tracking and logging.
    """

    def __init__(
        self,
        fraction_fit: float = 1.0,
        fraction_evaluate: float = 1.0,
        min_fit_clients: int = 2,
        min_evaluate_clients: int = 2,
        min_available_clients: int = 2,
        **kwargs
    ):
        super().__init__(
            fraction_fit=fraction_fit,
            fraction_evaluate=fraction_evaluate,
            min_fit_clients=min_fit_clients,
            min_evaluate_clients=min_evaluate_clients,
            min_available_clients=min_available_clients,
            **kwargs
        )

    def aggregate_fit(
        self,
        server_round: int,
        results: List[Tuple[fl.server.client_proxy.ClientProxy, FitRes]],
        failures: List[Union[Tuple[fl.server.client_proxy.ClientProxy, FitRes], BaseException]],
    ) -> Tuple[Optional[Parameters], Dict[str, Scalar]]:
        """Aggregates local client fit results into new global parameters."""
        logger.info(f"Flower Strategy: Aggregating round {server_round} with {len(results)} client updates.")

        aggregated_parameters, aggregated_metrics = super().aggregate_fit(
            server_round, results, failures
        )

        if aggregated_parameters is not None:
            logger.info(f"Flower Strategy: Round {server_round} aggregation successful.")

        return aggregated_parameters, aggregated_metrics

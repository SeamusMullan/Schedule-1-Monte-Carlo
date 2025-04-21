from typing import Callable, Dict, Any, List, Optional
import time
import random
from collections import defaultdict


class MonteCarlo:
    """
    A framework for running Monte Carlo simulations.

    This class provides methods to run simulations multiple times and gather statistics
    about the outcomes.
    """

    def __init__(self, random_seed: Optional[int] = None):
        """
        Initialize a new Monte Carlo simulation framework.

        Args:
            random_seed (Optional[int]): Seed for random number generation. Default is None.
        """
        if random_seed is not None:
            random.seed(random_seed)

    def run_simulation(
        self,
        simulation_func: Callable[[], Dict[str, Any]],
        num_iterations: int,
        progress_interval: int = 1000,
    ) -> Dict[str, Any]:
        """
        Run a simulation multiple times and gather statistics.

        Args:
            simulation_func (Callable[[], Dict[str, Any]]): Function that runs one simulation
                and returns a dictionary of results.
            num_iterations (int): Number of iterations to run.
            progress_interval (int, optional): How often to print progress. Defaults to 1000.

        Returns:
            Dict[str, Any]: Aggregate statistics from all simulations.
        """
        results = defaultdict(list)
        total_results = defaultdict(int)

        start_time = time.time()

        for i in range(num_iterations):
            if i % progress_interval == 0 and i > 0:
                elapsed = time.time() - start_time
                per_iteration = elapsed / i
                estimated_remaining = per_iteration * (num_iterations - i)
                print(
                    f"Completed {i}/{num_iterations} iterations. "
                    f"Est. time remaining: {estimated_remaining:.2f}s"
                )

            # Run one simulation
            simulation_result = simulation_func()

            # Collect results
            for key, value in simulation_result.items():
                results[key].append(value)
                if isinstance(value, (int, float)):
                    total_results[key] += value

        # Calculate statistics
        stats = {}
        for key, values in results.items():
            if all(isinstance(v, (int, float)) for v in values):
                stats[f"{key}_total"] = sum(values)
                stats[f"{key}_mean"] = sum(values) / len(values)
                stats[f"{key}_min"] = min(values)
                stats[f"{key}_max"] = max(values)

            # Count occurrences of each unique value
            if all(isinstance(v, (str, bool, int, float)) for v in values):
                value_counts = defaultdict(int)
                for value in values:
                    value_counts[value] += 1
                stats[f"{key}_counts"] = dict(value_counts)

                # Calculate percentages
                stats[f"{key}_percentages"] = {
                    value: count / num_iterations * 100
                    for value, count in value_counts.items()
                }

        total_time = time.time() - start_time
        stats["total_iterations"] = num_iterations
        stats["total_time_seconds"] = total_time
        stats["iterations_per_second"] = num_iterations / total_time

        return stats

import time
# import unittest
import threading

from datadog import lambda_stats, datadog_lambda_wrapper
from datadog.threadstats.aws_lambda import _lambda_stats


TOTAL_NUMBER_OF_THREADS = 1000


class MemoryReporter(object):
    """ A reporting class that reports to memory for testing. """

    def __init__(self):
        self.distributions = []
        self.dist_flush_counter = 0

    def flush_distributions(self, dists):
        self.distributions += dists
        self.dist_flush_counter = self.dist_flush_counter + 1


@datadog_lambda_wrapper
def wrapped_function(id):
    lambda_stats("dist_" + str(id), 42)
    # sleep makes the os continue another thread
    time.sleep(0.001)

    lambda_stats("common_dist", 42)


class TestWrapperThreadSafety(object):

    def test_wrapper_thread_safety(self):
        _lambda_stats.reporter = MemoryReporter()

        for i in range(TOTAL_NUMBER_OF_THREADS):
            threading.Thread(target=wrapped_function, args=[i]).start()
        # Wait all threads to finish
        time.sleep(10)

        # Check that at least one flush happened
        self.assertGreater(_lambda_stats.reporter.dist_flush_counter, 0)

        dists = _lambda_stats.reporter.distributions
        self.assertEqual(len(dists), TOTAL_NUMBER_OF_THREADS + 1)

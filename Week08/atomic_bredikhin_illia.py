import threading
import random


class AtomicOperation(threading.Thread):
    def __init__(self, number_of_points: int = 100000):
        super().__init__()
        self.number_of_points = number_of_points
        self.inner_points = 0
        self.total_points = 0

    def run(self):
        inner = 0

        for _ in range(self.number_of_points):
            x = random.random()
            y = random.random()

            if x * x + y * y <= 1:
                inner += 1

        self.inner_points = inner
        self.total_points = self.number_of_points


class AtomicPiEstimator(threading.Thread):
    def __init__(
        self,
        desired_accuracy: float = 1.0e-4,
        number_of_threads: int = 4,
        chunk_size: int = 100000
    ):
        super().__init__()

        self.desired_accuracy = desired_accuracy
        self.number_of_threads = number_of_threads
        self.chunk_size = chunk_size

        self.inner_points = 0
        self.total_points = 0

    def pi(self) -> float:
        if self.total_points == 0:
            return 0.0

        return 4 * self.inner_points / self.total_points

    def accuracy(self) -> float:
        import math
        return abs(math.pi - self.pi())

    def run(self):
        while self.accuracy() > self.desired_accuracy:
            workers = []

            for _ in range(self.number_of_threads):
                worker = AtomicOperation(self.chunk_size)
                workers.append(worker)
                worker.start()

            for worker in workers:
                worker.join()

            for worker in workers:
                self.inner_points += worker.inner_points
                self.total_points += worker.total_points


if __name__ == "__main__":
    estimator = AtomicPiEstimator(
        desired_accuracy=1e-5,
        number_of_threads=8,
        chunk_size=100000
    )

    estimator.start()
    estimator.join()

    print(f"PI = {estimator.pi()}")
    print(f"Accuracy = {estimator.accuracy()}")

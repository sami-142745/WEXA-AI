import math


class Statistics:

    @staticmethod
    def average(values):
        return sum(values) / len(values)

    @staticmethod
    def minimum(values):
        return min(values)

    @staticmethod
    def maximum(values):
        return max(values)

    @staticmethod
    def percentile(values, p):

        values = sorted(values)

        k = math.ceil((p / 100) * len(values)) - 1

        return values[max(0, k)]
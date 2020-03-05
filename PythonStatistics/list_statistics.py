import math


class ListStatistics:
    def __init__(self, input_list):
        assert input_list is not None
        self.input = input_list

    def mean(self):
        if len(self.input) <= 0:
            return float('NaN')

        list_sum = 0
        for num in self.input:
            list_sum += num

        return list_sum / len(self.input)

    def median(self):
        sorted_list = sorted(self.input)
        if len(sorted_list) % 2 == 0:
            index1 = int(len(sorted_list) / 2)
            index2 = int(len(sorted_list) / 2) - 1
            return (sorted_list[index1] + sorted_list[index2]) / 2
        else:
            return sorted_list[int(len(sorted_list) / 2)]

    def variance(self):
        if len(self.input) <= 1:
            return float('NaN')

        mean = self.mean()
        var_sum = 0

        for num in self.input:
            var_sum += math.pow((num - mean), 2)

        return var_sum / (len(self.input)-1)

    def std(self):
        return math.sqrt(self.variance())
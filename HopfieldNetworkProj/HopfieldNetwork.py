import numpy as np


class HopfieldNetwork:
    def __init__(self, size=5):
        self.log_intermediate = False
        self.__n = size
        self.__weights = np.matrix(np.zeros(shape=(self.__n, self.__n)))
        self.__thresholds = np.transpose(np.matrix(np.zeros(shape=self.__n)))

    def train_by_generalised_hebb_rule(self, patterns):
        w = np.matrix(np.zeros(shape=(self.__n, self.__n)))

        for i in range(0, self.__n):
            for j in range(0, self.__n):
                if i != j:
                    for k in range(0, patterns.shape[0]):
                        w[i, j] += patterns[k, i] * patterns[k, j]

                    w[i, j] /= self.__n

        self.__weights = w

        if self.log_intermediate:
            print("Learned weights = " + " \n" + str(self.__weights))

    def build_network_async(self, input_values):
        if self.__thresholds.shape != input_values.shape:
            raise AssertionError('input_values should be a vector of size ' + str(self.__n))

        outputs = np.copy(input_values)

        e_prev = np.zeros(shape=self.__n)
        e_cur = np.zeros(shape=self.__n)

        index = 0
        neuron_num = 0

        while index < 100:
            index += 1

            sum_temp = self.__weights[neuron_num] * outputs

            if self.log_intermediate:
                print("sums_temp for index = " + str(index) + " \n" + str(sum_temp))

            outputs[neuron_num] = 1 if self.__thresholds[neuron_num] <= sum_temp else -1

            if self.log_intermediate:
                print("outputs for index = " + str(index) + " \n " + str(outputs))

            e_sum = 0;
            e_bias = 0

            for i in range(0, self.__n):
                for j in range(0, self.__n):
                    e_sum += self.__weights[i, j] * outputs[i] * outputs[j]
                    e_bias += self.__thresholds[i] * outputs[i]

            e = -0.5 * e_sum + e_bias
            e_cur[neuron_num] = e;

            if self.log_intermediate:
                print("Energy of index " + str(index) + " = " + str(e) + " \n\n")

            neuron_num += 1

            if neuron_num == self.__n:
                neuron_num = 0

                if self._energy_is_the_same(e_prev, e_cur):
                    break

                e_prev = np.copy(e_cur)

        return outputs


    def _energy_is_the_same(self, e_prev, e_cur):
        for i in range(0, self.__n):
            if e_prev[i] != e_cur[i]:
                return False

        return True


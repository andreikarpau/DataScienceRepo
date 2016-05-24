import sys
import numpy as np

class HopfieldNetwork:
    n = 5
    weights = np.matrix(np.zeros(shape=(5, 5)))
    thresholds = np.transpose(np.matrix(np.zeros(shape=5)))
    log_intermediate = False

    def __init__(self, size):
        self.n = size
        self.weights = np.matrix(np.zeros(shape=(self.n, self.n)))
        self.thresholds = np.transpose(np.matrix(np.zeros(shape=self.n)))

    def _energy_is_the_same(self, e_prev, e_cur):
        for i in range(0, self.n):
            if e_prev[i] != e_cur[i]:
                return False

        return True

    def build_network_async(self, input_values):
        if self.thresholds.shape != input_values.shape:
            raise AssertionError('input_values should be a vector of size ' + str(self.n))

        outputs = np.copy(input_values)

        e_prev = np.zeros(shape=self.n)
        e_cur = np.zeros(shape=self.n)

        index = 0
        neuron_num = 0

        while index < 100:
            index += 1

            sums_temp = self.weights[neuron_num] * outputs

            if self.log_intermediate:
                print("sums_temp for index = " + str(index) + " \n" + str(sums_temp))

            bool_output = self.thresholds[neuron_num] <= sums_temp
            outputs[neuron_num] = bool_output.astype(int)

            if self.log_intermediate:
                print("outputs for index = " + str(index) + " \n " + str(outputs))

            e_sum = 0;
            e_bias = 0

            for i in range(0, self.n):
                for j in range(0, self.n):
                    e_sum += self.weights[i,j] * outputs[i] * outputs[j]
                    e_bias += self.thresholds[i] * outputs[i]

            e = -0.5 * e_sum + e_bias
            e_cur[neuron_num] = e;

            if self.log_intermediate:
                print("Energy of index " + str(index) + " = " + str(e) + " \n\n")

            neuron_num += 1

            if neuron_num == self.n:
                neuron_num = 0

                if self._energy_is_the_same(e_prev, e_cur):
                    break

                e_prev = np.copy(e_cur)

        return outputs
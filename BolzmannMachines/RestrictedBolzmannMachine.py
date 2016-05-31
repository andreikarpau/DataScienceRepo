import numpy as np


class RestrictedBolzmannMachine:
    log_intermediate = False
    v_size = 0
    h_size = 0
    w = []

    def __init__(self, v_count, h_count):
        self.v_size = v_count + 1
        self.h_size = h_count

    def train(self, input_samples):
        data = np.ones(shape=(input_samples.shape[0], self.v_size))
        data[:, :-1] = input_samples
        data = np.matrix(data)

        epoch_count = 10

        np.random.seed(0)
        self.w = np.random.normal(0, 0.01, self.v_size * self.h_size)
        self.w = np.matrix(np.reshape(self.w, (self.v_size, self.h_size)))

        for i in range(epoch_count):
            is_last_epoch = (epoch_count - 1) == i

            if self.log_intermediate:
                print("\n" + "train epoch: " + str(i) + " is_last_epoch = " + str(is_last_epoch))

            positive_delta_v = self.__positive_gradient(data, self.w, is_last_epoch)
            negative_delta_v = self.__negative_gradient(data, self.w, True)

            self.w += positive_delta_v

            if self.log_intermediate:
                print("\n" + "new w: " + "\n" + str(self.w))

    @staticmethod
    def __positive_phase_probabilities(v, w):
        sums = -(v * w)
        prob = 1 / (1 + np.exp(-sums))
        return prob

    @staticmethod
    def __sigmoid(vector):
        v = np.copy(vector)
        v[v >= 0.5] = 1
        v[v < 0.5] = 0
        return v

    def __positive_gradient(self, data, w, is_last_epoch):
        w_stats = []

        for data_i in range(data.shape[0]):
            v = data[data_i]
            h_prob = self.__positive_phase_probabilities(v, w)

            h_sample = []

            for i in range(h_prob.shape[1]):
                p = h_prob[0, i]

                if is_last_epoch:
                    h_sample.append(p)
                else:
                    h_tmp = np.random.choice([1., 0.], p=[p, 1 - p])
                    h_sample.append(h_tmp)

            h_sample = np.matrix(h_sample)

            w_stats_example = v.T * h_sample
            w_stats.append(w_stats_example)

        w_stats_mean = np.mean(w_stats, axis=0)

        if self.log_intermediate:
            print("__positive_gradient w_stats_mean: " + "\n" + str(w_stats_mean))

        return w_stats_mean


    def __negative_gradient(self, data, w, generate_v):
        w_stats = []

        for data_i in range(data.shape[0]):
            v = data[data_i]
            h = self.__sigmoid(self.__positive_phase_probabilities(v, w))


#visible bias log[pi/(1−pi)]
            print "Negative h = " + str(h)
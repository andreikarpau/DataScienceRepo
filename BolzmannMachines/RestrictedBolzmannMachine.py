import numpy as np


class RestrictedBolzmannMachine:
    log_intermediate = False
    v_size = 0
    h_size = 0
    rate = 0.1
    epochs_count = 10

    # weights matrix
    w = []
    hidden_bias = []
    visual_bias = []

    def __init__(self, v_count, h_count, learning_rate=0.1, epochs_count = 10):
        self.v_size = v_count
        self.h_size = h_count
        self.rate = learning_rate
        self.epochs_count = epochs_count

    def train(self, input_samples):
        np.random.seed(0)
        self.w = np.random.normal(0, 0.01, self.v_size * self.h_size)
        self.w = np.matrix(np.reshape(self.w, (self.v_size, self.h_size)))

        self.hidden_bias = np.matrix(np.zeros(shape=self.h_size))
        self.visible_bias = np.matrix(np.zeros(shape=self.v_size))

        for i in range(self.epochs_count):
            w_h_biased = np.matrix(np.zeros(shape=(self.v_size + 1, self.h_size)))
            w_h_biased[:-1, :] = self.w.copy()
            w_h_biased[-1,:] = self.hidden_bias.copy()

            w_v_biased = np.matrix(np.zeros(shape=(self.v_size, self.h_size + 1)))
            w_v_biased[:, :-1] = self.w.copy()
            w_v_biased[:,-1] = self.visible_bias.T.copy()

            is_last_epoch = (self.epochs_count - 1) == i

            if self.log_intermediate:
                print ("\n" + "train epoch: " + str(i) + " is_last_epoch = " + str(is_last_epoch))

            pos_v_bias_stats = []
            neg_v_bias_stats = []

            pos_w_stats = []
            pos_h_bias_stats = []

            neg_w_stats = []
            neg_h_bias_stats = []

            for data_i in range(input_samples.shape[0]):
                v = input_samples[data_i]

                v_biased = self.__get_biased_vector(v, self.v_size + 1)
                h_vector = self.__count_layer_vector(v_biased, w_h_biased, is_last_epoch)

                # positive gradient for v bias vector. Use states for it.
                pos_v_bias_stat = v

                # positive gradient for w and h bias
                pos_w_stat, pos_h_bias_stat = self.__count_gradient(v_biased, h_vector)

                h_biased = self.__get_biased_vector(h_vector, self.h_size + 1)
                v_generated = self.__count_layer_vector(h_biased, w_v_biased.T, is_last_epoch)

                # negative gradient for v bias vector. Use states for it.
                neg_v_bias_stat = v_generated

                v_generated_biased = self.__get_biased_vector(v_generated, self.v_size + 1)
                h_vector_generated = self.__count_layer_vector(v_generated_biased, w_h_biased, is_last_epoch)

                # negative gradient for w and h bias
                neg_w_stat, neg_h_bias_stat = self.__count_gradient(v_generated_biased, h_vector_generated)

                pos_v_bias_stats.append(pos_v_bias_stat)
                neg_v_bias_stats.append(neg_v_bias_stat)

                pos_w_stats.append(pos_w_stat)
                neg_w_stats.append(neg_w_stat)

                pos_h_bias_stats.append(pos_h_bias_stat)
                neg_h_bias_stats.append(neg_h_bias_stat)

            pos_v_gradient = np.mean(pos_v_bias_stats, axis=0)
            neg_v_gradient = np.mean(neg_v_bias_stats, axis=0)

            pos_w_gradient = np.mean(pos_w_stats, axis=0)
            neg_w_gradient = np.mean(neg_w_stats, axis=0)

            pos_h_gradient = np.mean(pos_h_bias_stats, axis=0)
            neg_h_gradient = np.mean(neg_h_bias_stats, axis=0)

            self.w += self.rate * (pos_w_gradient - neg_w_gradient)
            self.visible_bias += self.rate * (pos_v_gradient - neg_v_gradient)
            self.hidden_bias += self.rate * (pos_h_gradient - neg_h_gradient)

            if self.log_intermediate:
                print("\n" + "new w: " + "\n" + str(self.w))
                print("\n" + "new visible bias: " + "\n" + str(self.visible_bias))
                print("\n" + "new hidden bias: " + "\n" + str(self.hidden_bias))

    @staticmethod
    def __exp_sigmoid(sums):
        return  1 / (1 + np.exp(-sums))

    def __cpunt_probabilities(self, v, w):
        sums = -(v * w)
        prob = self.__exp_sigmoid(sums)
        return prob

    @staticmethod
    def __sigmoid(vector):
        v = np.copy(vector)
        v[v >= 0.5] = 1
        v[v < 0.5] = 0
        return v

    def __get_biased_vector(self, vector, biased_size):
        vector_biased = np.ones(shape=biased_size)
        vector_biased[:-1] = vector
        return np.matrix(vector_biased)

    def __count_layer_vector(self, vector_biased, weights_biased, use_probabilities_values):
        vector_prob = self.__cpunt_probabilities(vector_biased, weights_biased)

        sample_vector = []
        for i in range(vector_prob.shape[1]):
            p = vector_prob[0, i]

            if use_probabilities_values:
                sample_vector.append(p)
            else:
                generated_value= np.random.choice([1., 0.], p=[p, 1 - p])
                sample_vector.append(generated_value)

        return np.matrix(sample_vector)

    def __count_gradient(self, v_biased, h_vector):
        w_stats = v_biased.T * h_vector
        h_bias_stats = w_stats[-1,:]
        w_stats = w_stats[:-1,:]
        return w_stats, h_bias_stats

        # w_stats = []
        #
        # data_to_h = np.ones(shape=(input_samples.shape[0], self.v_size + 1))
        # data_to_h[:, :-1] = input_samples
        # data_to_h = np.matrix(data_to_h)
        #
        # for data_i in range(data_to_h.shape[0]):
        #     v = data_to_h[data_i]
        #     h_prob = self.__positive_phase_probabilities(v, self.w)
        #
        #     h_sample = []
        #
        #     for i in range(h_prob.shape[1]):
        #         p = h_prob[0, i]
        #
        #         if is_last_epoch:
        #             h_sample.append(p)
        #         else:
        #             h_tmp = np.random.choice([1., 0.], p=[p, 1 - p])
        #             h_sample.append(h_tmp)
        #
        #     h_sample = np.matrix(h_sample)
        #
        #     w_stats_example = v.T * h_sample
        #     w_stats.append(w_stats_example)
        #
        # w_stats_mean = np.mean(w_stats, axis=0)
        #
        # if self.log_intermediate:
        #     print("__positive_gradient w_stats_mean: " + "\n" + str(w_stats_mean))
        #
        # return w_stats_mean


    # def __negative_gradient(self, data, generate_v):
    #     w_stats = []
    #
    #     for data_i in range(data.shape[0]):
    #         v = data[data_i]
    #         h = self.__sigmoid(self.__positive_phase_probabilities(v, self.w))
    #
    #         print "Negative h = " + str(h)
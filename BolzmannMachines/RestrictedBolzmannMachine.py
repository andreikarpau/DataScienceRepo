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

    def count_visible_from_visible(self, input_sample):
        hidden = self.count_hidden(input_sample)
        visible = self.count_visible(hidden)
        return visible

    def count_visible(self, hidden_sample):
        w_v_biased = np.matrix(np.zeros(shape=(self.v_size, self.h_size + 1)))
        w_v_biased[:, :-1] = self.w.copy()
        w_v_biased[:, -1] = self.visible_bias.T.copy()

        h_biased = self.__get_biased_vector(hidden_sample, self.h_size + 1)
        v_generated = self.__count_layer_vector(h_biased, w_v_biased.T, True)

        if self.log_intermediate:
            print("\n" + "v_vector probabilities: " + "\n" + str(v_generated))

        v_generated = self.__make_binary(v_generated)
        return v_generated

    def count_hidden(self, input_sample):
        v = input_sample

        w_h_biased = np.matrix(np.zeros(shape=(self.v_size + 1, self.h_size)))
        w_h_biased[:-1, :] = self.w.copy()
        w_h_biased[-1, :] = self.hidden_bias.copy()

        v_biased = self.__get_biased_vector(v, self.v_size + 1)
        h_vector = self.__count_layer_vector(v_biased, w_h_biased, True)

        if self.log_intermediate:
            print("\n" + "h_vector probabilities: " + "\n" + str(h_vector))

        h_vector = self.__make_binary(h_vector)
        return h_vector

    def train(self, input_samples):
        np.random.seed(0)
        self.w = np.random.normal(0, 0.01, self.v_size * self.h_size)
        self.w = np.matrix(np.reshape(self.w, (self.v_size, self.h_size)))

        self.hidden_bias = np.matrix(np.zeros(shape=self.h_size))
        self.visible_bias = np.matrix(np.zeros(shape=self.v_size))

        self.visible_bias.fill(self.__count_initial_visible_bias(input_samples))

        if len(input_samples.shape) == 1:
            input_samples = input_samples.reshape(1, input_samples.shape[0])

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

            total_squared_error = 0

            for data_i in range(input_samples.shape[0]):
                v = input_samples[data_i]

                v_biased = self.__get_biased_vector(v, self.v_size + 1)
                h_vector = self.__count_layer_vector(v_biased, w_h_biased, is_last_epoch)

                # positive gradient for v bias vector. Use states for it.
                pos_v_bias_stat = v

                # positive gradient for w and h bias
                pos_w_stat, pos_h_bias_stat = self.__count_gradient(v_biased, h_vector)

                h_biased = self.__get_biased_vector(h_vector, self.h_size + 1)
                v_generated = self.__count_layer_vector(h_biased, w_v_biased.T, True)

                error = v - v_generated
                total_squared_error += error * error.T

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

            print("\n total squared error = " + str(total_squared_error))

    @staticmethod
    def __count_initial_visible_bias(input_samples):
        p = float(np.sum(input_samples)) / np.product(input_samples.shape)
        value = np.log((p / (1 - p)))
        return value

    @staticmethod
    def __exp_sigmoid(x):
        return 1 / (1 + np.exp(-x))

    def __count_probabilities(self, v, w):
        sums = v * w
        prob = self.__exp_sigmoid(sums)
        return prob

    @staticmethod
    def __make_binary(vector):
        v = np.copy(vector)
        v[v >= 0.5] = 1
        v[v < 0.5] = 0
        return v

    def __get_biased_vector(self, vector, biased_size):
        vector_biased = np.ones(shape=biased_size)
        vector_biased[:-1] = vector
        return np.matrix(vector_biased)

    def __count_layer_vector(self, vector_biased, weights_biased, use_probabilities_values):
        vector_prob = self.__count_probabilities(vector_biased, weights_biased)

        sample_vector = []
        for i in range(vector_prob.shape[1]):
            p = vector_prob[0, i]

            if use_probabilities_values:
                sample_vector.append(p)
            else:
                generated_value= np.random.choice([1., 0.], p=[p, 1 - p])
                sample_vector.append(generated_value)

        return np.matrix(sample_vector)

    @staticmethod
    def __count_gradient(v_biased, h_vector):
        w_stats = v_biased.T * h_vector
        h_bias_stats = w_stats[-1,:]
        w_stats = w_stats[:-1,:]
        return w_stats, h_bias_stats

    def __get_energy(self, v, h):
        sum = self.visible_bias * v.T + self.hidden_bias * h.T + np.sum(np.multiply(v.T * h, self.w))
        return -sum


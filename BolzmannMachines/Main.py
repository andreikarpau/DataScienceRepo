import numpy as np
import RestrictedBolzmannMachine as rbmachine

num_v = 4
num_h = 2

input_samples = np.array(([1, 0, 1, 1], [1, 1, 1, 0], [1, 0, 0, 1]))

rbm = rbmachine.RestrictedBolzmannMachine(num_v, num_h)
rbm.log_intermediate = True

rbm.train(input_samples)


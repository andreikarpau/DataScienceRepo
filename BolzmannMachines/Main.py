import numpy as np
import RestrictedBolzmannMachine as rbmachine

num_v = 9
num_h = 4

input_samples = np.array(([1, 0, 1, 1, 0, 1, 1, 0, 1]))
#input_samples = np.array(([1, 0, 1, 1], [1, 1, 1, 0], [1, 0, 0, 1]))

rbm = rbmachine.RestrictedBolzmannMachine(num_v, num_h, 0.5, 50)
rbm.log_intermediate = True

rbm.train(input_samples)


import numpy as np
import RestrictedBolzmannMachine as rbmachine

num_v = 9
num_h = 5

input_samples = np.array(([1, 0, 1, 1, 0, 1, 1, 0, 1],
                          [1, 0, 1, 0, 0, 1, 0, 1, 0],
                          [0, 0, 0, 1, 0, 0, 1, 0, 0],
                          [1, 0, 1, 1, 0, 0, 0, 0, 1],
                          [0, 0, 1, 1, 0, 1, 1, 1, 0]))

rbm = rbmachine.RestrictedBolzmannMachine(num_v, num_h, 1, 150)
rbm.log_intermediate = False

rbm.train(input_samples)

hidden = rbm.calculate_hidden(input_samples[0])
print "\n" + "Hidden counted:"
print hidden

visible = rbm.calculate_visible(hidden)
print "\n" + "Visible counted:"
print visible


hidden = rbm.calculate_hidden(input_samples[4])
print "\n" + "Hidden counted:"
print hidden

visible = rbm.calculate_visible(hidden)
print "\n" + "Visible counted:"
print visible



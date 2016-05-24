import numpy as np
import HopfieldNetwork as hn

# Verify network with sample data
h = hn.HopfieldNetwork(5)

sample_input_values = np.transpose(np.matrix([0, 1, 1, 0, 0]))
sample_answer = np.transpose(np.matrix([0, 1, 1, 0, 1]))

h.log_intermediate = True
h.weights = np.matrix([[0, -1, -1, 1, -1], [-1, 0, 1, -1, 1], [-1, 1, 0, -1, 1], [1, 1, -1, 0, -1], [-1, 1, 1, -1, 0]])
h.thresholds = np.transpose(np.matrix(np.zeros(shape=5)))

res = h.build_network_async(sample_input_values)

print("Result:")
print(res)
print("res == sample_answer " + str(sum(res == sample_answer) == 5))




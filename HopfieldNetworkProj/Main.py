import numpy as np
import HopfieldNetwork as hn

# Verify network with sample data
h = hn.HopfieldNetwork(5)
h.log_intermediate = True

sample_input_values = np.transpose(np.matrix([-1, 1, 1, -1, -1]))
sample_answer = np.transpose(np.matrix([-1, 1, 1, -1, 1]))

h.train_by_generalised_hebb_rule(np.matrix([-1, 1, 1, -1, 1]))

res = h.build_network_async(sample_input_values)

print("Result:")
print(res)
print("res == sample_answer " + str(sum(res == sample_answer) == 5))

patterns = np.matrix([[-1, -1, 1, -1, -1, -1], [1, -1, 1, -1, 1, -1], [-1, 1, 1, 1, 1, -1]])
h2 = hn.HopfieldNetwork(6)
h2.log_intermediate = True
h2.train_by_generalised_hebb_rule(patterns)

sample_input_values = np.transpose(np.matrix([1, 1, 1, 1, 1, -1]))
res = h2.build_network_async(sample_input_values)

print("Result:")
print(res)
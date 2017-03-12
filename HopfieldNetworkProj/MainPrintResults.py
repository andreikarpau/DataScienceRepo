import matplotlib.pyplot as plt
import numpy as np
import HopfieldNetwork as hn

image1 = np.zeros(shape=(10, 10))

image1[4:6, 3] = 1
image1[5, 1:3] = 1
image1[6, 1] = 1
image1[6, 3:9] = 1
image1[7, 3:10] = 1
image1[7:10, 3] = 1
image1[7:10, 8] = 1

image2 = np.zeros(shape=(10, 10))
image2[1, 0:10] = 1
image2[2, (2, 8)] = 1
image2[3, (3, 7)] = 1

image2[4, 4:7] = 1
image2[5:7, 3] = 1
image2[5:7, 7] = 1
image2[7, 4:7] = 1

image1_detect = np.copy(image1)
image1_detect[6, 1] = 0
image1_detect[1, 1:3] = 1
image1_detect[3, 7:9] = 1
image1_detect[8, 4:6] = 1

plt.subplot(441)
plt.imshow(image1)
plt.subplot(442)
plt.imshow(image2)
plt.subplot(443)
plt.imshow(image1_detect)


h = hn.HopfieldNetwork(100)
h.log_intermediate = True

learn_vector1 = np.asarray(2 * image1 - 1).reshape(-1)
learn_vector2 = np.asarray(2 * image2 - 1).reshape(-1)

image1_detect_vector = np.transpose(np.matrix(np.asarray(2 * image1 - 1).reshape(-1)))

h.train_by_generalised_hebb_rule(np.matrix([learn_vector1, learn_vector2]))
res = h.build_network_async(image1_detect_vector)

image1_detected = np.asarray((np.transpose(res) + 1) / 2).reshape(10,10)

plt.subplot(444)
plt.imshow(image1_detected)
plt.show()

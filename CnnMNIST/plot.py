import numpy as np
import matplotlib.pyplot as plt
import pickle


weights = None

with open('./weights_out/epoch1', 'rb') as input_file:
    weights = pickle.load(input_file)
    weights = weights - weights.min()
    weights = weights / weights.max() * 255

rows_num = int(weights.shape[3] / 4)
_, ax = plt.subplots(nrows=rows_num, ncols=4)

for channel_index in range(weights.shape[3]):
    image_np = weights[:,:,0,channel_index]
    image_arr = np.asarray(image_np)
    plt.subplot(rows_num, 4, channel_index + 1)
    plt.imshow(image_arr, cmap='gray')

plt.show()
print(weights)
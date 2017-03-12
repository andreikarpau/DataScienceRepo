import numpy as np
import RestrictedBolzmannMachine as rbmachine
import Image as im
from ImagesHelper import ImagesHelper as ih

sunImage = im.open("Data/Sun30.bmp")
ninjaImage = im.open("Data/Ninja30.bmp")
robotImage = im.open("Data/Robot30.bmp")
logoImage = im.open("Data/Logo30.bmp")

sumMask = ih.get_bit_mask_from_bitmap(sunImage)
ninjaMask = ih.get_bit_mask_from_bitmap(ninjaImage)
robotMask = ih.get_bit_mask_from_bitmap(robotImage)
logoMask = ih.get_bit_mask_from_bitmap(logoImage)

#---------------------First level machine---------------------------------
input_samples = np.array([sumMask, ninjaMask, logoMask])

rbm = rbmachine.RestrictedBolzmannMachine(900, 400, 3, 50)
rbm.log_intermediate = False

rbm.train(input_samples)

hidden_sun = rbm.calculate_hidden(sumMask)
visible_sun = rbm.calculate_visible(hidden_sun)

#ih.subplot_bit_mask(hidden_sun, 20, 20, 321)
#ih.subplot_bit_mask(visible_sun, 30, 30, 322)

hidden_ninja = rbm.calculate_hidden(ninjaMask)
visible_ninja = rbm.calculate_visible(hidden_ninja)

#ih.subplot_bit_mask(hidden_ninja, 20, 20, 323)
#ih.subplot_bit_mask(visible_ninja, 30, 30, 324)

hidden_logo = rbm.calculate_hidden(logoMask)
visible_logo = rbm.calculate_visible(hidden_logo)

#ih.subplot_bit_mask(hidden_logo, 20, 20, 325)
#ih.subplot_bit_mask(visible_logo, 30, 30, 326, True)

#---------------------Second level machine---------------------------------
input_samples2 = np.array([hidden_sun, hidden_ninja, hidden_logo])

rbm2 = rbmachine.RestrictedBolzmannMachine(400, 100, 3, 250)
rbm2.log_intermediate = False
rbm2.train(input_samples2)

hidden_sun2 = rbm2.calculate_hidden(hidden_sun)
visible_sun2 = rbm2.calculate_visible(hidden_sun2)

ih.subplot_bit_mask(hidden_sun2, 10, 10, 331)
ih.subplot_bit_mask(visible_sun2, 20, 20, 332)
ih.subplot_bit_mask(visible_sun, 30, 30, 333)

hidden_ninja2 = rbm2.calculate_hidden(hidden_ninja)
visible_ninja2 = rbm2.calculate_visible(hidden_ninja2)

ih.subplot_bit_mask(hidden_ninja2, 10, 10, 334)
ih.subplot_bit_mask(visible_ninja2, 20, 20, 335)
ih.subplot_bit_mask(visible_ninja, 30, 30, 336)

hidden_logo2 = rbm2.calculate_hidden(hidden_logo)
visible_logo2 = rbm2.calculate_visible(hidden_logo2)

ih.subplot_bit_mask(hidden_logo2, 10, 10, 337)
ih.subplot_bit_mask(visible_logo2, 20, 20, 338)
ih.subplot_bit_mask(visible_logo, 30, 30, 339, True)

#---------------------Third level machine---------------------------------
# input_samples3 = np.array([hidden_sun2, hidden_ninja2, hidden_logo2])
#
# rbm3 = rbmachine.RestrictedBolzmannMachine(100, 81, 5, 300)
# rbm3.log_intermediate = False
# rbm3.train(input_samples3)
#
# hidden_sun3 = rbm3.count_hidden(hidden_sun2)
# visible_sun3 = rbm3.count_visible(hidden_sun3)
#
# ih.subplot_bit_mask(hidden_sun3, 9, 9, 331)
# ih.subplot_bit_mask(visible_sun3, 10, 10, 332)
# ih.subplot_bit_mask(visible_sun, 30, 30, 333)
#
# hidden_ninja3 = rbm3.count_hidden(hidden_ninja2)
# visible_ninja3 = rbm3.count_visible(hidden_ninja3)
#
# ih.subplot_bit_mask(hidden_ninja3, 9, 9, 334)
# ih.subplot_bit_mask(visible_ninja3, 10, 10, 335)
# ih.subplot_bit_mask(visible_ninja, 30, 30, 336)
#
# hidden_logo3 = rbm3.count_hidden(hidden_logo2)
# visible_logo3 = rbm3.count_visible(hidden_logo3)
#
# ih.subplot_bit_mask(hidden_logo3, 9, 9, 337)
# ih.subplot_bit_mask(visible_logo3, 10, 10, 338)
# ih.subplot_bit_mask(visible_logo, 30, 30, 339, True)
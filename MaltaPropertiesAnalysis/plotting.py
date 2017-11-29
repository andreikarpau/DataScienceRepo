import matplotlib.pyplot as plt
from helper import FileHelper

ids, bedrooms, prices, latitudes, longitudes, bedroom_prices = FileHelper.get_geocoded_data()

# Location-Price plotting
#-------------------------------------
# plt.scatter(longitudes, latitudes, c=prices, s=50, cmap='BrBG')
# plt.colorbar()
# plt.show()

# Location-BedroomPrice plotting
#-------------------------------------
# plt.scatter(longitudes, latitudes, c=bedroom_prices, s=50, cmap='BrBG')
# plt.colorbar()
# plt.show()

# Location-Bedrooms plotting
#-------------------------------------
plt.scatter(longitudes, latitudes, c=bedrooms, s=50, cmap='BrBG')
plt.colorbar()
plt.show()

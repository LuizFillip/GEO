import matplotlib.pyplot as plt
import numpy as np

# Sample curves
curve1 = np.arange(100) # Replace with your own curve data
curve2 = curve1 * (-30) # Replace with your own curve data

plt.plot(curve1)
plt.plot(curve2)

# Calculate derivatives
derivative1 = np.gradient(curve1)
derivative2 = np.gradient(curve2)

# Calculate dot product
dot_product = np.dot(derivative1, derivative2)

# Calculate magnitudes
norm1 = np.linalg.norm(derivative1)
norm2 = np.linalg.norm(derivative2)

# Calculate angle in radians
angle_radians = np.arccos(dot_product / (norm1 * norm2))

# Convert angle to degrees
angle_degrees = np.degrees(angle_radians)

print("Angle between the curves: {:.2f} degrees".format(angle_degrees))

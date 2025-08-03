import plotext as plt
import numpy as np

# Sample RPG stats
categories = ['Tech', 'Theory', 'Practice', 'Research', 'Communication']
values = [7, 9, 6, 8, 5]

# Normalize values (optional)
max_val = max(values)
values_norm = [v / max_val for v in values]

# Angles for each category (in radians)
angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False)

# Close the loop for radar shape
values_norm += values_norm[:1]
angles = np.append(angles, angles[0])

# Create polar plot
plt.polar(angles, values_norm)

# Add labels (you can print separately, as plotext can't put text at angles well)
plt.title("Skills Radar (Normalized)")
plt.show()
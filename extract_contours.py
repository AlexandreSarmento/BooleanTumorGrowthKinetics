#! /bin/python3
# Tue Oct  4 16:52:47 2022 ------------------------------

#import cv2 
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import find_contours
from skimage.morphology import binary_opening, binary_closing

# C:/Users/Alexandre Sarmento/Documents/PYTHON/UFRN/BooleanKinetics
matrix_skmel = np.loadtxt(
    'C:/Users/Alexandre Sarmento/Documents/PYTHON/UFRN/BooleanKinetics/contor/hipo2/matrix7_skmel.tsv', 
    delimiter='\t', 
    dtype='uint8')
# opening = binary_opening(matrix_skmel)
closing = binary_closing(matrix_skmel)

# contours, hierarchy = cv2.findContours(matrix_skmel,
#   mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)

contours = find_contours(closing, fully_connected='high', positive_orientation='low')
counts = np.concatenate(contours)

np.savetxt(
    'C:/Users/Alexandre Sarmento/Documents/PYTHON/UFRN/BooleanKinetics/contor/hipo2/matrix7_contours.tsv', 
     counts, 
     delimiter='\t', 
     fmt="%.2f"
     )

# Display the image and plot all contours found
fig, ax = plt.subplots()
ax.imshow(closing, cmap=plt.cm.gray)


i=0
for contour in contours:
  if(contour.shape[0] > 13): 
    ax.plot(contour[:, 1], contour[:, 0], linewidth=2)
    i += 1
    print(contour.shape[0])
  else: continue
    # ax.plot(contour[:, 0, 0], contour[:, 0, 1], linewidth=2)

print(i)
print('n. of contours: '+str(len(contours)))

ax.axis('image')
ax.set_xticks([])
ax.set_yticks([])
plt.show()

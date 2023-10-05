# Dependencies
import cv2
import numpy as np
# Builtins
from math import atan2, tan, pi
import sys

print("Loading OpenCV... ", end="")
sys.stdout.flush()
import cv2
print(f"version {cv2.__version__} loaded.")

print("Loading image and converting colorspaces...", end="")
sys.stdout.flush()
img = cv2.imread("red.png")
# In OpenCV we work with BGR for historical reasons
img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
# But for processing we want to use the L*a*b* colorspace
lab = cv2.cvtColor(img, cv2.COLOR_BGR2Lab)
print("done.")

print("Filtering in L*a*b* colorspace...", end="")
sys.stdout.flush()
# We want to filter for the red color of the cones
# We can do a pretty good job of this since the a*
# axis of the L*a*b* colorspace tells you how red
# (or green) something is
COLOR_FILTER_LO = np.array([50, 160, 0])
COLOR_FILTER_HI = np.array([90, 255, 255])
mask = cv2.inRange(lab, COLOR_FILTER_LO, COLOR_FILTER_HI)
print("done.")

print("Performing morphological operations...", end="")
sys.stdout.flush()
# Now, we need to "open" the mask to remove any
# speckle-like noise
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
# Then we'll dilate it to make all the features larger and more uniform
mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, np.ones((5, 5), np.uint8))
print("done.")

print("Iterating through pixels to find tops of cones...", end="")
sys.stdout.flush()
# First, we'll create an array to keep track
# fo the row above the one we're currently working
# with
row_size = mask[0].size
row_above = np.zeros(row_size, dtype=np.bool_)
# Of course, we'll need to keep track of the locations
# of the tips of the cones too, since that's the whole
# point of this segment
cones = []
# Now, we're going to loop through each row
for row_i, row in enumerate(mask):
    # Now we need to keep track of whether we've seen
    # a set pixel to the left of us or not (this is
    # kind of like the column analog of row_above)
    set_before = False
    # We'll also need to keep track of whether we've
    # rejected the fact that this is a new cone, which
    # occurs when it matches up with a set pixel above
    reject_new = False
    # Now, we'll loop through every index in the row
    for i in range(row_size):
        if row[i] and not set_before:
            # We found what might be the start of a
            # new cone
            set_before = True
            reject_new = False
        if set_before and row[i] and row_above[i] and not reject_new:
            # Never mind, the potential cone exists
            # above us and is one we've already seen
            reject_new = True
        elif set_before and not row[i]:
            # We found the end of a possibly new cone
            set_before = False
            if not reject_new:
                # We found the end of a truly new cone
                cones.append((i, row_i))
    # Don't forget to update row_above
    row_above = row
print("done.")

print("Connecting cones to nearest neighbors...", end="")
sys.stdout.flush()
min_allowed_dist = 50
max_sqdist = (img.shape[0] ** 2) + (img.shape[1] ** 2)
angles, points = [], []
cones_not_taken = list(range(len(cones)))
for cone in cones:
    best_sqdist, best_i = max_sqdist, None
    for other_i_in_cones_not_taken, other_i in enumerate(cones_not_taken):
        other_cone = cones[other_i]
        sqdist = 0
        sqdist += (cone[0] - other_cone[0]) ** 2
        sqdist += (cone[1] - other_cone[1]) ** 2
        if sqdist < best_sqdist and sqdist > (min_allowed_dist ** 2):
            best_sqdist = sqdist
            best_i = other_i
    #cones_not_taken.pop(other_i_in_cones_not_taken)
    other_cone = cones[best_i]
    angles.append(atan2(
        (cone[1] - other_cone[1]),
        (cone[0] - other_cone[0]),
    ) % pi)
    points.append(cone)
print("done.")

print("Computing final lines and drawing them...", end="")
sys.stdout.flush()
# Now, we just need to split these into the
# left and right sides, which have angles
# less than and greater than pi/2
# respectively
# Then, we'll find the mean angle and the
# mean point
# Finally, we'll use this to draw our line
final_img = img.copy()
def draw_regression_line(points, angles, indices):
    mean_x, mean_y, mean_theta = 0, 0, 0
    for i in indices:
        mean_x     += points[i][0]
        mean_y     += points[i][1]
        mean_theta += angles[i]
    mean_x, mean_y, mean_theta = mean_x / len(indices), mean_y / len(indices), mean_theta / len(indices)
    slope = tan(mean_theta)
    start_t, end_t = -1000, 1000
    start = (mean_x + start_t, mean_y + (start_t * slope))
    start = (int(start[0]), int(start[1]))
    end = (mean_x + end_t, mean_y + (end_t * slope))
    end = (int(end[0]), int(end[1]))
    cv2.line(final_img, start, end, (255, 0, 0), 5)
draw_regression_line(points, angles, [ i for i, theta in enumerate(angles) if theta >  (pi / 2) ])
draw_regression_line(points, angles, [ i for i, theta in enumerate(angles) if theta <= (pi / 2) ])
print("done.")

print("Saving final image (as `my_answer.png`)...", end="")
sys.stdout.flush()
final_img_cvt = cv2.cvtColor(final_img, cv2.COLOR_BGR2RGB)
cv2.imwrite("my_answer.png", final_img_cvt)
print("done.")

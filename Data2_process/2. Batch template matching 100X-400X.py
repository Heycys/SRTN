import cv2
import numpy as np
import os

# Path to the 400X image
img_400X_path = "E:/breast/400X/SOB_B_A-14-22549AB-400-013.png"
# Directory containing 100X images
img_100X_dir = "E:/breast/100X/"

# Read the 400X image as a template
img_400X = cv2.imread(img_400X_path)  # Read the color image
img_400X_gray = cv2.imread(img_400X_path, cv2.IMREAD_GRAYSCALE)  # Read the grayscale image

# Resize the 400X image to 175x115 to use as a filter
filter = cv2.resize(img_400X_gray, (175, 115))

# Set the matching threshold
threshold = 0.95

for filename in os.listdir(img_100X_dir):
    img_100X_path = os.path.join(img_100X_dir, filename)

    img_100X = cv2.imread(img_100X_path)  # Read the color image
    img_100X_gray = cv2.cvtColor(img_100X, cv2.COLOR_BGR2GRAY)  # Convert to grayscale

    # Slide the filter over the 100X image and calculate the match with the filter for each region
    match_result = cv2.matchTemplate(img_100X_gray, filter, cv2.TM_CCOEFF_NORMED)

    # Find the position with the highest match
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match_result)

    # Stop searching when a match above the threshold is found
    if max_val > threshold:
        # Calculate the position of the matching region
        top_left = max_loc  # Top-left corner
        bottom_right = (top_left[0] + 175, top_left[1] + 115)  # Bottom-right corner

        # Crop the matching region
        img_100X_cropped = img_100X[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

        # Save the cropped matching region to the specified path
        cropped_path = "E:/breast/feature matching/LR/{}.png".format(os.path.splitext(filename)[0])
        cv2.imwrite(cropped_path, img_100X_cropped)

        # Save the original template to the specified path
        new_path = "E:/breast/feature matching/HR/{}.png".format(os.path.splitext(os.path.basename(img_400X_path))[0])
        cv2.imwrite(new_path, img_400X)  # Save the color image

        # Stop searching
        break

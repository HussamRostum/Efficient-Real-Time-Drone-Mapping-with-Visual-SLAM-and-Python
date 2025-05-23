import cv2
import numpy as np

# Load images
img1 = cv2.imread('map11.png', cv2.IMREAD_GRAYSCALE)  # Black map
img2 = cv2.imread('Picture1.png', cv2.IMREAD_GRAYSCALE)  # Map with green path and red walls

# ORB detector
orb = cv2.ORB_create()

# Find keypoints and descriptors
kp1, des1 = orb.detectAndCompute(img1, None)
kp2, des2 = orb.detectAndCompute(img2, None)

# Brute Force matcher with Hamming distance
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
matches = bf.match(des1, des2)

# Sort matches by distance (lower is better)
matches = sorted(matches, key=lambda x: x.distance)

# Accuracy estimate (arbitrary logic: good if distance < 50)
good_matches = [m for m in matches if m.distance < 50]
accuracy = (len(good_matches) / len(matches)) * 100 if matches else 0

# Draw matches
matched_image = cv2.drawMatches(img1, kp1, img2, kp2, good_matches, None, flags=2)

# Save or display results
cv2.imwrite('orb_matched_result.png', matched_image)
print(f"Matching Accuracy: {accuracy:.2f}%")

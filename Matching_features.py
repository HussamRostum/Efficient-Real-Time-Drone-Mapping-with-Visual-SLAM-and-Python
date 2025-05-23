import cv2
import numpy as np

# Load the image

image_1 = cv2.imread('img1.jpg')
image_2 = cv2.imread('img2.jpg')

medium_size = (500, 400)
image_1 = cv2.resize(image_1, medium_size)
image_2 = cv2.resize(image_2, medium_size)



#this cod for testing
# combined_image = np.hstack((image_1, image_2 ))
# cv2.imshow('test', combined_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

orb = cv2.ORB_create(nfeatures=1000)
keypoints1, descriptors1 = orb.detectAndCompute(image_1, None)
keypoints2, descriptors2 = orb.detectAndCompute(image_2, None)
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
matches = bf.match(descriptors1, descriptors2)
matches = sorted(matches, key=lambda x: x.distance)

matched_image = cv2.drawMatches(image_1, keypoints1, image_2, keypoints2, matches[:100],None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
cv2.namedWindow('Matches')
cv2.imshow("Matches",matched_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

import cv2

# Load the input video
input_path = '21.mp4'  # Change to your actual video path
cap = cv2.VideoCapture(input_path)

# Get video properties
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4
out = cv2.VideoWriter('orb_output_video.mp4', fourcc, fps, (frame_width, frame_height))

# Create ORB detector
orb = cv2.ORB_create()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to grayscale for ORB
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect ORB keypoints
    keypoints = orb.detect(gray, None)

    # Draw keypoints
    frame_with_keypoints = cv2.drawKeypoints(frame, keypoints, None, color=(0, 255, 0), flags=0)

    # Write the frame
    out.write(frame_with_keypoints)

# Release everything
cap.release()
out.release()
cv2.destroyAllWindows()

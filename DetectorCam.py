import cv2

# Initialize the webcam (0 is usually the default camera)
cap = cv2.VideoCapture(0)
ret, frame1 = cap.read()  # Read a frame from the webcam
ret, frame2 = cap.read()  # Read another frame for comparison

while cap.isOpened():  # Loop until the webcam is closed
    # Calculate the absolute difference between the two frames
    diff = cv2.absdiff(frame1, frame2)
    # Convert the difference to grayscale
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    # Apply Gaussian blur to reduce noise
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # Apply thresholding to get a binary image
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    # Dilate the thresholded image to fill in gaps
    dilated = cv2.dilate(thresh, None, iterations=3)
    # Find contours in the dilated image
    contours, _ = cv2.findContours(
        dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:  # Loop through each contour found
        if cv2.contourArea(contour) < 500:  # Ignore small contours (noise)
            continue
        # Get the bounding box for the contour
        x, y, w, h = cv2.boundingRect(contour)
        # Draw a rectangle around the detected motion
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("feed", frame1)  # Display the frame with detected motion

    frame1 = frame2  # Update frame1 to be the previous frame
    ret, frame2 = cap.read()  # Read a new frame for comparison

    if cv2.waitKey(40) == 27:  # Wait for the 'Esc' key to exit
        break

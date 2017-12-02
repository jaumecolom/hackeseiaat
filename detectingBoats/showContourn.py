#REFERENCE: http://www.pyimagesearch.com/2015/05/04/target-acquired-finding-targets-in-drone-and-quadcopter-video-streams-using-python-and-opencv/

# What does this code?
#Finally, the code detects all the structure with green margins or similars,
#with a polygonal shape and a minimum dimensions. Once detected,contourns are
#plotted to objects that fit on the filter and image momentum is computed.
#Is it possible to use this main code with simple images or with the webcam

#What is the main code objective?
#Is a first approach into detecting obstacles in real time for a drone, focused
#in locate objectives or doors to go through.

# import the necessary packages
import cv2
import numpy as np
import imutils
import time

camera = cv2.VideoCapture("boat33.mp4")
counter = 0
# keep looping
while True:
	#grabbed tells us if a frame has been detected by the webCam.
	#Frame is the image generated by the webCam at each moment
	(grabbed, frame) = camera.read()
	status = "Not detected"

	# Uncomment this line to use an image instead of a webCam
	# frame = cv2.imread('../IMG-20170511-WA0017.jpg')

	#If the frames stop appearing, this would stop the program
	if not grabbed:
		break


	# convert the frame to grayscale, blur it, and detect edges
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	hsv_test = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	blurred = cv2.GaussianBlur(gray, (7, 7), 0)
	edged = cv2.Canny(blurred, 50, 150)

	#copy the original frame to modify the copy with filters
	ShapMaskFrame = frame.copy();
	# pass BGR to HSV
	ShapMaskFrame = cv2.cvtColor(ShapMaskFrame, cv2.COLOR_BGR2HSV)


    # HSV color filter
	color = 50; #white
	sensitivity = 50
	lower = np.array([color - sensitivity, 0, 100])
	upper = np.array([color + sensitivity, 255, 255])
	# first we filter the color
	shapeMask = cv2.inRange(ShapMaskFrame, lower, upper)
	#shapeMask is a black frame with only white pixels that satisfy the filter
	#conditions imposed on the cv2.inRange function
	#We look for all the countours of the shapeMask, all the margins of the
	#color range selected
	(_,cnts, _) = cv2.findContours(shapeMask.copy(), cv2.RETR_EXTERNAL,
								cv2.CHAIN_APPROX_SIMPLE)

	#----------------------------------------------------------------

	# loop over the contours
	for c in cnts:
		t = time.time()
		# approximate the contour
		peri = cv2.arcLength(c, True)
		#approximate slopes to straight line polygons
		approx = cv2.approxPolyDP(c, 0.005 * peri, True)
		#print(len(approx))
		#approx is an array, inside there is the value for each of the segments
		#that conform the polygons
		if len(approx) >= 2 and len(approx) <= 300:
			#We find dimensions and coordinates of the segments that form  each
			#of the polygons that we located with the color filter
			(x, y, w, h) = cv2.boundingRect(approx)
			#we use the aspectRatio as a geometrical condition to erase unwanted
			#polygons
			aspectRatio = float(h) / float(w)

			keepDims = w > 70  and h > 200 #set a minimum size for the object
			#guarantee that is "squared" or a rod shape
			keepAspectRatio = aspectRatio >= 0.7 and aspectRatio <= 10

			# we will only plot the polygons that fit on the geometrical and
			#color conditions
			if keepDims and keepAspectRatio :
				# draw an outline around the target and update the status
				# text
				cv2.drawContours(frame, [approx], -1, (0, 0, 255), 4)
				status = "Boat(s) detected"

				if status == "Boat(s) detected":
					counter = counter + 1
					if counter >= 60:
						print('true')
				else:
					counter = 0

				# compute the center of the contour ploted on the image. Also,
				# refered as image moment, and plot it on the image.
				M = cv2.moments(approx)
				(cX, cY) = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
				(startX, endX) = (int(cX - (w * 0.15)), int(cX + (w * 0.15)))
				(startY, endY) = (int(cY - (h * 0.15)), int(cY + (h * 0.15)))
				cv2.line(frame, (startX, cY), (endX, cY), (0, 0, 255), 3)
				cv2.line(frame, (cX, startY), (cX, endY), (0, 0, 255), 3)


	# draw the status text on the frame
	cv2.putText(frame, status, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
		(0, 0, 255), 2)
	#Show the edited video
	cv2.imshow("Frame", frame)
	#cv2.imshow("Test", shapeMask)
	#cv2.imshow("Test2", hsv_test)

	# if the 'q' key is pressed, stop the loop
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()

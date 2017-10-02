import numpy as np
import cv2
from musicSelector import loadNewSong

def getMovementHistory(movementBuffer):
	firstFrame = movementBuffer[0]
	historyFrame = firstFrame - firstFrame

	#thresh = cv2.dilate(thresh, None, iterations=2)

	for i in range(1, len(movementBuffer)-1):
		frameDelta = cv2.absdiff(firstFrame, movementBuffer[i])
		thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
		historyFrame += thresh * i
	
	cv2.imshow('frame', historyFrame)
	return (cv2.countNonZero(historyFrame), historyFrame.mean())


def collectionSequence(frameBufferSize, iterations):
	movementBuffer = [None] * frameBufferSize
	counter = 0
	intensityValues = []
	quantityValues = []

	#iterations describes the number of data points a user wants to capture. frameBufferSize is the number of frames for one data point, so multiply to find the total number of frames that have to be run through
	for i in range(0, frameBufferSize*iterations):
		# Capture frame-by-frame
	    	ret, frame = cap.read()
		# Our operations on the frame come here
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		movementBuffer[counter] = gray
	
		counter+=1
		if counter >= len(movementBuffer):
			quant, intensity = getMovementHistory(movementBuffer)
			quantityValues.append(quant)
			intensityValues.append(intensity)

			counter = 0
		# Display the resulting frame
		#cv2.imshow('frame',gray)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	
	return (quantityValues, intensityValues)

def runTrainingSequence(emotions, bufferSize, trainingSize):
	lowPercent = 25
	highPercent = 75
	emotionMap = {}
	for emotion in emotions:
		print emotion

		rawValues = collectionSequence(bufferSize, trainingSize)
		quantValues = np.array(rawValues[0])
		intensityValues = np.array(rawValues[1])

		lowQuant = np.percentile(quantValues, lowPercent)
		highQuant = np.percentile(quantValues, highPercent)
		lowIntensity = np.percentile(intensityValues, lowPercent)
		highIntensity = np.percentile(intensityValues, highPercent)	

		emotionMap[emotion] = (lowQuant, highQuant, lowIntensity, highIntensity)
		print "Low Quant: " + str(lowQuant) + "\nHigh Quant: " + str(highQuant) + "\nlow Intensity: " + str(lowIntensity) + "\nHigh Intensity:" + str(highIntensity)

	return emotionMap

def findDanceEmotion(emotionMap, quant, intensity):
	for emotion, emotionVals in emotionMap.iteritems():
		if quant > emotionVals[0] and quant < emotionVals[1] and intensity > emotionVals[2] and intensity < emotionVals[3]:
			return emotion

	return None

def allBufferSame(buff):
	 return all(x == buff[0] for x in buff)

cap = cv2.VideoCapture(0)
if cap.isOpened():
	print("Webcam online.")
else:
	print("Webcam not connected")
	exit()

emotionMap = runTrainingSequence(["still", "excitment", "anger", "inspired"], 10, 40)
changeBuffer = [None] * 5
movementBuffer = [None] * 10
previousEmotion = None
counter = 0
while(True):
	# Capture frame-by-frame
    	ret, frame = cap.read()
	# Our operations on the frame come here
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	movementBuffer[counter] = gray

	counter+=1
	if counter >= len(movementBuffer):
		quant, intensity = getMovementHistory(movementBuffer)
		currentEmotion = findDanceEmotion(emotionMap, quant, intensity)
		#print currentEmotion + " | " + str( (quant, intensity) )	

		changeBuffer.append(currentEmotion)
		changeBuffer.pop(0)

		if allBufferSame(changeBuffer) and changeBuffer[0] != previousEmotion:
			previousEmotion = changeBuffer[0]
			if previousEmotion != None:
				print previousEmotion
				loadNewSong(previousEmotion)
		#print changeBuffer

		counter = 0
	# Display the resulting frame
	#cv2.imshow('frame',gray)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()



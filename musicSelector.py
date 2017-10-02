from pygame import mixer 
import time

def loadNewSong(emotion):
	if emotion == "still":
		mixer.music.stop()
	else:
		song = fileMap[emotion][0]
		mixer.music.load(musicFolderLoc+song)
		mixer.music.play()

fileMap = {
		"excitment" : ["Electric_Daisy.ogg"],
		"anger" : ["Massachusetts.ogg"],
		"inspired" : ["Angel.ogg"]
	}
musicFolderLoc = "/home/diego/Music/"

mixer.init()



import sys
import imageio
imageio.plugins.ffmpeg.download()
import moviepy.editor as mp
import requests
import speech_recognition as sr

# Create audio file from video
recognizer = sr.Recognizer()
inputfile = sys.argv[1]
clip = mp.VideoFileClip(inputfile)
fasterclip = clip.speedx(factor=1.25)
tempstart = 500
while tempstart < fasterclip.duration:
    tempend = tempstart + 30
    newclip = clip.subclip(t_start=tempstart,t_end=tempend)
    newclip.audio.write_audiofile("test.wav")
    with sr.AudioFile("test.wav") as source:
        audio = recognizer.record(source)
        print (recognizer.recognize_google(audio))
    tempstart = tempstart + 14

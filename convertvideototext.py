import imageio
imageio.plugins.ffmpeg.download()
import os
import sys
import moviepy.editor as mp
from pydub import AudioSegment
import audiotools
from google.cloud import storage
from google.cloud import speech

# Create wav file from video
INPUTFILE = sys.argv[1]
BASEFILENAME = os.path.splitext(INPUTFILE)[0]
WAVFILENAME = BASEFILENAME + ".wav"
FLACFILENAME = BASEFILENAME + ".flac"
TEXTFILENAME = BASEFILENAME + ".txt"
clip = mp.VideoFileClip(INPUTFILE)
clip.audio.write_audiofile(WAVFILENAME)
# This stuff was here for testing purposes and is not needed
# newclip = clip.subclip(100,200)
clip.audio.write_audiofile(WAVFILENAME)

# Convert to mono because Google Cloud Speech needs it to be mono
print("Converting file to mono FLAC...")
mysound = AudioSegment.from_wav(WAVFILENAME)
mysound = mysound.set_channels(1)
mysound.export(WAVFILENAME, format = "wav")

# Convert wav to FLAC
audiotools.open(WAVFILENAME).convert(
    FLACFILENAME,
    audiotools.FlacAudio,
    audiotools.DEFAULT_QUALITY)
SAMPLERATE =  audiotools.open(FLACFILENAME).sample_rate() # We're using this later

# Upload the file to a Google Cloud Storage bucket because you have to for
# files over like a minute
GOOGLE_APPLICATION_CREDENTIALS = {
  "type": "service_account",
  "project_id": "atomic-graph-183417",
  "private_key_id": "afb44277e98a11eea5cc16fb7544f91dc6fa9004",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDQuq3WYoZq9YW4\nuDUxtTb5qL3M0wWP6e707eSVo1aKLMf3+ccSwXuP7F4/BZXQEfp7HHWDvRg2cB//\nhpLZVwmjd7VhoqSQamW5ZgOi1vo8tpM6CZo2X3R3N58BVQaA+vr4amieA2aFx13J\nZ0YeWNvOIDmu1ePr7foLevKsJjMjkA0Z4qJWNiBUk+dfJvthShzYzd7X/8Fa+vPM\nNal9CAytdktfVMDa7xBVkYKAAPjw7sJS1lp3EGBeLy6k2ELOc+K/2zEJVpbDfZNx\n9b/8azU3YR+uMZ8RigeLQfjhTnyaluqfeOjTj5o4slo5eOSD1f78xfanbnaP2HIw\n5stb70sNAgMBAAECggEAUk2BtTqFORCVyTftVavYQQotyOFeXJhH7lENZImS2on8\n0YUuX3FmWOJBaUU5BOHJ7BhVJ/x8Wx7MJzP3nHZq6QePQC/jBsTFVpzoiyGMazss\ng2J86bqq0EVgz6Qom9wa8K/4j3HUz6REkWFE7ztndHgVdqCFLibYhQVWQdYQLRFu\nFoRYzQzqZAcquBv+b5w838aunPJR604ogil4I3uflsr1QeL9ACwYB4a/A/uriWwI\nqnqWsiVSMRzNbRxox9YPNZsYxYC44neB8pNcTm3YgHZeW9n4E9fKuZ3GSJ5y2OHe\ndLR3xigwmhndn+LHyXDq9d8vwSp7YmOf/BOwVMOPywKBgQDs/sqTio4NmVRgg5j/\nD4jJMKjYZpZc+ry73KYc1ToJJ1JYwfB/xaUpeae+c/2gbuh/quasJpUyiiHEw2Ze\nw2+X5O4P6NK3dwBcniwT4Y7FBCRi3C72vqbmYpewjnVo7D2Wmj+eh4wXU+s9mthE\nMVZV34luXG2fwo9Eka4VQjk5wwKBgQDhd58rholS5tJPQ6pVL1uhnH0wh5pfEx/w\n5IzB/OO0FEs/GY7N0F9zlJA/9e869K1aa/MY0TyDBnjJCfCEb/7q6yZx52x76NSQ\n5E8QqdSybqhywcAgODhYTzs55peFSTnJkNeql57uun30ZYWor6chFuoksvC+0cX/\nOkRkXfBK7wKBgB7tALJQGklcAM63XXerJ0ZZuy7B9E0dyxMYr/SDPpeDMhOy+xcx\nS2QmI+WObUJKNryyKHe+cSmvLMjoVqt3BVDk5svcreKS/NEZMtdFT8QVzkm4Qcih\nCFZ39yNq85dFfKPybOra9UT2BnR7iE0dww5hpSVpmkSGtvtTp0vO4HjRAoGAThFB\nR6zZt568iz1+qOgw7hBlOHx7cxgIIzy/kBukLCIqu7p5u8G+iyKRn9Pj9aHqtDhU\nf+9S6HtBLzsF0JWGyoiJUz8yTOUdVN34kmh7gRzXroRvpbhRqiIk+7NgG4JzQ9un\nESZWnYptOkY8tV+8mrR4diSPP0MbL3hZXfc40HkCgYEAii7EUP4aehey6TqD4ZGV\n57bo5kyuNZWH+PnviPvUm38VZc/n0Ka4niLaaY2R2mhGHsvZcHFPFlJ+aN/46zkm\n1NR3DiiuG4ojZcHxvoX+WWh5DyGHhtg1MVeKKxqHwn85LYF6vH1Ghkkgkt7m6v+E\nkI3cJRFAbm1El1SHkb3mGDc=\n-----END PRIVATE KEY-----\n",
  "client_email": "lecturetotext@atomic-graph-183417.iam.gserviceaccount.com",
  "client_id": "117014652722365002528",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://accounts.google.com/o/oauth2/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/lecturetotext%40atomic-graph-183417.iam.gserviceaccount.com"
}
storage_client = storage.Client('atomic-graph-183417')
bucket_name = 'atomic-graph-183417'
print("Uploading to Google Cloud Storage...")
try:
    bucket = storage_client.create_bucket(bucket_name)
except Exception:
    # If the bucket is already made
    bucket = storage_client.get_bucket(bucket_name)
blob = bucket.blob(FLACFILENAME)
blob.upload_from_filename(FLACFILENAME)
FILE_URI = "gs://" + bucket_name + "/" + FLACFILENAME

# Use Google Cloud Speech to transcribe text
client = speech.SpeechClient()
operation = client.long_running_recognize(
    audio = speech.types.RecognitionAudio(uri = FILE_URI),
    config = speech.types.RecognitionConfig(
        encoding = 'FLAC',
        language_code = 'en-US',
        sample_rate_hertz = SAMPLERATE,
        enable_word_time_offsets = True
    ),
)
print('Waiting for transcribing operation to complete...')
response = operation.result(timeout=99999)

# Once the text is transcribed write it to a file with minute timestamps
textfile = open(TEXTFILENAME,"w+")
minutecounter = 0
print("0 minutes\n\n")
textfile.write("0 minutes\n\n")
# Each result is for a consecutive portion of the audio. Iterate through
# them to get the transcripts for the entire audio file.
for result in response.results:
    try:
        seconds = int(result.alternatives[0].words[1].start_time.seconds)
        minutes = seconds/60
        if(minutes != minutecounter):
            print("\n\n" + str(minutes) + " minutes " + "\n\n")
            textfile.write("\n\n" + str(minutes) + " minutes " + "\n\n")
            minutecounter = minutes
    except Exception,e:
        print(e.message)
    print('Transcript: {}'.format(result.alternatives[0].transcript))
    textfile.write(result.alternatives[0].transcript)
textfile.close()

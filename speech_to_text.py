#  use multi lingual models (large v2)
import whisper
model= whisper.load_model("large-v2")

result= model.transcribe(audio="audios/2_Exercise 2_ Good Morning Sir.mp3",
                         language="hi",
                         task="transcribe",
                         word_timestamps=False)

print(result)
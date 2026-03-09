import whisper
# import json
import os

model = whisper.load_model("large-v2")

audio_folder = "audios"
output_folder = "json"

os.makedirs(output_folder, exist_ok=True)

audios = os.listdir(audio_folder)

for file in audios:

    if file.endswith(".mp3") and "_" in file:

        filename = file.replace(".mp3", "")
        number, title = filename.split("_", 1)

        print(number, title)

        audio_path = os.path.join(audio_folder, file)

        result = model.transcribe(
            audio=audio_path,
            language="hi",
            task="translate",
        )

        chunks = []

        for segment in result["segments"]:
            chunks.append({
                "number": number,
                "title": title,
                "start": segment["start"],
                "end": segment["end"],
                "text": segment["text"]
            })

        data = {
            "chunks": chunks,
            "full_text": result["text"]
        }

        # with open(f"{output_folder}/{filename}.json", "w", encoding="utf-8") as f:
            # json.dump(data, f, ensure_ascii=False, indent=2)

# print("PROCESS COMPLETED SUCCESSFULLY ")
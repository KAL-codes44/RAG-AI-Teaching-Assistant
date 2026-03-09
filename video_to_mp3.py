import os
import re
import subprocess
files = os.listdir("videos")
# print(files)
for file in files:
    # print(file)
    # tutorial_num= file.split("")
    number = re.search(r'\d+', file).group()
    
    name = file.split("_ Python Tutorial")[0].strip()
    # print(name , number)
    subprocess.run(["ffmpeg", "-i", f"videos/{file}", f"audios/{number}_{name}.mp3"])
    
print("completed PROCESS")
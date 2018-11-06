import json
from urllib import request as ur

def hit_api(outline):
    raw = ur.urlopen("http://www.conorstuartroe.com/lauvinko/gloss?outline=" + outline.replace(" ","_")).read()
    obj = json.loads(raw)
    if obj["status"] == "success":
        transcription = obj["gloss"]["transcription"]
        return " ".join(transcription)
    else:
        return "Failed, because: " + obj["reason"]

if __name__ == "__main__":
    while True:
        outline = input("Outline:  ")
        print(hit_api(outline))

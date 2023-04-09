import json
from gtts import gTTS
import os

class API_VO:
    settings = None
    settingsPath = f"{os.getcwd()}\\lib\\VoiceOver\\VOsettings.json"

    def __init__(self):
        self.auth()


    def auth(self):
        f = open(self.settingsPath, "r")
        self.settings = json.loads(f.read())
        f.close()


    def TextToMp3(self, text, filePath):
        txtToAu = gTTS(text)
        txtToAu.save(f"{filePath}")
        

if __name__ == "__main__":
    print("Testing VoiceOver.")
    tts = API_VO()
    tts.TextToMp3("This is some testing text, that should be spoken.", "TestTTS.wav")








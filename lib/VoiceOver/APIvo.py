import json
from TTS.api import TTS

class API_VO:
    settings = None
    settingsPath = "D:\\Users\\geosp\\Documents\\Code\\PY\\Projects\\InstaReel\\InstaReel\\lib\\VoiceOver\\VOsettings.json"
    tts = None


    def __init__(self):
        self.auth()


    def auth(self):
        f = open(self.settingsPath, "r")
        self.settings = json.loads(f.read())
        f.close()
        print(f"[VO] Initalising TTS model")
        model_name = TTS.list_models()[0]
        self.tts = TTS(model_name)
        print(f"[VO] TTS Model initalised.")


    def TTS_ToWAV(self, text, filePath):
        self.tts.tts_to_file(text=text, speaker=self.tts.speakers[0], language=self.tts.languages[0], file_path=filePath)


if __name__ == "__main__":
    print("Testing VoiceOver.")
    tts = API_VO()
    tts.TTS_ToWAV("This is some testing text, that should be spoken.", "TestTTS.wav")








import json
import os
import re
from datetime import datetime


class SessionHaldeler:
    DefaultSessionDirLocation = f"{os.getcwd()}\\Sessions\\"
    DefaultSessionName = "[Session]"
    DefaultJson = """{
    "SessionSeed": "",
    "State": "init",
    "Title": "",
    "Scripts": {
        "Raw": "",
        "Images": [],
        "PreProcessedScript": "",
        "ProcessedScript": "",
        "ProcessedScriptArray": []
    }
}"""

    Seed = ""
    dir = None
    settings = None
    stateError = None

    def __init__(self, seed = ""):
        # sanetise seed so its dir safe
        self.Seed = self._sanatiseSeed(seed)
        
        #  create a new session
        if (self.SessionExists()):
            self.LoadExistingSession()
        else:
            self.CreateNewSession()
        self.settings['SessionSeed'] = self.Seed
    

    def CreateNewSession(self):
        # create the session Dir
        self.dir = os.path.join(self.DefaultSessionDirLocation, f"{self.DefaultSessionName}{self.Seed}\\")
        os.mkdir(self.dir)

        # create the session json
        self.SyncSettings(self.DefaultJson)
    

    def LoadExistingSession(self):
        self.dir = os.path.join(self.DefaultSessionDirLocation, f"{self.DefaultSessionName}{self.Seed}\\")
        
        # self.CurrentSession_settings = json.loads(settingsJsonString)
        f = open( f"{self.dir}settings.json", "r")
        self.settings = json.loads(f.read()) 
        f.close()


    def SyncSettings(self, settingsJsonString = None):
        if (settingsJsonString == None):
            settingsJsonString = self.settings
        if (not isinstance(settingsJsonString, str)):
            settingsJsonString = json.dumps(settingsJsonString, indent=4)
        self.settings = json.loads(settingsJsonString)
        f = open(f"{self.dir}settings.json", "w")
        f.write(settingsJsonString)
        f.close()


    def SessionExists(self):
        self.Seed = self._sanatiseSeed(self.Seed)
        NewSession_Directory = os.path.join(self.DefaultSessionDirLocation, f"{self.DefaultSessionName}{self.Seed}\\")
        NewSession_SettingsPath = f"{NewSession_Directory}settings.json"

        if ( not os.path.isdir(NewSession_Directory) and not os.path.isfile(NewSession_SettingsPath)):
            # raise SessionNotFound(self.Seed, NewSession_Directory)
            return False
        return True


    def IntStateToString(self, s):
        STATE_DICTIONARY = {
            0: "initalised",                # Just initalised by the Session Handeler
            1: "postLoaded",                # Has beed loaded with an instagram post
            2: "preScriptFormat",           # Script data has been pre-formatted
            3: "scriptFinalised",           # Script has been finaised
            4: "voWaiting",                 # Waiting for voice over audio files
            5: "edit",                      # Ready to or being edited
            6: "render",                    # Ready to or being redered
            7: "complete",                  # Finished, ready to be deleted
            99: f"ERROR:{self.stateError}"  # Error occured at state    
        }
        return STATE_DICTIONARY[s]


    def HandelError(self):
        try:
            self.stateError = self.settings['State']
            self.settings['State'] = self.IntStateToString(99)
            print(f"[SessionHandeler] Error raised during state {self.stateError} '{self.IntStateToString(self.stateError)}'")
            self.SyncSettings(self.settings)
        except:
            print(f"[SessionHandeler] Could not set error state due to error.")
            raise


    def _sanatiseSeed(self, seed):
        if (seed == "" or seed == None):
            seed = f"NoSeedGiven-{datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S')}"
        else:
            seed = re.sub(r'\W+', '-', seed)
        return seed


# define Python user-defined exceptions
class SessionNotFound(Exception):
    "Raised when a sesion dir and or file cannot be found"
    def __init__(self, seed, dir):
        self.seed = seed
        self.dir = dir
        super().__init__(f"Could not find a local session with seed: {self.seed}. Directory or settings.json does not exist in: {self.dir}")


if __name__ == "__main__":
    # used to handel the creation nd maintenance of different sessions.
    print("Starting Session Handeler")

    # Create a new session
    sh = SessionHaldeler()








from moviepy.editor import *
import json
import os
import shutil

class ShortFormVideoEditor():

    """
    This is the high level video editor, that uses helper functions (lower level) from EditorUtils.py
    """
    settingsPath = "D:\\Users\\geosp\\Documents\\Code\\PY\\Projects\\InstaReel\\InstaReel\\lib\\Vid\\VideoSettings.json"
    ScriptInformation = None
    WorkSpacePath = None


    def __init__(self, workSpaceDirectory, ScriptInformation):
        # load the settings json
        f = open(self.settingsPath, "r")
        self.GPTSettings = json.loads(f.read())
        f.close()
        
        self.WorkSpacePath = workSpaceDirectory
        self.ScriptInformation = ScriptInformation


    # --- Pre-Processor functions for processing rushes ---

    def pre_AddToRushPool(self, recourcePath):
        # Move a resource to local 'workspace' folder (image, audio, or other)
        if (os.path.isfile(recourcePath)):
            dirDelimeter = "\\"
            if ("\\\\" in recourcePath):
                dirDelimeter = "\\\\"
            # put through splittext() first to avoid interpreting '.' chars dir names as extentions
            filename, file_extension = os.path.splitext(recourcePath)
            fileNameWithExtention = filename.split(dirDelimeter)[-1] + file_extension
            if(not os.path.isfile(f"{self.WorkSpacePath}\\RUSHES\\{fileNameWithExtention}")):
                shutil.copy2(recourcePath, f"{self.WorkSpacePath}\\RUSHES\\{fileNameWithExtention}")
        else:
            raise FileNotFoundError(f"Could not find file: {recourcePath}. Needs to be the full path to a file.")
        pass 
    
    # --- Processor functions for constructing clips ---

    def proc_ConstructClipSegment(self, ImageClip, VoAudio):
        
        pass


    def proc_Transition_SimpleFade(self, startingClip, endingClip):
        pass

    # --- Post-pProcessing functions for finishing touches ---

    def post_AddMusic(self, audioFile, volume = 0.6):
        pass

    # --- Rendering and saving fucntions ---

    def RenderToFile(self, clipArray):
        pass


if __name__ == "__main__":
    print("Testing VideoEditor.")

    f = open( f"D:\\Users\\geosp\\Documents\\Code\\PY\\Projects\\InstaReel\\InstaReel\\Sessions\\[Session]DEBUG\\settings.json", "r")
    settings = json.loads(f.read()) 
    f.close()

    wsdir = "D:\\Users\\geosp\\Documents\\Code\\PY\\Projects\\InstaReel\\InstaReel\\lib\\Vid\\TemporaryWorkspaceDirectory"
    
    editor = ShortFormVideoEditor(wsdir, settings)
    imgdir = "D:\\Users\\geosp\\Documents\\Code\\PY\\Projects\\InstaReel\\InstaReel\\Sessions\\[Session]DEBUG\\IMG"
    vodir = "D:\\Users\\geosp\\Documents\\Code\\PY\\Projects\\InstaReel\\InstaReel\\Sessions\\[Session]DEBUG\\VO"

    for filename in os.listdir(imgdir):
        f = os.path.join(imgdir, filename)
        editor.pre_AddToRushPool(f)

    for filename in os.listdir(vodir):
            f = os.path.join(vodir, filename)
            editor.pre_AddToRushPool(f)
    # editor.pre_CollectRushes()
    # editor.proc_ConstructClipSegment()
    # editor.proc_Transition_SimpleFade()
    # editor.post_AddMusic()
    # editor.RenderToFile()
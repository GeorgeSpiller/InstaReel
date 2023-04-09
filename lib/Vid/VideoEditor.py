from moviepy.editor import *
import json
import os
import shutil
from lib.Vid.EditorUtils import *
from moviepy.video.fx.fadein import fadein



class ShortFormVideoEditor():

    """
    This is the high level video editor, that uses helper functions (lower level) from EditorUtils.py
    """
    settingsPath = f"{os.getcwd()}\\lib\\Vid\\VideoSettings.json"
    settings = None
    ScriptInformation = None
    WorkSpacePath = None


    def __init__(self, ScriptInformation):
        # load the settings json
        f = open(self.settingsPath, "r")
        self.settings = json.loads(f.read())
        f.close()
        
        self.WorkSpacePath = f"{os.getcwd()}\\lib\\Vid\\Workspace"
        self.ScriptInformation = ScriptInformation


    def RunShortsEngine(self):
        clipSegments = self.proc_GenClipSegments()
        clipConcat = clipSegments[0]
        for i in range(1, len(clipSegments)-1):
            clipConcat = self.proc_Transition_SimpleFade(clipConcat, clipSegments[i])
        return clipConcat

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


    def proc_GenClipSegments(self):
        # loop through all clip segments where:
        # - a clip segment is a combonation of one VO audio file and one Image file, as
        #   denoted in the ScriptInformation dict.
        ClipSegments = []
        for i, clipSegmentLine in enumerate(self.ScriptInformation['Scripts']['ProcessedScriptArray']):
            ImageFilePath = f"{self.WorkSpacePath}\\RUSHES\\Image{int(clipSegmentLine[1:2])}.png"
            VOFilePath = f"{self.WorkSpacePath}\\RUSHES\\vo-{i}.mp3"
            # for each clip segment, create it using the Editor Utils and save it to rush pool
            if (os.path.isfile(ImageFilePath) and os.path.isfile(VOFilePath)):
                ClipSegments.append(proc_ConstructClipSegment(self.settings['clipSettings'], ImageFilePath, VOFilePath))
        return ClipSegments


    def proc_Transition_SimpleFade(self, startingClip, endingClip):
        return concatenate_videoclips([startingClip, startingClip])


    # --- Post-pProcessing functions for finishing touches ---


    def post_AddMusic(self, audioFile, volume = 0.6):
        pass


    # --- Rendering and saving fucntions ---


    def RenderToFile(self, clip):
        clip.write_videofile("temp.mp4")
        clip.close()


    def CleanWorkspace(self):
        for filename in os.listdir(self.WorkSpacePath):
            file_path = os.path.join(self.WorkSpacePath, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    if ('gitignore' in file_path):
                        continue
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))


if __name__ == "__main__":
    print("Testing VideoEditor.")

    f = open( f"{os.getcwd()}\\Sessions\\[Session]3072068653637051762\\settings.json", "r")
    settings = json.loads(f.read()) 
    f.close()

    # wsdir = f"{os.getcwd()}\\lib\\Vid\\TemporaryWorkspaceDirectory"
    
    editor = ShortFormVideoEditor(settings)
    imgdir = f"{os.getcwd()}\\Sessions\\[Session]3072068653637051762\\IMG"
    vodir = f"{os.getcwd()}\\Sessions\\[Session]3072068653637051762\\VO"

    for filename in os.listdir(imgdir):
        f = os.path.join(imgdir, filename)
        editor.pre_AddToRushPool(f)

    for filename in os.listdir(vodir):
            f = os.path.join(vodir, filename)
            editor.pre_AddToRushPool(f)

    editor.RunShortsEngine()
from Sessions.SessionHandler import *
from lib.GPT.APIGPT import API_GPT
from lib.Instagram.APInstagram import API_Instagram
import re
import requests


def RemoveHashtags(script):
    hashtags =  re.findall("#\w+", script)
    if ('#onthisday' in [x.lower() for x in hashtags]):
        i = [x.lower() for x in hashtags].index('#onthisday')
        del hashtags[i]
    for h in hashtags:
        script = script.replace(h, "")
    return script.strip()


def RemoveImageDescriptions(script, imageDescriptionList):
    for strImagDesc in imageDescriptionList:
        strImagDesc = re.sub("\d+:\W+", "", strImagDesc).strip()
        script = script.replace(strImagDesc.strip(), "")
    script = re.sub("\d+.\W+", "", script).strip()
    return script.strip()


def DownloadImageToDir(url, dir, ImageName):
    img_data = requests.get(url).content
    with open(f"{dir}\\{ImageName}.png", 'wb') as handler:
        handler.write(img_data)


def SuplimentImagesWithAiGeneratedImages(CurrentSession, gpt):
    scriptWordCount = len(CurrentSession.settings['Scripts']["PreProcessedScript"].split(" "))
    desiredWordsPerImage = int(CurrentSession.settings['ScriptWordsPerImage'])
    print(f"actualWordsPerImage ({scriptWordCount // len(CurrentSession.settings['Scripts']['Images'])} = {scriptWordCount} // {len(CurrentSession.settings['Scripts']['Images'])}")
    actualWordsPerImage = scriptWordCount // len(CurrentSession.settings['Scripts']["Images"])
    promptGenerationImageDescription = gpt.GPTSettings['prompts']['GetImageGenerationPrompt'].replace("<SCRIPT>", f"\"{CurrentSession.settings['Scripts']['PreProcessedScript']}\".")
    # if there are not enough images in the post to match wordsPerImage, generate more images
    while(actualWordsPerImage > desiredWordsPerImage):
        print(f" while({actualWordsPerImage} < {desiredWordsPerImage}):")
        imageDescription = gpt.CustomPrompt(promptGenerationImageDescription, "GetImageGenerationPrompt")
        url = gpt.GenerateImage(imageDescription)
        imgNumber = len(CurrentSession.settings['Scripts']["Images"])+1
        DownloadImageToDir(url, CurrentSession.imgDir, f"Image{imgNumber}")
        CurrentSession.settings['Scripts']["Images"].append(f"{imgNumber}: {imageDescription}")
        actualWordsPerImage = scriptWordCount // len(CurrentSession.settings['Scripts']["Images"])


def MainLoop():
    print("Starting.")

    # Create session
    CurrentSession = SessionHaldeler()
    stateInt = CurrentSession.StrStateToInt(CurrentSession.settings['State'])
    # init all the APIs
    gpt = API_GPT()
    insta = API_Instagram()
    try:
        while(stateInt != 7):
            print(f"[STATE] Current State ({stateInt}) '{CurrentSession.settings['State']}'")
            
            if (stateInt == 0):
                # Get Description using Instagram API
                insta.GetPostToProcess()
                ImageUrlList = insta.PostGet_Images()
                CurrentSession.settings['Scripts']['Raw'] = insta.PostGet_Description()
                # save images in order to local dir
                for i, imgUrl in enumerate(ImageUrlList):
                    DownloadImageToDir(imgUrl, CurrentSession.imgDir, f"Image{i}")

                CurrentSession.settings['State'] = CurrentSession.IntStateToString(stateInt + 1)
                CurrentSession.SyncSettings()
            
            elif (stateInt == 1):
                # get list of image descriptions that are present in the script
                Prompt_ImageDescriptions = gpt.GPTSettings["prompts"]["ImageDescriptions"].replace("<SCRIPT>", f"\"{CurrentSession.settings['Scripts']['Raw']}\".")
                GTPresp = gpt.CustomPrompt(Prompt_ImageDescriptions, "Prompt_ImageDescriptions")
                # get image descriptions
                imgDesc = [x for x in GTPresp.split('\n') if x != '']  
                # add image indexes to begining
                CurrentSession.settings['Scripts']["Images"].clear()
                for i, v in enumerate(imgDesc):
                    CurrentSession.settings['Scripts']["Images"].append(f"{i}: {v}")
                
                # Pre-script processing
                # remove all hashtags, except for the #OnThisDay. Remove all image descriptions.
                CurrentSession.settings['Scripts']["PreProcessedScript"]  = RemoveHashtags(CurrentSession.settings['Scripts']['Raw'])
                CurrentSession.settings['Scripts']["PreProcessedScript"]  = RemoveImageDescriptions(CurrentSession.settings['Scripts']["PreProcessedScript"] , CurrentSession.settings['Scripts']["Images"])
                
                # additinal AI generated images
                # Generate some supplimentry images if there are not many images to show. Generate based on script length
                if (int(CurrentSession.settings['SuplimentImagesWithAiGeneratedImages']) == 1):
                    SuplimentImagesWithAiGeneratedImages(CurrentSession, gpt)
                    
                CurrentSession.settings['State'] = CurrentSession.IntStateToString(stateInt + 1)
                CurrentSession.SyncSettings()

            elif (stateInt == 2):
                # Script finalising
                # insert images
                Prompt_InsertImage = gpt.GPTSettings["prompts"]["InsertImage"]
                Prompt_InsertImage = Prompt_InsertImage.replace("<SCRIPT>", f"\"{CurrentSession.settings['Scripts']['PreProcessedScript']}\".")
                Prompt_InsertImage = Prompt_InsertImage.replace("<IMAGES>", f"({'. '.join(CurrentSession.settings['Scripts']['Images'])})")
                CurrentSession.settings['Scripts']["ProcessedScript"] = gpt.CustomPrompt(Prompt_InsertImage, "Prompt_InsertImage")
                CurrentSession.settings['Scripts']["ProcessedScriptArray"] = re.split("\(\d+\)", CurrentSession.settings['Scripts']["ProcessedScript"])
                CurrentSession.settings['Scripts']["ProcessedScriptArray"] = [s.strip() for s in CurrentSession.settings['Scripts']["ProcessedScriptArray"] if s != ""]
                # get title
                Prompt_Title = gpt.GPTSettings["prompts"]["Title"]
                Prompt_Title = Prompt_Title.replace("<SCRIPT>", f"\"{CurrentSession.settings['Scripts']['PreProcessedScript']}\".")
                CurrentSession.settings['Title'] = gpt.CustomPrompt(Prompt_Title, "Prompt_Title")
                
                CurrentSession.settings['State'] = CurrentSession.IntStateToString(stateInt + 1)
                CurrentSession.SyncSettings()
                
            elif (stateInt == 3):
                # get VO
                if (os.path.isdir(CurrentSession.voDir)):
                    # count the number of files in this directory
                    numberOfVOFiles = len([entry for entry in os.listdir(CurrentSession.voDir) if os.path.isfile(os.path.join(CurrentSession.voDir, entry))])
                    if (numberOfVOFiles == len(CurrentSession.settings['Scripts']['ProcessedScriptArray'])):
                        print("VO's found")
                    else:
                        print(f"Not all VO's in dir {CurrentSession.voDir} were present. Expected {len(CurrentSession.settings['Scripts']['ProcessedScriptArray'])} files, found {numberOfVOFiles}.")
                
                CurrentSession.settings['State'] = CurrentSession.IntStateToString(stateInt + 1)
                CurrentSession.SyncSettings()

            elif (stateInt == 4):
                CurrentSession.settings['State'] = CurrentSession.IntStateToString(stateInt + 1)
                CurrentSession.SyncSettings()

            elif (stateInt == 5):
                CurrentSession.settings['State'] = CurrentSession.IntStateToString(stateInt + 1)
                CurrentSession.SyncSettings()

            elif (stateInt == 6):
                CurrentSession.settings['State'] = CurrentSession.IntStateToString(stateInt + 1)
                CurrentSession.SyncSettings()
            
            else:
                break
                
            stateInt = CurrentSession.StrStateToInt(CurrentSession.settings['State'])
        print("Processing complete.")
    except Exception as e:
        CurrentSession.HandelError()
        raise e




if __name__ == "__main__":
    MainLoop()
    # CurrentSession = SessionHaldeler("DEBUG-SESSION")
    # # init all the APIs
    # gpt = API_GPT()
    # p = gpt.GPTSettings['prompts']['GetImageGenerationPrompt'].replace("<SCRIPT>", f"\"{CurrentSession.settings['Scripts']['Raw']}\".")
    # print(gpt.GenerateImage(p))
from Sessions.SessionHandler import *
from lib.GPT.APIGPT import API_GPT
import re


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
        script = script.replace(strImagDesc.strip(), "")
    return script.strip()

if __name__ == "__main__":
    print("Starting.....")
    # Create session
    CurrentSession = SessionHaldeler("DEBUG-SESSION")
    try:
        # init all the APIs
        gpt = API_GPT()

        # Get Description using Instagram API
        # instead this is hard coded in the json for now
        CurrentSession.settings['State'] = CurrentSession.IntStateToString(1)

        # Pre-script processing
        # get list of image descripts that are present in the script
        Prompt_ImageDescriptions = gpt.GPTSettings["prompts"]["ImageDescriptions"].replace("<SCRIPT>", f"\"{CurrentSession.settings['Scripts']['Raw']}\".")
        GTPresp = gpt.CustomPrompt(Prompt_ImageDescriptions)
        CurrentSession.settings['Scripts']["Images"] = [x for x in GTPresp.split('\n') if x != '']
        # remove all hashtags, except for the #OnThisDay 
        CurrentSession.settings['Scripts']["PreProcessedScript"]  = RemoveHashtags(CurrentSession.settings['Scripts']['Raw'])
        CurrentSession.settings['Scripts']["PreProcessedScript"]  = RemoveImageDescriptions(CurrentSession.settings['Scripts']["PreProcessedScript"] , CurrentSession.settings['Scripts']["Images"])
        CurrentSession.SyncSettings()
        # pre formatting script finished, set state
        CurrentSession.settings['State'] = CurrentSession.IntStateToString(2)
        
        # Script finalising
        # insert images
        Prompt_InsertImage = gpt.GPTSettings["prompts"]["InsertImage"]
        Prompt_InsertImage = Prompt_InsertImage.replace("<SCRIPT>", f"\"{CurrentSession.settings['Scripts']['PreProcessedScript']}\".")
        Prompt_InsertImage = Prompt_InsertImage.replace("<IMAGES>", f"({'. '.join(CurrentSession.settings['Scripts']['Images'])})")
        CurrentSession.settings['Scripts']["ProcessedScript"] = gpt.CustomPrompt(Prompt_InsertImage)
        CurrentSession.settings['Scripts']["ProcessedScriptArray"] = re.split("\(\d+\)", CurrentSession.settings['Scripts']["ProcessedScript"])
        # get title
        Prompt_Title = gpt.GPTSettings["prompts"]["Title"]
        Prompt_Title = Prompt_Title.replace("<SCRIPT>", f"\"{CurrentSession.settings['Scripts']['PreProcessedScript']}\".")
        CurrentSession.settings['Ttile'] = gpt.CustomPrompt(Prompt_Title)
        CurrentSession.SyncSettings()
        CurrentSession.settings['State'] = CurrentSession.IntStateToString(3)

    except:
        CurrentSession.HandelError()
        raise


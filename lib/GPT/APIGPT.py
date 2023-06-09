import json 
import openai
import re
import os

class API_GPT():
    GPTSettings = None
    settingsPath = f"{os.getcwd()}\\lib\\GPT\\GPTsettings.json"

    def __init__(self):
        self.auth()


    def auth(self):
        f = open(self.settingsPath, "r")
        self.GPTSettings = json.loads(f.read())
        f.close()
        openai.api_key = self.GPTSettings["apiKey"]
        openai.organization = self.GPTSettings["orgId"]
    

    def CustomPrompt(self, PromptString, promptTag = None):
        if (promptTag == None):
            promptTag = PromptString[:80]

        print(f"[GPT] Sending prompt: {promptTag}...")
        response = openai.ChatCompletion.create(model=self.GPTSettings["model"], messages=[{"role": "user", "content": PromptString}])
        ans = response.choices[0].message.content
        print(f"[GPT] Response recieved.")
        return ans.strip().replace("\n", "").replace("\r", "")


    def FormatImageDescriptions(self, script):
        Prompt_ImageDescriptions = self.GPTSettings["prompts"]["ImageDescriptions"].replace("<SCRIPT>", f"\"{script}\".")
        return self.CustomPrompt(Prompt_ImageDescriptions, "Prompt_ImageDescriptions")
    

    def Prompt_ImageDescriptions(self, script, ImageFileNames):
        # get list of image descriptions that are present in the script
        GTPresp = self.FormatImageDescriptions(script)
        # split at all '#.' where # is a number. Assumes there are never more than 10 images
        imgDesc = [x for x in re.split("[^\d]\d\.", GTPresp) if x != '']

        if (len(imgDesc) == 1):
            raise Exception(f"GPT did not return image descriptions as a formattable list: {imgDesc}")
        
        # add image indexes to begining
        imageDescDict = {}
        if (len(imgDesc) > len(ImageFileNames)):
            print(f"[GPT] [Warning] Gave more image descriptions than there are images in the instagram post ({len(imgDesc)} > {len(ImageFileNames)}).")
        
        for i, v in enumerate(imgDesc):
            # Assumption here is: All image descriptions are in the order that the images appear in the post
            # imageDescList.append(f"{i}: {v}")
            imagePostIndex = i
            # Wrap around the image post index if GPT has given more image descriptions than there are images in the post
            if (imagePostIndex > len(ImageFileNames)):
                imagePostIndex = 0
            
            if(ImageFileNames[i] in imageDescDict):
                imageDescDict[ImageFileNames[i]] += v
            else:
                imageDescDict[ImageFileNames[i]] = v
        return imageDescDict


    def Prompt_InsertImage(self, script, images):
        Prompt_InsertImage = self.GPTSettings["prompts"]["InsertImage"]
        Prompt_InsertImage = Prompt_InsertImage.replace("<SCRIPT>", f"\"{script}\".")
        Prompt_InsertImage = Prompt_InsertImage.replace("<IMAGES>", f"({'. '.join(images.values())})")
        return self.CustomPrompt(Prompt_InsertImage, "Prompt_InsertImage")


    def Prompt_Title(self, script):
        Prompt_Title = self.GPTSettings["prompts"]["Title"]
        Prompt_Title = Prompt_Title.replace("<SCRIPT>", f"\"{script}\".")
        return self.CustomPrompt(Prompt_Title, "Prompt_Title")
                

    def GenerateImage(self, imageDescription):
        print(f"[DAL-E] Sending prompt: {imageDescription}...")
        response = openai.Image.create(prompt=imageDescription,n=1,size="512x512")
        imageUrl = (response["data"][0]["url"])
        print("[DAL-E] Response recieved. ")
        return imageUrl


if __name__ == "__main__":
    print("Testing GPT: Can we hear you?")

    gptapi = API_GPT()
    print(gptapi.GenerateImage("The letter 'A' in an epic high resolution detailed dramatic landscape."))
    # ans = gptapi.CustomPrompt("Hello, can you hear me GPT?")
    
    # print(ans)


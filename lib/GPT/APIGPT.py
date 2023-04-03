import json 
import openai

class API_GPT():
    GPTSettings = None
    settingsPath = "D:\\Users\\geosp\\Documents\\Code\\PY\\Projects\\InstaReel\\InstaReel\\lib\\GPT\\GPTsettings.json"

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


    def GenerateImage(self, imageDescription):
        print(f"[DAL-E] Sending prompt: {imageDescription}...")
        response = openai.Image.create(prompt=imageDescription,n=1,size="512x512")
        imageUrl = (response["data"][0]["url"])
        print("[DAL-E] Response recieved. ")
        return imageUrl


if __name__ == "__main__":
    print("Testing GPT: Can we hear you?")

    gptapi = API_GPT()
    ans = gptapi.CustomPrompt("Hello, can you hear me GPT?")
    
    print(ans)


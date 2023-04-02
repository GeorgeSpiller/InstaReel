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
        openai.api_key = self.GPTSettings["apiKey"]
        openai.organization = self.GPTSettings["orgId"]


    def CustomPrompt(self, PromptString):
        print(f"[GPT] Sending prompt: {PromptString[:80]}...")
        response = openai.Completion.create(engine = self.GPTSettings["engine"], prompt = PromptString, temperature = int(self.GPTSettings["temperature"]), max_tokens = int(self.GPTSettings["maxTokens"]))
        ans = response.choices[0].text
        print("[GPT] Response recieved.")
        return ans.strip()
    

if __name__ == "__main__":
    print("Testing GPT: Can we hear you?")

    gptapi = API_GPT()
    gptapi.CustomPrompt("Hello, can you hear me GPT?")



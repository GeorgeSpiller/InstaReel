import json 
import openai

class API_GPT():

    authKey = None
    temperature = None
    maxTokens = None
    engine = "text-davinci-003"

    def __init__(self):
        self.auth()

    def auth(self):
        f = open("D:\\Users\\geosp\\Documents\\Code\\PY\\Projects\\InstaReel\\InstaReel\\lib\\GPT\\GPTsettings.json", "r")
        GPTSettings = json.loads(f.read())
        self.authKey = GPTSettings["apiKey"]
        self.temperature = 0.6
        self.maxTokens = 2048
        openai.api_key = self.authKey


    def CustomPrompt(self, PromptString):
        response = openai.Completion.create(engine = self.engine, prompt = PromptString, temperature = self.temperature, max_tokens = self.maxTokens)
        print(response.choices[0].text)



if __name__ == "__main__":
    print("Can GPT hear you?")

    gptapi = API_GPT()
    gptapi.CustomPrompt("Hello, can you hear me GPT?")



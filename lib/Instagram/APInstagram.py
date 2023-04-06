from instagrapi import Client
import json

class API_Instagram:
    settings = None
    settingsPath = "D:\\Users\\geosp\\Documents\\Code\\PY\\Projects\\InstaReel\\InstaReel\\lib\\Instagram\\InstagramSettings.json"
    cl = None
    rawPostDict = None


    def __init__(self):
        self.auth()


    def auth(self):
        f = open(self.settingsPath, "r")
        self.settings = json.loads(f.read())
        f.close()
        print(f"[INSTAGRAM] Logging in as user: {self.settings['username']}")
        self.cl = Client()
        self.cl.login(self.settings['username'], self.settings['password'])
        print(f"[INSTAGRAM] Login successful.")


    def GetPostToProcess(self):
        url = "https://www.instagram.com/p/CqiLin5piVy/"# input("Enter the url of the post to process.\n>> ")
        print(f"[INSTAGRAM] Grabbing post data... HARDCODED URL")
        pk = self.cl.media_pk_from_url(url)
        self.rawPostDict = self.cl.media_info(pk).dict()
        print(f"[INSTAGRAM] Data for post recieved. ({pk})")
        return pk


    def PostGet_Description(self):
        return self.rawPostDict['caption_text']


    def PostGet_Images(self):
        urlListRaw = [r['thumbnail_url'] for r in self.rawPostDict['resources']]
        return [hurl.replace("HttpUrl('", "").replace("', )", "") for hurl in urlListRaw]



if __name__ == "__main__":
    print("Testing Instagram.")
    gram = API_Instagram()
    gram.GetPostToProcess()
    print(gram.PostGet_Description())
    print(gram.PostGet_Images())



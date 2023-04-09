from instagrapi import Client
import json
import os
import validators

class API_Instagram:
    settings = None
    settingsPath = f"{os.getcwd()}\\lib\\Instagram\\InstagramSettings.json"
    cl = None
    rawPostDict = None
    NullLoginDefaultSeed = None


    def __init__(self):
        self.auth()


    def auth(self):
        try:
            f = open(self.settingsPath, "r")
            self.settings = json.loads(f.read())
            f.close()
            print(f"[INSTAGRAM] Logging in as user: {self.settings['username']}. (Status 429 can be ignored).")
            self.cl = Client()
            self.cl.login(self.settings['username'], self.settings['password'])
            print(f"[INSTAGRAM] Login successful.")
        except AssertionError as ae:
            print(f"[INSTAGRAM] Failed to login as user {self.settings['username']}: {ae}")
            self.NullLoginDefaultSeed = input(F"[INSTAGRAM] Please enter an already loaded pk to use instead, or nothing to exit. >> ")
            if self.NullLoginDefaultSeed == "":
                exit()


    def GetPostToProcess(self):
        # if we could not login, the retrun the default seed of an already loaded post
        if (self.NullLoginDefaultSeed != None):
            return self.NullLoginDefaultSeed
        
        url = input("Enter the url of the post to process. Enter nothing to use hardcoded url\n>> ")
        if (not validators.url(url)):
            url = "https://www.instagram.com/p/CqsTGd-vlOi/"
        print(f"[INSTAGRAM] Grabbing post data...")
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



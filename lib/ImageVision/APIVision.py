import json
from array import array
import os
from PIL import Image
import sys
import time
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

class API_Vision:
    settingsPath = f"{os.getcwd()}\\lib\\ImageVision\\settings.json"
    computervision_client = None

    def __init__(self):
        self.auth()


    def auth(self):
        f = open(self.settingsPath, "r")
        self.settings = json.loads(f.read())
        f.close()
        print(f"[Vision] Auth...")
        key = self.settings['key']
        endpoint = self.settings['endpoint']
        self.computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(key))
        print(f"[Vision] successful.")

    def ImageToDescription(self, imagePath):
        features = [VisualFeatureTypes.description,
            VisualFeatureTypes.tags,
            VisualFeatureTypes.categories,
            VisualFeatureTypes.brands,
            VisualFeatureTypes.objects,
            VisualFeatureTypes.adult]
        # Open local image file
        with open(imagePath, mode="rb") as image_data:
            analysis = self.computervision_client.analyze_image_in_stream(image_data , features)
        
        for caption in analysis.description.captions:
            print("Description: '{}' (confidence: {:.2f}%)".format(caption.text, caption.confidence * 100))
        
        if (len(analysis.categories) > 0):
            print("Categories:")
            landmarks = []
            for category in analysis.categories:
                # Print the category
                print(" -'{}' (confidence: {:.2f}%)".format(category.name, category.score * 100))
                if category.detail:
                    # Get landmarks in this category
                    if category.detail.landmarks:
                        for landmark in category.detail.landmarks:
                            if landmark not in landmarks:
                                landmarks.append(landmark)

            # If there were landmarks, list them
            if len(landmarks) > 0:
                print("Landmarks:")
                for landmark in landmarks:
                    print(" -'{}' (confidence: {:.2f}%)".format(landmark.name, landmark.confidence * 100))

        # Get brands in the image
        if (len(analysis.brands) > 0):
            print("Brands: ")
            for brand in analysis.brands:
                print(" -'{}' (confidence: {:.2f}%)".format(brand.name, brand.confidence * 100))


if __name__ == "__main__":
    print("Testing VisionAPI.")
    v = API_Vision()
    v.ImageToDescription(f"{os.getcwd()}\\Sessions\\[Session]3072068653637051762\\IMG\\Image3.png")



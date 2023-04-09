import math
from moviepy.editor import *
from PIL import Image, ImageFilter 
import json
import os
import numpy


def proc_ConstructClipSegment(ClipSettings, ImageClipPath, VoAudio):
    print( f"[{os.path.basename(ImageClipPath).split('/')[-1]} + {os.path.basename(VoAudio).split('/')[-1]}]" )
    
    # create the VO audio clip
    VoAudioClip = AudioFileClip(VoAudio)

    # create a blured version of the image that we will use as the background
    bk_blured = Image.open(ImageClipPath).filter(ImageFilter.GaussianBlur(radius = ClipSettings['bk_blurRadius']))
    bk_blured.save(f"{ImageClipPath}.blured.png")

    # Create a black clip that we will overlay images ontop of. Clip is the same length as the VO audio
    baseClip = ColorClip((ClipSettings['width'], ClipSettings['height']), (0, 0, 0), duration=VoAudioClip.duration)
    baseClip.duration = VoAudioClip.duration
    baseClip.audio = VoAudioClip
    baseClip.fps = ClipSettings['fps']
    
    # create a blured background clip
    backgroundImage = ImageClip(f"{ImageClipPath}.blured.png").set_duration(VoAudioClip.duration).set_pos(("center","center")).resize(width=ClipSettings['height'], height=ClipSettings['height'])
    
    # create the standard, main image clip 
    focus = ImageClip(ImageClipPath).set_duration(VoAudioClip.duration).set_pos(("center","center"))
    focus = zoom_in_effect(focus, ClipSettings['zoomRatio'])

    retClip = CompositeVideoClip([baseClip, backgroundImage, focus])
    focus.close()
    backgroundImage.close()
    baseClip.close()
    return retClip



# zoom effect take from https://github.com/Zulko/moviepy/issues/1402
def zoom_in_effect(clip, zoom_ratio):
    def effect(get_frame, t):
            img = Image.fromarray(get_frame(t))
            base_size = img.size

            w, h = img.size
            new_w = w * (1 + (zoom_ratio * t))
            new_h = new_w * (h / w)

            # Determine the height based on the new width to maintain the aspect ratio.
            new_size = (int(new_w), int(new_h))

            img = img.resize(new_size, Image.LANCZOS)

            x = math.ceil((new_size[0] - base_size[0]) / 2)
            y = math.ceil((new_size[1] - base_size[1]) / 2)

            img = img.crop([
                x, y, new_size[0] - x, new_size[1] - y
            ]).resize(base_size, Image.LANCZOS)

            result = numpy.array(img)
            img.close()

            return result
    return clip.fl(effect)


if __name__ == "__main__":
    print("Video Editor Utils.")
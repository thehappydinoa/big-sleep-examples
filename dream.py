import os
import shutil
import glob
from tkinter import N
from typing import Optional
from uuid import uuid4

from big_sleep import Imagine
from imageio import imread, mimsave

# Put your phrase here
TEXT = "The stars are a great mirror"

# Penalize the phrases
TEXT_MIN = "blur|zoom"

# Bad characters for files
BAD_CHARACTERS = "\n?."


def clean_up_text(text: str) -> str:
    for ch in BAD_CHARACTERS:
        text = text.replace(ch, "")
    return text

def create_animation_from_dir(dir: Optional[str] = None, file_type=".png", save_gif=True, save_video=False):
    if dir is None:
        dir = os.getcwd()

    textpath = None
    images = []
    for file_name in sorted(os.listdir(dir)):
        if file_name.endswith(file_type):
            images.append(imread(os.path.join(dir, file_name)))
            if not textpath:
                textpath = file_name.split(".")[0]

    if save_video:
        mimsave(f"{textpath}.mp4", images)
        print(f"Generated image generation animation at ./{textpath}.mp4")
    if save_gif:
        mimsave(f"{textpath}.gif", images)
        print(f"Generated image generation animation at ./{textpath}.gif")
    

def mkdir_and_dream(text: str, save_gif=False, save_video=False, **kwargs) -> str:
    start = os.getcwd()

    best_dir = os.path.join(start, "best")
    if not os.path.isdir(best_dir):
        os.mkdir(best_dir)

    image_id = str(uuid4())

    print(f"Moving into {image_id}/")

    if not os.path.isdir(image_id):
        os.mkdir(image_id)
    os.chdir(image_id)

    dream = Imagine(
        text=clean_up_text(text),
        save_every=25,
        save_progress=True,
        save_best=True,
        open_folder=False,
        **kwargs,
    )

    try:
        dream()
    except OSError as err:
        print("Error: Could not create file.")
        print(err)
        shutil.rmtree(image_id)
    except KeyboardInterrupt:
        print("Exit: User cancelled.")

    # create_animation_from_dir()

    # Copy to best dir
    for file in glob.glob("*.best.*"):
        shutil.copy(file, os.path.join(best_dir, file))

    os.chdir(start)

    return image_id


if __name__ == "__main__":
    # mkdir_and_dream(TEXT, text_min=TEXT_MIN)
    mkdir_and_dream(TEXT, text_min=TEXT_MIN, num_cutouts=48, max_classes=900, lr=0.05)
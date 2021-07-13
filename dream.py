import os
import shutil
import glob
from tkinter import N
from typing import Optional
from uuid import uuid4

from big_sleep import Imagine
from imageio import imread, mimsave

# Put your phrase here
PHRASES = [
    "The moon is a great place to work|The sky is the limit",
    "A dream is a dream",
    "A dream is a journey",
    "I was a robot",
    "Psychedelic fractal trees",
    "Psychedelic fractal mushrooms",
    "Psychedelic fractal trees|mushrooms|atoms",
]

# Penalize the phrases
TEXT_MIN = "blur|zoom"

# Bad characters for files
BAD_CHARACTERS = "\n?."


def clean_up_text(text: str) -> str:
    for ch in BAD_CHARACTERS:
        text = text.replace(ch, "")
    return text


def create_animation_from_dir(
    dir: Optional[str] = None, file_type="png", save_gif=True, save_video=False
):
    start = None
    if dir:
        start = os.getcwd()
        os.chdir(dir)
    else:
        dir = os.getcwd()

    def get_file_order(file_name: str) -> int:
        return int(file_name.replace("." + file_type, "").split(".")[-1])

    file_names = [
        path
        for path in glob.glob(f"*.{file_type}")
        if "best" not in path and path.count(".") >= 2
    ]
    file_names.sort(key=get_file_order)

    text_path = None
    images = []
    for file_name in file_names:
        images.append(imread(file_name))
        if not text_path:
            text_path = file_name.split(".")[0]

    if save_video:
        mimsave(f"{text_path}.mp4", images)
        print(f"Generated image generation animation at ./{text_path}.mp4")
    if save_gif:
        mimsave(f"{text_path}.gif", images)
        print(f"Generated image generation animation at ./{text_path}.gif")

    if start:
        os.chdir(start)


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

    if save_gif or save_video:
        create_animation_from_dir(save_gif=save_gif, save_video=save_video)

    # Copy to best dir
    for file in glob.glob("*.best.*"):
        shutil.copy(file, os.path.join(best_dir, file))

    os.chdir(start)

    return image_id


if __name__ == "__main__":
    # mkdir_and_dream(TEXT, text_min=TEXT_MIN)
    # for phrase in PHRASES:
    #     mkdir_and_dream(
    #         phrase,
    #         text_min=TEXT_MIN,
    #         num_cutouts=48,
    #         max_classes=900,
    #         lr=0.05,
    #         iterations=250,
    #         save_gif=True,
    #     )
    create_animation_from_dir("b2e78ed0-d68d-4436-a5bb-97ee4471768a", save_gif=True)

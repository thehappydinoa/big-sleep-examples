import os
import shutil
import glob
from uuid import uuid4

from big_sleep import Imagine

# Put your phrase here
TEXT = "A lighthouse on the moon"

# Penalize the phrases
TEXT_MIN = ("blur|zoom")

# Bad characters for files
BAD_CHARACTERS = "\n?."


def clean_up_text(text: str) -> str:
    for ch in BAD_CHARACTERS:
        text = text.replace(ch, "")
    return text


def mkdir_and_dream(text: str, **kwargs) -> str:
    start = os.getcwd()

    best_dir = "best"
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

    for file in glob.glob("*.best.*"):
        shutil.copy(file, os.path.join(best_dir, file))

    os.chdir(start)

    return image_id


if __name__ == "__main__":
    mkdir_and_dream(TEXT, text_min=TEXT_MIN)

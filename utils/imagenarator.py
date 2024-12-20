import os
import re
import textwrap

from PIL import Image, ImageDraw, ImageFont
from rich.progress import track

from TTS.engine_wrapper import process_text
from utils.console import print_step, print_substep


def draw_multiple_line_text(
    image, text, font, text_color, padding, wrap=50, transparent=False
) -> None:
    """
    Draw multiline text over given image
    """
    # TODO: Optimize code for comments

    draw = ImageDraw.Draw(image)
    Fontperm = font.getsize(text)
    image_width, image_height = image.size
    lines = textwrap.wrap(text, width=wrap)
    y = (image_height / 2) - (((Fontperm[1] + (len(lines) * padding) / len(lines)) * len(lines)) / 2)
    for line in lines:
        line_width, line_height = font.getsize(line)
        if transparent:
            shadowcolor = "black"
            for i in range(1, 5):
                draw.text(
                    ((image_width - line_width) / 2 - i, y - i),
                    line,
                    font=font,
                    fill=shadowcolor,
                )
                draw.text(
                    ((image_width - line_width) / 2 + i, y - i),
                    line,
                    font=font,
                    fill=shadowcolor,
                )
                draw.text(
                    ((image_width - line_width) / 2 - i, y + i),
                    line,
                    font=font,
                    fill=shadowcolor,
                )
                draw.text(
                    ((image_width - line_width) / 2 + i, y + i),
                    line,
                    font=font,
                    fill=shadowcolor,
                )
        draw.text(((image_width - line_width) / 2, y), line, font=font, fill=text_color)
        y += line_height + padding


def imagemaker(theme, reddit_obj: dict, txtclr, padding=5, transparent=False) -> None:
    """
    Render Images for video
    """

    texts = reddit_obj["thread_post"]
    id = re.sub(r"[^\w\s-]", "", reddit_obj["thread_id"])

    #texts = split_text(" ".join(texts))

    if transparent:
        font = ImageFont.truetype(os.path.join("fonts", "Roboto-Bold.ttf"), 100)
    else:
        font = ImageFont.truetype(os.path.join("fonts", "Roboto-Regular.ttf"), 100)
    size = (1920, 1080)

    for idx, text in track(enumerate(texts), "Rendering Image"):
        image = Image.new("RGBA", size, theme)
        text = process_text(text, False)
        draw_multiple_line_text(image, text, font, txtclr, padding, wrap=30, transparent=transparent)
        image.save(f"assets/temp/{id}/png/img{idx}.png")
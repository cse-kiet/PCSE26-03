import asyncio
from random import randint
from time import sleep

from dotenv import get_key
from huggingface_hub import InferenceClient
from PIL import Image

import os
os.makedirs("Data", exist_ok=True)


if not HF_TOKEN:
    raise ValueError("HuggingFace API key missing in .env file")
MODEL = "black-forest-labs/FLUX.1-dev"

client = InferenceClient(
    provider="fal-ai",
    api_key=HF_TOKEN,
)


def clean_prompt(prompt: str) -> str:
    prompt = prompt.strip()
    lower_prompt = prompt.lower()

    if lower_prompt.startswith("generate image of "):
        prompt = prompt[18:]
    elif lower_prompt.startswith("generate image "):
        prompt = prompt[15:]

    return prompt.strip()


def image_file_name(prompt: str, index: int) -> str:
    safe_prompt = prompt.lower().replace(" ", "_")
    return fr"Data\generate_image_{safe_prompt}{index}.jpg"


def open_images(prompt: str):
    for i in range(1, 5):
        image_path = image_file_name(prompt, i)

        try:
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(1)
        except IOError:
            print(f"Unable to open {image_path}")


def generate_one_image(prompt: str, index: int):
    image = client.text_to_image(
        prompt=f"{prompt}, 4k, sharp, ultra detailed, high resolution",
        model=MODEL,
        width=1024,
        height=1024,
        num_inference_steps=8,
        seed=randint(0, 1000000),
    )

    image.save(image_file_name(prompt, index))


async def generate_images(prompt: str):
    tasks = [
        asyncio.to_thread(generate_one_image, prompt, i)
        for i in range(1, 5)
    ]

    await asyncio.gather(*tasks)


def GenerateImages(prompt: str):
    prompt = clean_prompt(prompt)

    print(f"Generating images for: {prompt}")
    asyncio.run(generate_images(prompt))
    open_images(prompt)


while True:
    try:
        with open(r"Frontend\Files\ImageGeneration.data", "r", encoding="utf-8") as f:
            data = f.read().strip()

        prompt, status = data.split(",", 1)
        prompt = prompt.strip()
        status = status.strip()

        if status == "True":
            GenerateImages(prompt)

            with open(r"Frontend\Files\ImageGeneration.data", "w", encoding="utf-8") as f:
                f.write("False,False")

            break

        sleep(1)

    except Exception as e:
        print(f"Image generation error: {e}")

        with open(r"Frontend\Files\ImageGeneration.data", "w", encoding="utf-8") as f:
            f.write("False,False")

        break

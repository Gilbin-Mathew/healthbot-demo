# backend.py

import ollama
import base64


def generate_response(prompt):
    response = ollama.generate(
        model="llava",
        prompt=prompt,
        stream=False
    )

    text = response.get("response", "")
    images = []

    if "images" in response:
        for img in response["images"]:
            images.append(base64.b64decode(img))

    return text, images

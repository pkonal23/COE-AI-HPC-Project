import requests
import base64
import os

class LLMinfer:
    def __init__(self, api_url="http://localhost:8000/generate", api_key="mysecretkey", model="llama4"):
        self.api_url = api_url
        self.api_key = api_key
        self.model = model
        self.headers = {
            "Content-Type": "application/json",
            "X-API-Key": self.api_key
        }

    def infer(self, mode, prompt_text, image_path=None, max_tokens=1024, temperature=0.7, top_p=1.0, stream=False):
        if mode == "text-to-text":
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": "This is a chat between a user and an assistant. The assistant is helping the user with general questions."
                    },
                    {
                        "role": "user",
                        "content": prompt_text
                    }
                ],
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_p": top_p,
                "stream": stream
            }

        elif mode == "image-text-to-text":
            if not image_path or not os.path.exists(image_path):
                raise FileNotFoundError("Image path must be provided and valid for image-text-to-text mode.")

            with open(image_path, "rb") as f:
                base64_image = base64.b64encode(f.read()).decode("utf-8")

            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": "This is a chat between a user and an assistant. The assistant is helping the user to describe an image."
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            },
                            {
                                "type": "text",
                                "text": prompt_text
                            }
                        ]
                    }
                ],
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_p": top_p,
                "stream": stream
            }

        else:
            raise ValueError("Invalid mode. Use 'text-to-text' or 'image-text-to-text'.")

        response = requests.post(self.api_url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()

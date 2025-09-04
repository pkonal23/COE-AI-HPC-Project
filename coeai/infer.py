# import requests
# import base64
# import os

# class LLMinfer:
#     def __init__(self, api_url="http://localhost:8000/generate", api_key="mysecretkey", model="llama4"):
#         self.api_url = api_url
#         self.api_key = api_key
#         self.model = model
#         self.headers = {
#             "Content-Type": "application/json",
#             "X-API-Key": self.api_key
#         }

#     def infer(self, mode, prompt_text, image_path=None, max_tokens=1024, temperature=0.7, top_p=1.0, stream=False):
#         if mode == "text-to-text":
#             payload = {
#                 "model": self.model,
#                 "messages": [
#                     {
#                         "role": "system",
#                         "content": "This is a chat between a user and an assistant. The assistant is helping the user with general questions."
#                     },
#                     {
#                         "role": "user",
#                         "content": prompt_text
#                     }
#                 ],
#                 "max_tokens": max_tokens,
#                 "temperature": temperature,
#                 "top_p": top_p,
#                 "stream": stream
#             }

#         elif mode == "image-text-to-text":
#             if not image_path or not os.path.exists(image_path):
#                 raise FileNotFoundError("Image path must be provided and valid for image-text-to-text mode.")

#             with open(image_path, "rb") as f:
#                 base64_image = base64.b64encode(f.read()).decode("utf-8")

#             payload = {
#                 "model": self.model,
#                 "messages": [
#                     {
#                         "role": "system",
#                         "content": "This is a chat between a user and an assistant. The assistant is helping the user to describe an image."
#                     },
#                     {
#                         "role": "user",
#                         "content": [
#                             {
#                                 "type": "image_url",
#                                 "image_url": {
#                                     "url": f"data:image/jpeg;base64,{base64_image}"
#                                 }
#                             },
#                             {
#                                 "type": "text",
#                                 "text": prompt_text
#                             }
#                         ]
#                     }
#                 ],
#                 "max_tokens": max_tokens,
#                 "temperature": temperature,
#                 "top_p": top_p,
#                 "stream": stream
#             }

#         else:
#             raise ValueError("Invalid mode. Use 'text-to-text' or 'image-text-to-text'.")

#         response = requests.post(self.api_url, headers=self.headers, json=payload)
#         response.raise_for_status()
#         return response.json()


# coeai/infer.py
import requests
import json
from typing import List, Optional, Union, Dict

class LLMinfer:
    """
    COE AI LLM inference client for LAN access.

    Supports:
    - text-to-text
    - image-to-text (only llama4:16x17b)
    - streaming (prints while collecting)
    - custom messages
    """

    def __init__(self, api_key: str, host: str = "http://127.0.0.1:8001"):
        self.api_key = api_key
        self.host = host.rstrip("/")

    def generate(
        self,
        model: str,
        inference_type: str = "text-to-text",
        prompt: Optional[str] = None,
        messages: Optional[List[Dict[str, Union[str, List[Dict]]]]] = None,
        files: Optional[List[str]] = None,
        max_tokens: int = 512,
        temperature: float = 0.7,
        top_p: float = 1.0,
        stream: bool = False,
        print_stream: bool = True
    ) -> Dict:
        """
        Generate a response from the model.

        Returns a Python dict always, even in streaming mode.
        """
        url = f"{self.host}/generate"

        # Validation
        if inference_type not in ["text-to-text", "image-to-text"]:
            raise ValueError("inference_type must be 'text-to-text' or 'image-to-text'")
        if inference_type == "image-to-text":
            if model != "llama4:16x17b":
                raise ValueError("image-to-text is only supported on 'llama4:16x17b'")
            if not files or len(files) == 0:
                raise ValueError("No image files provided for image-to-text inference")

        # Prepare messages
        payload_messages = messages if messages else (
            [{"role": "user", "content": [{"type": "text", "text": prompt}]}] if prompt else None
        )
        if not payload_messages:
            raise ValueError("Either prompt or messages must be provided")

        # Prepare files payload for image-to-text
        files_payload = []
        if inference_type == "image-to-text" and files:
            for path in files:
                files_payload.append(("files", open(path, "rb")))

        # Prepare form data
        data = {
            "model": model,
            "inference_type": inference_type,
            "max_tokens": str(max_tokens),
            "temperature": str(temperature),
            "top_p": str(top_p),
            "stream": str(stream).lower(),
            "prompt": prompt or "",
            "messages": json.dumps(payload_messages)
        }

        # Send request
        if stream:
            full_output = ""
            with requests.post(url, headers={"X-API-Key": self.api_key}, data=data, files=files_payload, stream=True, timeout=600) as r:
                r.raise_for_status()
                for line in r.iter_lines():
                    if line:
                        chunk = line.decode("utf-8")
                        full_output += chunk
                        if print_stream:
                            print(chunk, end="")
            return {"response": full_output}
        else:
            response = requests.post(url, headers={"X-API-Key": self.api_key}, data=data, files=files_payload, timeout=600)
            response.raise_for_status()
            return response.json()

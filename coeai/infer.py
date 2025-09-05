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

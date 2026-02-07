# coeai/infer.py
"""
COE AI LLM Inference Client

Professional client library for the COE AI LLM inference API with:
- Automatic file handle cleanup
- Comprehensive error handling  
- Optional debug logging
- Support for all vision-capable models
"""

import requests
import json
import logging
from typing import List, Optional, Union, Dict
from pathlib import Path


# Configure logger
logger = logging.getLogger(__name__)


class COEAIError(Exception):
    """Base exception for COEAI client errors"""
    pass


class AuthenticationError(COEAIError):
    """Raised when API key authentication fails"""
    pass


class ModelNotFoundError(COEAIError):
    """Raised when specified model is not available"""
    pass


class InferenceError(COEAIError):
    """Raised when inference request fails"""
    pass


class LLMinfer:
    """
    COE AI LLM inference client for LAN access.

    Supports:
    - text-to-text: All available text models
    - image-to-text: Vision-capable models (llama4:16x17b, llama3.2-vision:11b, etc.)
    - streaming: Real-time response streaming
    - custom messages: Advanced conversation handling

    Example:
        >>> from coeai import LLMinfer
        >>> llm = LLMinfer(api_key="your-key", host="http://10.9.6.165:8000")
        >>> response = llm.generate(model="tinyllama:latest", prompt="Hello!")
    """

    # Vision-capable models (can be extended as new models are added)
    VISION_MODELS = {"llama4:16x17b", "llama4:128x17b", "llama3.2-vision:11b"}

    def __init__(self, api_key: str, host: str = "http://10.9.6.165:8000"):
        """
        Initialize the COE AI LLM inference client.

        Note: This API is only accessible from UPES's internal network (UPESNET).
        Get your API key from: https://coeai.ddn.upes.ac.in

        Args:
            api_key: Your COE AI API authentication key
            host: The FastAPI server endpoint URL (default: http://10.9.6.165:8000)

        Raises:
            ValueError: If api_key is empty or invalid
        """
        if not api_key or not api_key.strip():
            raise ValueError("API key cannot be empty")

        self.api_key = api_key.strip()
        self.host = host.rstrip("/")
        logger.info(f"Initialized COEAI client with host: {self.host}")

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
        Generate a response from the specified model.

        Args:
            model: Model name (e.g., "tinyllama:latest", "llama4:16x17b")
            inference_type: Either "text-to-text" or "image-to-text"
            prompt: Text prompt for generation (optional if messages provided)
            messages: Custom conversation messages (optional if prompt provided)
            files: List of image file paths for image-to-text (optional)
            max_tokens: Maximum number of tokens to generate (default: 512)
            temperature: Sampling temperature 0.0-2.0 (default: 0.7)
            top_p: Nucleus sampling parameter 0.0-1.0 (default: 1.0)
            stream: Enable streaming response (default: False)
            print_stream: Print streaming output to console (default: True)

        Returns:
            Dict: API response dictionary containing generated content

        Raises:
            ValueError: If parameters are invalid
            AuthenticationError: If API key authentication fails
            ModelNotFoundError: If specified model is not available
            InferenceError: If inference request fails
            FileNotFoundError: If specified image files don't exist

        Example:
            >>> response = llm.generate(
            ...     model="tinyllama:latest",
            ...     prompt="Explain AI",
            ...     max_tokens=100
            ... )
        """
        # Validate inference type
        if inference_type not in ["text-to-text", "image-to-text"]:
            raise ValueError(
                f"inference_type must be 'text-to-text' or 'image-to-text', "
                f"got '{inference_type}'"
            )

        # Validate image-to-text requirements
        if inference_type == "image-to-text":
            if not files or len(files) == 0:
                raise ValueError(
                    "No image files provided for image-to-text inference. "
                    "Please provide at least one image file path via the 'files' parameter."
                )

            # Check if files exist
            for file_path in files:
                if not Path(file_path).exists():
                    raise FileNotFoundError(
                        f"Image file not found: {file_path}\n"
                        f"Please check the file path and try again."
                    )

            # Warn if model might not support vision
            if model not in self.VISION_MODELS:
                logger.warning(
                    f"Model '{model}' may not support image-to-text. "
                    f"Recommended vision models: {', '.join(self.VISION_MODELS)}"
                )

        # Validate prompt or messages
        if not prompt and not messages:
            raise ValueError("Either 'prompt' or 'messages' must be provided")

        # Prepare messages
        payload_messages = messages if messages else (
            [{"role": "user", "content": [{"type": "text", "text": prompt}]}] if prompt else None
        )

        logger.debug(f"Sending request to {self.host}/generate with model '{model}'")

        # Prepare request
        url = f"{self.host}/generate"
        file_handles = []

        try:
            # Prepare files payload for image-to-text
            files_payload = []
            if inference_type == "image-to-text" and files:
                for path in files:
                    fh = open(path, "rb")
                    file_handles.append(fh)
                    files_payload.append(("files", fh))
                logger.debug(f"Attached {len(files)} image file(s)")

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
                return self._handle_streaming(url, data, files_payload, print_stream)
            else:
                return self._handle_non_streaming(url, data, files_payload)

        except requests.exceptions.ConnectionError as e:
            raise InferenceError(
                f"Could not connect to COE AI server at {self.host}\n"
                f"Please check:\n"
                f"  1. Server is running\n"
                f"  2. You're on UPES Wi-Fi network\n"
                f"  3. Host URL is correct\n"
                f"Original error: {str(e)}"
            )
        except requests.exceptions.Timeout as e:
            raise InferenceError(
                f"Request timed out after 600 seconds.\n"
                f"This may happen with very large models or long prompts.\n"
                f"Original error: {str(e)}"
            )
        finally:
            # Always close file handles
            for fh in file_handles:
                try:
                    fh.close()
                except Exception as e:
                    logger.warning(f"Failed to close file handle: {e}")

    def _handle_streaming(self, url: str, data: dict, files_payload: list, print_stream: bool) -> Dict:
        """Handle streaming response"""
        full_output = ""
        try:
            with requests.post(
                url,
                headers={"X-API-Key": self.api_key},
                data=data,
                files=files_payload,
                stream=True,
                timeout=600
            ) as r:
                self._check_response_status(r)
                
                for line in r.iter_lines():
                    if line:
                        chunk = line.decode("utf-8")
                        full_output += chunk
                        if print_stream:
                            print(chunk, end="")

            return {"response": full_output}

        except requests.exceptions.HTTPError as e:
            self._handle_http_error(e)

    def _handle_non_streaming(self, url: str, data: dict, files_payload: list) -> Dict:
        """Handle non-streaming response"""
        try:
            response = requests.post(
                url,
                headers={"X-API-Key": self.api_key},
                data=data,
                files=files_payload,
                timeout=600
            )
            self._check_response_status(response)
            return response.json()

        except requests.exceptions.HTTPError as e:
            self._handle_http_error(e)

    def _check_response_status(self, response: requests.Response):
        """Check response status and raise appropriate errors"""
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            # Will be handled by _handle_http_error
            raise

    def _handle_http_error(self, error: requests.exceptions.HTTPError):
        """Handle HTTP errors with detailed messages"""
        response = error.response
        status_code = response.status_code

        try:
            error_detail = response.json().get("detail", "No error details provided")
        except:
            error_detail = response.text

        if status_code == 401:
            raise AuthenticationError(
                f"Authentication failed. Invalid or expired API key.\n"
                f"Please check your API key and try again.\n"
                f"Get a new key from: https://10.9.6.165"
            )
        elif status_code == 400:
            raise ValueError(
                f"Bad request: {error_detail}\n"
                f"Please check your parameters (model name, inference type, etc.)"
            )
        elif status_code == 404:
            raise ModelNotFoundError(
                f"Model not found or endpoint unavailable.\n"
                f"Error: {error_detail}\n"
                f"Use llm.list_models() to see available models."
            )
        elif status_code == 429:
            raise InferenceError(
                f"Rate limit exceeded: {error_detail}\n"
                f"Please wait and try again."
            )
        elif status_code >= 500:
            raise InferenceError(
                f"Server error ({status_code}): {error_detail}\n"
                f"This is likely a temporary issue. Please try again later."
            )
        else:
            raise InferenceError(
                f"HTTP {status_code}: {error_detail}"
            )

    def list_models(self) -> List[str]:
        """
        Get list of available models from the server.

        Returns:
            List[str]: List of available model names

        Raises:
            AuthenticationError: If API key authentication fails
            InferenceError: If request fails

        Example:
            >>> models = llm.list_models()
            >>> print(f"Available models: {', '.join(models)}")
        """
        url = f"{self.host}/models"

        try:
            response = requests.get(
                url,
                headers={"X-API-Key": self.api_key},
                timeout=10
            )
            self._check_response_status(response)
            data = response.json()
            models = data.get("models", [])
            logger.info(f"Retrieved {len(models)} models from server")
            return models

        except requests.exceptions.HTTPError as e:
            self._handle_http_error(e)
        except requests.exceptions.ConnectionError:
            raise InferenceError(
                f"Could not connect to {self.host}\n"
                f"Please check your network connection and server availability."
            )
        except Exception as e:
            raise InferenceError(f"Failed to list models: {str(e)}")

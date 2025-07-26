# coeai `PyPI Package`

**Interact with high-capacity multimodal LLMs hosted on the COE AI GPU cluster from any Python environment.**

`coeai` is a lightweight Python wrapper currently around the *LLaMA-4 16x17B* model (128K context, vision-enabled) deployed on the Centre of Excellence for AI (COE AI) servers at UPES. It exposes a single `/generate` HTTP endpoint, making it trivial to run both text-only and image+text inference from notebooks, scripts or backend services connected to the UPES Wi-Fi.

> **Text and image input** **128,000-token context** **Streaming or batch** **Runs on the COE AI GPU node**

---

## Table of Contents
1. [Features](#features)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Quick Start](#quick-start)
5. [API Usage](#api-usage)
6. [Model Parameters](#model-parameters)
7. [Authentication](#authentication)
8. [Joining COE AI](#joining-coe-ai)
9. [Troubleshooting](#troubleshooting)
10. [License](#license)
11. [Author](#author)

---

## Features

* **Ultra-long context** up to **128K tokens** per request for long documents or multi-turn chats
* **Vision support** send images along with text for multimodal reasoning
* **High performance** queries are served by a dedicated GPU node inside the COE AI HPC cluster
* **Simple auth** authenticate with a short-lived API key (valid 30 days) sent in the request header
* **Drop-in wrapper** minimal Python API; no need to handle HTTP manually

---

## Requirements

* Python **3.8 or newer**
* Network access to `http://10.16.1.50:8000` from the UPES campus Wi-Fi
* A **valid API key** issued by the COE AI team

---

## Installation

```bash
pip install coeai
```

This pulls the latest release from PyPI.

---

## Quick Start

The wrapper exposes a single `LLMinfer` class. Initialize it with the API URL and your API key, then call `infer()`.

### Text-to-Text

```python
from coeai import LLMinfer

llm = LLMinfer(
    api_url="http://10.16.1.50:8000/generate",
    api_key="API_KEY"
)

response = llm.infer(
    mode="text-to-text",
    prompt_text="Summarize the key points of general relativity.",
    max_tokens=500,
    temperature=0.6,
    top_p=0.95,
    stream=False
)

print(response)

```

### Image + Text

```python
from coeai import LLMinfer

# Initialize the client
llm = LLMinfer(
    api_url="http://10.16.1.50:8000/generate",
    api_key="API_KEY"
)

# Run inference with image and prompt
response = llm.infer(
    mode="image-text-to-text",
    prompt_text="Describe what's happening in the image.",
    image_path="/home/konal.106904/sample.jpg",  # <-- update to a valid path
    max_tokens=512,
    temperature=0.7,
    top_p=1.0,
    stream=False
)

# Print the response
print(response)

```

---

## API Usage

### Using the Python Wrapper

The examples above show the recommended approach using the `LLMinfer` class.

### Direct API Access with cURL

You can also interact directly with the `/generate` endpoint using cURL.

#### Prerequisites

| Requirement | Purpose |
|-------------|---------|
| A running instance of the API | Default URL: `http://10.16.1.50:8000/generate` |
| Valid API key | Supply in the `X-API-Key` request header |
| cURL 7.68+ | Supports `--data @-` JSON piping |

#### Text-Only Request

```bash
curl -X POST http://10.16.1.50:8000/generate \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY_HERE" \
  -d '{
    "model": "llama4",
    "messages": [
      {
        "role": "system",
        "content": "This is a chat between a user and an assistant. The assistant is helping the user with general questions."
      },
      {
        "role": "user",
        "content": "Explain what a black hole is."
      }
    ],
    "max_tokens": 512,
    "temperature": 0.7,
    "top_p": 1.0,
    "stream": false
  }'
```

#### Image + Text Request

For multimodal requests, include the image as a Base64-encoded Data URI in the `content` array:

> **Note:** Replace `YOUR_API_KEY_HERE` with your own API key and `PUT_BASE64_IMAGE_STRING_HERE` with the **Base64-encoded** contents of your image file.

**How it Works:**
1. **Inline Image**: The `image_url` object embeds the entire image as a Data URI so no separate file upload is required
2. **Multi-Modal Prompt**: The `content` field is an array containing both the image and the accompanying text question, preserving ordering
3. **Response**: The server returns a JSON object containing the assistant's interpretation of the supplied image

---

## Model Parameters

### Default Parameters

| Field          | Description                                  | Default |
|----------------|----------------------------------------------|---------|
| `model`        | Model name (currently fixed to `llama4`)     | `llama4`      |
| `stream`       | Return tokens incrementally                  | `false` |
| `max_tokens`   | Maximum new tokens to generate               | `1024`  |
| `temperature`  | Sampling temperature (creativity)            | `0.7`   |
| `top_p`        | Nucleus sampling                             | `1.0`   |
| `stop`         | List of stop sequences                       | `null`  |

### Parameter Details

| Parameter      | Description |
|----------------|-------------|
| `model`        | The model identifier exposed by your server (here `llama4`) |
| `messages`     | Conversation history, each entry containing a `role` and `content` |
| `max_tokens`   | Upper bound on tokens in the assistant reply |
| `temperature`  | Controls randomness; lower values yield more deterministic output |
| `top_p`        | Nucleus sampling; keep at `1.0` for default behavior |
| `stream`       | When `true`, the API will send incremental responses via Server-Sent Events (SSE) |

> **Note:** The server enforces total context of 128K tokens (prompt + generated). Adjust `max_tokens` accordingly.

---

## Authentication

All requests must include an **API key** issued by the COE AI team. Pass the key when constructing `LLMinfer` (it is added as an `Authorization` header behind the scenes).

### Requesting an API Key

1. **Send an email** to `hpc-access@ddn.upes.ac.in` *from your official UPES account* using this template:

```
Subject: API Key Request for COE AI LLM Access

Dear COE AI Team,

I am requesting access to the LLM API for my project work.

Project Details:
- Project Name: <Your Project Name>
- Project Description: <Brief description>
- Expected Usage: <How you plan to use the LLM>
- Duration: <Timeline>

Reason for API Access:
<Research objectives or academic requirements>

Additional Information:
- Name: <Your Name>
- Email: <Your Email>
- Department/Affiliation: <Dept/Organisation>
- Student/Faculty ID: <If applicable>

Thank you for considering my request.

Best regards,
<Your Name>
```

2. Allow **2-3 business days** for processing. The team will reply with your API key.

### Key Renewal

Keys expire **after 30 days**. Email the same address with the subject:
```
Subject: API Key Renewal Request for COE AI LLM Access
```

Include your previous key and a brief usage summary.

---

## Troubleshooting

| Symptom | Possible Cause | Fix |
|---------|----------------|-----|
| `ConnectionError` | Not on UPES network | Connect to campus Wi-Fi or VPN |
| `401 Unauthorized` | Missing/expired API key | Request or renew your key |
| Long latency | Very large prompts or high `max_tokens` | Reduce prompt size or output length |

---

## License

`coeai` is released under the **MIT License**.

---

## Author

**Konal Puri**  
Centre of Excellence: AI (COE AI), HPC Project, UPES

PyPI: <https://pypi.org/project/coeai>
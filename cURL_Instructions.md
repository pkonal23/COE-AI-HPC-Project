# COE AI LLM API - cURL Usage Guide

This guide provides command-line examples for interacting with the COE AI LLM API using `curl`.

> **⚠️ Requirments**
> - **Network**: You must be connected to **UPESNET** (UPES Internal Wi-Fi).
> - **API Key**: Get your key from [https://coeai.ddn.upes.ac.in](https://coeai.ddn.upes.ac.in).

---

## 🔗 Base URL
**`http://10.9.6.165:8000`**

---

## 1. Check Connection & List Models

Verify your connection and see available models.

```bash
curl -X GET http://10.9.6.165:8000/models \
  -H "X-API-Key: YOUR_API_KEY"
```

---

## 2. Basic Text Generation

Simple prompt-response generation.

```bash
curl -X POST http://10.9.6.165:8000/generate \
  -H "X-API-Key: YOUR_API_KEY" \
  -F "model=tinyllama:latest" \
  -F "inference_type=text-to-text" \
  -F "prompt=Write a haiku about computers." \
  -F "max_tokens=100"
```

---

## 3. Chat / Conversation Mode

Send a conversation history using the `messages` parameter (JSON formatted string).

```bash
curl -X POST http://10.9.6.165:8000/generate \
  -H "X-API-Key: YOUR_API_KEY" \
  -F "model=gpt-oss:120b" \
  -F "inference_type=text-to-text" \
  -F 'messages=[{"role":"system","content":[{"type":"text","text":"You are a helpful assistant."}]},{"role":"user","content":[{"type":"text","text":"What is the capital of France?"}]}]' \
  -F "max_tokens=200"
```

---

## 4. Single Image Analysis

Upload an image for analysis using a Vision model.

```bash
curl -X POST http://10.9.6.165:8000/generate \
  -H "X-API-Key: YOUR_API_KEY" \
  -F "model=llama3.2-vision:11b" \
  -F "inference_type=image-to-text" \
  -F "prompt=Describe this image in detail." \
  -F "files=@/path/to/your/image.jpg" \
  -F "max_tokens=512"
```

---

## 5. Multiple Image Comparison

Compare two or more images.

```bash
curl -X POST http://10.9.6.165:8000/generate \
  -H "X-API-Key: YOUR_API_KEY" \
  -F "model=llama4:16x17b" \
  -F "inference_type=image-to-text" \
  -F "prompt=Compare these two images side by side." \
  -F "files=@/path/to/image1.jpg" \
  -F "files=@/path/to/image2.jpg" \
  -F "max_tokens=1024"
```

---

## 6. Streaming Response

Receive the response token-by-token (real-time). Note the `-N` flag for curl to disable buffering.

```bash
curl -N -X POST http://10.9.6.165:8000/generate \
  -H "X-API-Key: YOUR_API_KEY" \
  -F "model=deepseek-r1:70b" \
  -F "inference_type=text-to-text" \
  -F "prompt=Explain quantum entanglement." \
  -F "stream=true"
```

---

## 7. Advanced Parameters

Control creativity and length.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `temperature` | `0.7` | Higher = more creative, Lower = more factual (0.0 - 2.0) |
| `top_p` | `1.0` | Nucleus sampling (0.0 - 1.0) |
| `max_tokens` | `512` | Maximum length of generation |

```bash
curl -X POST http://10.9.6.165:8000/generate \
  -H "X-API-Key: YOUR_API_KEY" \
  -F "model=deepseek-r1:70b" \
  -F "prompt=Solve this math problem: 24 * 184" \
  -F "max_tokens=200" \
  -F "temperature=0.1" \
  -F "top_p=0.9"
```

---

## ⚠️ Common Errors

| Status Code | Meaning | Solution |
|-------------|---------|----------|
| `401` | Unauthorized | Check `X-API-Key` header |
| `404` | Model Not Found | Use endpoint `/models` to check available models |
| `429` | Rate Limit Exceeded | Wait a moment before next request |
| `500` | Server Error | Server might be overloaded or model crashed |
| `Connection Failed` | Network Error | ensure you are on **UPESNET** |

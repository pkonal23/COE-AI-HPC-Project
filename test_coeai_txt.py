from coeai import LLMinfer

llm = LLMinfer(
    api_url="http://10.16.1.50:8000/generate",
    api_key="coeai-i52mJRrqV9M-6ubL8DVDPMaSLKJGm"
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

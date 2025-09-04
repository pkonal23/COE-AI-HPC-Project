from coeai.infer import LLMinfer

api_key = "mysecretkeycoeaiqwerty"
llm = LLMinfer(api_key, host="http://10.9.6.165:8001")

messages = [
    {"role": "system", "content": [{"type": "text", "text": "You are a witty assistant."}]},
    {"role": "user", "content": [{"type": "text", "text": "Explain quantum computing in simple terms."}]}
]

response = llm.generate(
    model="tinyllama:latest",
    inference_type="text-to-text",
    messages=messages,
    max_tokens=400,
    temperature=0.9,
    top_p=0.95,
    print_stream=True
)

print("\nCollected full response:", response)

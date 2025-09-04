from coeai.infer import LLMinfer

api_key = "mysecretkeycoeaiqwerty"
llm = LLMinfer(api_key, host="http://10.9.6.165:8001")

messages = [
    {"role": "system", "content": [{"type": "text", "text": "You are a helpful assistant."}]},
    {"role": "user", "content": [{"type": "text", "text": "Give a short summary of COVID-19 impact."}]}
]

response = llm.generate(
    model="llama4:16x17b",
    inference_type="text-to-text",
    messages=messages,
    max_tokens=300,
    temperature=0.6,
    top_p=0.95
)

print(response)

from coeai.infer import LLMinfer

api_key = "mysecretkeycoeaiqwerty"
llm = LLMinfer(api_key, host="http://10.9.6.165:8001")

response = llm.generate(
    model="llama4:16x17b",
    inference_type="image-to-text",
    files=["/Users/konalsmac/Downloads/agies.png"],
    prompt="Describe this image in detail",
    max_tokens=512
)

print(response)

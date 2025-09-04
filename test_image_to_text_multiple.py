from coeai.infer import LLMinfer

api_key = "mysecretkeycoeaiqwerty"
llm = LLMinfer(api_key, host="http://10.9.6.165:8001")

image_paths = [
    "/Users/konalsmac/Downloads/agies.png",
    "/Users/konalsmac/Downloads/gemini.png"
]

response = llm.generate(
    model="llama4:16x17b",
    inference_type="image-to-text",
    files=image_paths,
    prompt="Compare the images and describe similarities and differences",
    max_tokens=512,
    temperature=0.7,
    top_p=1.0
)

print(response)

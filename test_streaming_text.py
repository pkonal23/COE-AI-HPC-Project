from coeai.infer import LLMinfer

api_key = "mysecretkeycoeaiqwerty"
llm = LLMinfer(api_key, host="http://10.9.6.165:8001")

try:
    response = llm.generate(
        model="llama4:16x17b",
        inference_type="image-to-text",
        files=["/path/to/image.png"],
        prompt="Describe this image"
    )
    print(response)
except requests.exceptions.HTTPError as e:
    print(e.response.json())  # <-- shows FastAPI error

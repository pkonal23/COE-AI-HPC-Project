from coeai import LLMinfer

# Initialize the client
llm = LLMinfer(
    api_url="http://10.16.1.50:8000/generate",
    api_key="coeai-2XkLN6BahBIFvvxCWizpo40lmzd"
)

# Run inference with image and prompt
response = llm.infer(
    mode="image-text-to-text",
    prompt_text="Describe what's happening in the image.",
    image_path="/Users/konalsmac/Downloads/website.jpg",  # <-- update to a valid path
    max_tokens=512,
    temperature=0.7,
    top_p=1.0,
    stream=False
)

# Print the response
print(response)

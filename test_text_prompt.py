from coeai import LLMinfer

llm = LLMinfer(api_key="mysecretkeycoeaiqwerty", host="http://10.9.6.165:8001")

response = llm.generate(
    model="tinyllama:latest",
    prompt="Write a haiku about autumn leaves."
)

print(response)  # returns the JSON response

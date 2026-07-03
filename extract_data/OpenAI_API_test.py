import base64
import requests

# OpenAI API Key
api_key = "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"

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
image_path = "/Users/haopengzong/WX20231207-153319@2x.png"

# Getting the base64 string
base64_image = encode_image(image_path)
print(base64_image)
file_path = "/Users/haopengzong/JFC/output.txt"
with open(file_path, 'w') as file:
    file.write(base64_image)
headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
}

payload = {
  "model": "gpt-4-vision-preview",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Can you extract the grades in the format like subject1:mark1/subject2:mark2"
        },
        {
          "type": "image_url",
          "image_url": {
          "url":  f"data:image/jpeg;base64,{base64_image}"
          }
        }
      ]
    }
  ],
  "max_tokens": 300
}

response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

print(response.json())


# from openai import OpenAI
# client = OpenAI()

# completion = client.chat.completions.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
#     {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
#   ]
# )

# print(completion.choices[0].message)
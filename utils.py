import requests, os, glob, json, base64, time
import openai

def delete():
    """Deletes all images in the image/ directory"""
    files = glob.glob("images/*")
    for f in files:
      os.remove(f)

def upload_file(file_path):
    """Upload a file to a CDN"""
    # Set the API endpoint
    API_ENDPOINT = "https://upload.connerow.dev/upload-base64"

    # Read the image file and encode it in base64
    with open(file_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

    # Set the headers for the request
    headers = {
        "Content-Type": "application/json",
        "accept": "*/*"
    }

    # Set the payload for the request
    payload = {
        "image": f"data:image/png;base64,{encoded_image}"
    }

    # Make the POST request
    response = requests.post(API_ENDPOINT, headers=headers, json=payload)

    # Get the response data
    response_data = response.json()

    # Check if the request was successful
    if response_data["success"]:
        # The request was successful, return the URL
        return response_data["url"]
    else:
        # The request was not successful, return the error message
        return response_data["message"]


def gpt(prompt): 
  """change the prompt with openai's text completion"""
  
  openai.api_key = os.getenv("API_KEY")
  
  start_sequence = "\nA:"
  restart_sequence = "\n\nQ: "
  
  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"I am a highly intelligent question answering bot. If you ask me a question that is rooted in truth, I will give you the answer. If you ask me a question that is nonsense, trickery, or has no clear answer, I will respond with \"Question mark\".\n\nQ: Give me a iconic icon for the following sentence. This is used for a logo: \"{prompt}\"\nA: ",
    temperature=0,
    max_tokens=100,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop=["\n"]
  )
  #print(response.content)
  #print(response)
  if 'choices' in response:
    answer = response['choices'][0]['text']
  else:
    answer = 'Unknown'
  print("prompt: "+answer)
  return answer+"digital art, emblem"
  
  


def dalle1(num, icon):
  """Generate an image using the openAI v1 image generater"""
  num +=1
  # Set up the API endpoint and API key
  endpoint = "https://api.openai.com/v1/images/generations"
  api_key = os.environ["API_KEY"]
  
  # Set up the text prompt for the logo
  
  
  # Set up the parameters for the API request
  params = {
      "model": "image-alpha-001",
      "prompt": icon,
      "num_images": 1,
      "size": "256x256",
      "response_format": "url"
  }
  urls = []
  for i in range(1,int(num)):
  
    # Make the API request
    response = requests.post(endpoint, json=params, headers={"Authorization": f"Bearer {api_key}"})
  
    # Get the URL of the generated image
    image_url = response.json()["data"][0]["url"]
  
    # Download the image
    response = requests.get(image_url)
    open(f"./images/logo{i}.png", "wb").write(response.content)
    urls.append(upload_file(f'images/logo{i}.png'))
    print(f"Dalle1 done {i}/{num-1}")
  #print(urls)
  return urls
    
    
def dalle2(number, icon):
  """Generate an image using DALL-E 2"""
  number += 3
  arr = []
  for i in range(3, int(number)):
    response = openai.Image.create( # generate image
      prompt=icon,
      n=1,
      size="256x256",
    )
    print("Dalle2 Done")
    img_data = requests.get(response["data"][0]["url"]).content
    with open(f'images/logo{i}.jpg', 'wb') as handler:
      handler.write(img_data)
    arr.append(upload_file(f'images/logo{i}.jpg'))
  #print(arr)
  return arr

def convertFromSeconds(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
     
    return "%d:%02d:%02d" % (hour, minutes, seconds)


print("\033[32m[Utils] loaded\033[0m")
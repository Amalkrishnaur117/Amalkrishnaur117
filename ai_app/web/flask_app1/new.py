import ollama
import json
import re
language = "english"
topic = "rtc"
level = "beginers"
response = ollama.chat(model='llama3.2', messages=[
  {
    'role': 'user',
    'content': f"""Generate a JSON file for a presentation based on a given topic and specified learning level (beginner, medium, or advanced). Each JSON object should contain multiple scenes, with each scene structured as follows:

    id: A unique identifier for each scene, numbered sequentially.
    title: A concise title summarizing the main idea of the scene.
    points: A list of 2-4 essential points related to the topic.
    script: A single, detailed narration text tailored to the specified learning level.

For the script content:

    Include only the specified learning level’s content.
    Do not include language categories (e.g., "English").
    If a specific language is given, translate the script to that language; otherwise, default to English.
    Customize the content depth as follows:
        Beginner: Use simple language and provide clear explanations, assuming no prior knowledge.
        Medium: Include moderate detail, assuming basic familiarity with the topic.
        Advanced: Offer concise, technical content, assuming the audience has advanced understanding.
don't need to show level in script
language is {language} topic is {topic} and level is {level} i need only json file don't generate other than json

  """,
  },
])
print(response['message']['content'])
input_string = response['message']['content']
json_string = re.search(r'\{.*\}', input_string, re.DOTALL).group(0)
#json_data = json.load(response['message']['content'])
print(json_string)
with open("output.json", "w") as json_file:
    json_file.write(json_string)

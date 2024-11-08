import ollama
response = ollama.chat(model='llama3.2', messages=[
  {
    'role': 'user',
    'content': """Generate a JSON file for a presentation based on a given topic and specified learning level (beginner, medium, or advanced). Each JSON object should contain multiple scenes, with each scene structured as follows:

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
language is english topic is mqtt and level is beginers

  """,
  },
])
print(response['message']['content'])

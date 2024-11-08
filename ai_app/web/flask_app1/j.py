import json

# Open the JSON file and load its contents
with open("output.json", "r") as json_file:
    json_data = json.load(json_file)

# Print the data (or use it for further processing)
print(json_data)

import requests

# Define the URLs and corresponding file names in a dictionary
url_dict = {
    "https://uflorida-my.sharepoint.com/:x:/g/personal/j_fleischer_ufl_edu/EVJAIUIn6K9Csg3fUs2XD8EB4oj7T12L20kOhyvG_2ZnyA?download=1":
    "dota2-620k.csv",
    "https://uflorida-my.sharepoint.com/:x:/g/personal/j_fleischer_ufl_edu/EWcJDzPIIf5Imw4jtPSkCckBHnBL1mdDVFFcJ7qh9d5uxA?download=1":
    "minecraft260k.csv",
    "https://uflorida-my.sharepoint.com/:x:/g/personal/j_fleischer_ufl_edu/EarI7dz6emhPl5qIO0GraugBfxARz2ATkBotYndi0wd7WQ?download=1":
    "tf2100k.csv"
}

# Function to download the file from URL and save it
def download_file(url, file_name):
    response = requests.get(url, allow_redirects=True)
    if response.status_code == 200:
        with open(file_name, 'wb') as file:
            file.write(response.content)
        print(f"File '{file_name}' downloaded successfully.")
    else:
        print(f"Failed to download file from URL: {url}")

# Loop through the URL dictionary and download the files
for url, file_name in url_dict.items():
    download_file(url, file_name)

import requests
import os

def download_latest_release(url, download_path):
    try:
        response = requests.get(url)
        data = response.json()
        if 'message' in data and data['message'] == 'Not Found':
            print("Repository or release not found.")
            return
        if 'assets' not in data or len(data['assets']) == 0:
            download_url = data['zipball_url']  # Download the source code as a zipball
            _download_file(download_url, download_path)
        else:
            assets = data['assets']
            download_url = assets[0]['browser_download_url']
            _download_file(download_url, download_path)
    except Exception as e:
        print(f"Error: {e}")

def _download_file(url, download_path):
    response = requests.get(url)
    with open(download_path, 'wb') as f:
        f.write(response.content)
    #print(f"Downloaded the latest release to {download_path}")
    print(f"FOMX: Downloaded the latest release to {download_path}")
    #print(f'Update: Downloaded the latest release')

# if __name__ == "__main__":
    # repo_url = "https://api.github.com/repos/SketchedDoughnut/development/releases/latest"
    # download_path = "latest_release.zip"  # Change the path if needed
    # download_latest_release(repo_url, download_path)
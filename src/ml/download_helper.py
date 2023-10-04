import requests
from constants import ModelsConst

def is_model_exist(path):
    try:
        with open(path, "rb") as file:
            return True
    except FileNotFoundError:
        return False

def download_asset(asset=ModelsConst.RANDOM_FOREST.value):
    asset_url = (
        f"https://github.com/FishPain/sure-bo/releases/download/v0.1.0/{asset}.pkl"
    )
    destination_path = f"src/models/{asset}.pkl"

    if is_model_exist(destination_path):
        print(f"Model {asset} already exist at {destination_path}")
        return None

    response = requests.get(asset_url, stream=True)

    if response.status_code == 200:
        with open(destination_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=128):
                file.write(chunk)

        print(f"Download successful. Saved to {destination_path}")
        return True

    else:
        print(f"Failed to download asset. Status code: {response.status_code}")
        return False

if __name__ == "__main__":
    download_asset()

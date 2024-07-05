import requests
import json


def fetch_top_datasets(n=20):
    url = "https://huggingface.co/api/datasets"
    response = requests.get(url)
    response.raise_for_status()
    datasets_info = response.json()

    # Sort datasets based on download count (assuming 'downloads' field exists)
    sorted_datasets = sorted(datasets_info, key=lambda x: x.get('downloads', 0), reverse=True)

    # Get the top n datasets
    top_datasets = sorted_datasets[:n]

    return top_datasets


def save_to_json(data, filename='top_datasets.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def main():
    # Fetch the top 20 datasets from Hugging Face
    top_datasets = fetch_top_datasets(20)

    # Save the dataset details to a JSON file
    save_to_json(top_datasets)

    print(f"Saved details of the top 20 datasets to 'top_datasets.json'")


if __name__ == "__main__":
    main()

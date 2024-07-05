import requests
import json

# List of dataset IDs
dataset_ids = [
    "allenai/ai2_arc",
    "cais/mmlu",
    "nyu-mll/glue",
    "hendrycks/competition_math",
    "tau/commonsense_qa",
    "dair-ai/emotion",
    "Skylion007/openwebtext",
    "stanfordnlp/imdb",
    "rajpurkar/squad_v2",
    "Rowan/hellaswag",
    "Helsinki-NLP/tatoeba_mt",
    "cambridgeltl/xcopa",
    "rajpurkar/squad",
    "GEM/wiki_lingua",
    "EdinburghNLP/xsum",
    "allenai/winogrande",
    "webis/tldr-17",
    "Samsung/samsum",
    "Salesforce/wikitext",
    "abisee/cnn_dailymail"
]

def fetch_dataset_info(dataset_id):
    url = f"https://huggingface.co/api/datasets/{dataset_id}"
    response = requests.get(url)
    if response.status_code == 200:
        dataset_info = response.json()
        download_urls = []

        # Use the siblings field to get download URLs
        siblings = dataset_info.get('siblings', [])
        for sibling in siblings:
            if sibling.get('rfilename'):
                download_urls.append(f"https://huggingface.co/datasets/{dataset_id}/resolve/main/{sibling['rfilename']}?download=true")

        return {
            "_id": dataset_info.get("_id", ""),
            "id": dataset_id,
            "author": dataset_info.get("author", ""),
            "lastModified": dataset_info.get("lastModified", ""),
            "likes": dataset_info.get("likes", 0),
            "private": dataset_info.get("private", False),
            "sha": dataset_info.get("sha", ""),
            "description": dataset_info.get("description", ""),
            "downloads": dataset_info.get("downloads", 0),
            "tags": dataset_info.get("tags", []),
            "createdAt": dataset_info.get("createdAt", ""),
            "key": dataset_info.get("key", ""),
            "url": f"https://huggingface.co/datasets/{dataset_id}",
            "downloadUrls": download_urls
        }
    else:
        print(f"Error fetching {dataset_id}: {response.status_code}")
        return None

datasets_info = [fetch_dataset_info(dataset_id) for dataset_id in dataset_ids]
datasets_info = [info for info in datasets_info if info is not None]

with open('datasets_info.json', 'w') as f:
    json.dump(datasets_info, f, indent=4)

print(f"Saved dataset info to 'datasets_info.json'")

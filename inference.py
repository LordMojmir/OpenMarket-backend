import replicate
import os
import dotenv

def get_all_possible_models():
    return [
        "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
        "mistralai/mixtral-8x7b-instruct-v0.1",
        "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
        "snowflake/snowflake-arctic-instruct",
        "meta/meta-llama-3-8b-instruct",
        "meta/llama-2-13b-chat"
        "mistralai/mistral-7b-instruct-v0.2"
    ]

def get_response(for_model, prompt):
    os.environ["REPLICATE_API_TOKEN"] = "r8_5OnMrq4INduZM50iNklGQyXDeQeqTkT32qINX"
    print(os.environ.get("REPLICATE_API_TOKEN"))
    models = [
        "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
        "mistralai/mixtral-8x7b-instruct-v0.1",
        "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
        "snowflake/snowflake-arctic-instruct",
        "meta/meta-llama-3-8b-instruct",
        "meta/llama-2-13b-chat"
            "mistralai/mistral-7b-instruct-v0.2"
    ]
    #
    # if for_model not in models:
    #     raise ValueError(f"Model {for_model} not found")
    # else:
    #     print(f"Using model {for_model}")

    api = replicate.Client(api_token=os.environ["REPLICATE_API_TOKEN"])
    output = api.run(
        for_model,
            input={"prompt": prompt,
                      "max_tokens": 100,
                        "temperature": 0.1,
                        "top_p": 0.9,
                   "system_prompt":"You are a helpful assistant, keep your resposne as short as possible"
    },

    )
    result = ""
    for item in output:
        result += item
        # print(item, end="")

    return result

if __name__ == "__main__":
    prompt = "What is the capital of France?"
    for_model = "meta/llama-2-13b-chat"
    response = get_response(for_model, prompt)
    print(response)
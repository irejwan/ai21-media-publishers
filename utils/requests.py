import requests
from constants import *
from utils.filters import *


def complete(prompt, api_key):
    auth_header = f"Bearer {api_key}"
    resp = requests.post(
        apis['instruct'],
        headers={"Authorization": auth_header},
        json={"prompt": prompt, **MODEL_CONF}
    )
    return resp.json()


def create_prompt(media, article):
    post_type = "tweet" if media == "Twitter" else "Linkedin post"
    instruction = f"Write a {post_type} touting the following press release."
    return f"{instruction}\nArticle:\n{article}\n\n{post_type}:\n"


def generate(article, media, api_key, max_retries=2, top=3):
    prompt = create_prompt(media, article)
    completions_filtered = []
    try_count = 0
    while not len(completions_filtered) and try_count < max_retries:
        res = complete(prompt, api_key=api_key)
        completions_filtered = [comp['data']['text'] for comp in res['completions']
                                if apply_filters(comp, article, media)]
        try_count += 1
    res = prioritize_emojis(filter_duplicates(completions_filtered))[:top]
    return [remove_utf_emojis(anonymize(i)) for i in res]


def summarize(url, api_key):
    auth_header = f"Bearer {api_key}"
    resp = requests.post(
        apis['summarize'],
        headers={"Authorization": auth_header, "Content-Type": "application/json"},
        json={"source": url, "sourceType": "URL"}
    )
    result = resp.json()

    return result['summary']

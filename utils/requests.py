import requests
import os
import re
from filters import apply_filters

base_url = "https://api.ai21.com/studio/v1"

MODEL_CONF = {
    "maxTokens": 200,
    "temperature": 0.8,
    "numResults": 16
    # "logitBias": {'<|endoftext|>': -5}
}

def _full_url(model_type, custom_model, endpoint):
    return os.path.join(base_url, model_type, custom_model or '', endpoint)


def complete(model_type, prompt, config, api_key, custom_model=None):
    url = _full_url(model_type, custom_model, endpoint='complete')
    auth_header = f"Bearer {api_key}"
    resp = requests.post(
        url,
        headers={"Authorization": auth_header},
        json={"prompt": prompt, **config}
    )
    return resp.json()


def query(prompt, api_key, external=False):
    if external:
        if 'maxTokens' in MODEL_CONF:
            del MODEL_CONF['maxTokens']
        return complete(model_type="experimental/j1-compose",
                   prompt=prompt,
                   config=MODEL_CONF,
                   api_key=api_key)
    else:
        MODEL_CONF['prompt'] = prompt
        return requests.post('http://localhost:8080/sample', json=MODEL_CONF).json()


def generate(prompt, media, api_key, max_retries=2, top=3, external=False):
    completions_filtered = []
    try_count = 0
    while not len(completions_filtered) and try_count < max_retries:
        res = query(prompt, api_key=api_key, external=external)
        completions_filtered = [comp['data']['text'] for comp in res['completions']
                                if apply_filters(comp, prompt, media)]
        try_count += 1
    return completions_filtered[:top]


def text_segmentation(source, sourceType, api_key):
    url = 'http://api.ai21.com/studio/v1/segmentation'
    auth_header = f"Bearer {api_key}"
    resp = requests.post(
        url,
        headers={"Authorization": auth_header},
        json={"source": source, "sourceType": sourceType}
    )
    return resp.json()


def get_text_from_url(url, external=False):
    if not external:
        res = requests.get('http://localhost:5000/?url=' + url).json()
        return res['title'].strip(), re.sub('\n\n+', '\n\n', res['textContent'].strip())
    else:
        raise NotImplemented
        # res = text_segmentation(source=url, sourceType='URL', api_key=st.secrets['api-keys']['ai21-algo-team-prod'])


def tokenize(text, api_key):
    url = _full_url('', '', endpoint='tokenize')
    auth_header = f"Bearer {api_key}"
    res = requests.post(
        url,
        headers={"Authorization": auth_header},
        json={"text": text}
    )
    return res.json()['tokens']

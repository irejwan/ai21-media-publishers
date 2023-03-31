CHAR_LIMIT = {
    "Twitter": (30, 280),
    "Linkedin": (100, 1500),
}

max_tokens = 2048 - 300

MODEL_CONF = {
    "maxTokens": 200,
    "temperature": 0.8,
    "numResults": 16
    # "logitBias": {'<|endoftext|>': -5}
}

url_placeholder = "https://www.ai21.com/blog/introducing-j2"
apis = {
    'instruct': "https://api.ai21.com/studio/v1/j2-jumbo-instruct/complete",
    'summarize': 'https://api.ai21.com/studio/v1/summarize',
    'tokenize': 'https://api.ai21.com/studio/v1/tokenize'
}

import json
import os.path
from uuid import uuid4
import streamlit as st
from constants import *
from utils.requests import generate, get_text_from_url
from utils.string_utils import validate_email
from utils.style import *
import qrcode


external = False
api_key = st.secrets['api-keys']['ai21-algo-team-prod']


def on_next():
    st.session_state['index'] = (st.session_state['index'] + 1) % len(st.session_state['completions'])


def on_prev():
    st.session_state['index'] = (st.session_state['index'] - 1) % len(st.session_state['completions'])


def toolbar():
    cols = st.columns([0.35, 0.1, 0.1, 0.1, 0.35])
    with cols[1]:
        st.button(label='<', key='prev', on_click=on_prev)
    with cols[2]:
        st.text(f"{st.session_state['index'] + 1}/{len(st.session_state['completions'])}")
    with cols[3]:
        st.button(label="\>", key='next', on_click=on_next)


def refresh():
    del st.session_state['completions']


def save_to_file(data, external=False):
    if not external:
        base_dir = 'data'
        if not os.path.exists(base_dir):
            os.mkdir(base_dir)
        filename = os.path.join(base_dir, str(uuid4()) + '.json')

        with open(filename, "w") as f:
            json.dump(data, f)
    else:
        raise NotImplemented


def extract():
    url = st.session_state['url']
    st.session_state['title'], st.session_state['article'] = get_text_from_url(url, external=external)


def compose():
    article = st.session_state['article']
    media = st.session_state['media']
    post_type = "tweet" if media == "Twitter" else "Linkedin post"
    instruction = f"Write a {post_type} touting the following press release."
    prompt = f"{instruction}\nPress Release:\n{article}\n\n{media}:\n"

    with st.spinner("Loading..."):
        st.session_state["completions"] = generate(prompt, api_key=api_key, media=media)
        st.session_state['index'] = 0


def generate_qr(media, post, article_url):
    header = "I created this post using "
    if media == "Twitter":
        url = "https://twitter.com/intent/tweet?text="
        handle = "@AI21 Labs - The Publishing Show"
    else:
        url = "https://www.linkedin.com/post/edit/?text="
        handle = "@AI21_Publishers"
    url += header + handle + ":\n" + post + "\nRead more here:\n" + article_url
    url = url.replace(' ', '%20')

    qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_L)
    qr.add_data(url)
    qr.make()
    return qr.make_image(fill_color=textColor, back_color=text_background_color)


def main():
    apply_style()

    if 'completions' not in st.session_state:
        st.session_state['url'] = st.text_input(label="Enter your article URL", value=url_placeholder).strip()

        st.button(label='Extract', on_click=extract)

        if 'title' in st.session_state:
            st.markdown(f"The extracted article: **{st.session_state['title']}**")

            st.session_state['media'] = st.radio(
                "Generate me a post for 👉",
                options=['Linkedin', 'Twitter'],
                horizontal=True
            )

            st.button(label="Compose", on_click=compose)

    else:
        if len(st.session_state['completions']) == 0:
            st.write("Please try again 😔")

        else:
            curr_text = st.session_state['completions'][st.session_state['index']]
            st.text_area(label="Your awesome generated post", value=curr_text.strip(), height=200)
            if len(st.session_state['completions']) > 1:
                toolbar()

            img = generate_qr(st.session_state['media'], curr_text, st.session_state['url'])
            cols = st.columns([0.25, 0.5, 0.25])
            with cols[1]:
                st.image(img.get_image())

            email = st.text_input(label="Enter your Email to get this text").strip()

            if st.button(label="Send me a copy!"):
                data = {"email": email, "text": curr_text, **st.session_state}
                if not validate_email(email):
                    st.error("Please verify your email")
                else:
                    save_to_file(data, external=external)

            st.button(label="< Back", on_click=refresh)


if __name__ == '__main__':
    main()

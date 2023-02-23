import json
import streamlit as st
from constants import *
from utils.requests import generate, get_text_from_url
from utils.string_utils import validate_email
from utils.style import apply_style


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
        st.button(label='>', key='next', on_click=on_next)


def refresh():
    del st.session_state['completions']


def main():
    apply_style()

    st.session_state['url'] = st.text_input(label="Enter your article URL", value=url_placeholder).strip()

    if st.button(label='Extract', key='extract'):
        st.session_state['title'], st.session_state['article'] = get_text_from_url(st.session_state['url'])
    st.session_state['title'] = st.text_input(label="Your Article",
                                              value=st.session_state.get('title', title_placeholder)).strip()

    media = st.radio(
        "Generate me a post for 👉",
        options=['Linkedin', 'Twitter'],
        horizontal=True
    )

    article = st.session_state.get('article', article_placeholder)
    post_type = "tweet" if media == "Twitter" else "Linkedin post"
    instruction = f"Write a {post_type} touting the following press release."
    prompt = f"{instruction}\nPress Release:\n{article}\n\n{media}:\n"

    if st.button(label="Compose"):
        with st.spinner("Loading..."):
            st.session_state["completions"] = generate(prompt, api_key=api_key, media=media)
            st.session_state['index'] = 0

    if 'completions' in st.session_state:
        if len(st.session_state['completions']) == 0:
            st.write("Please try again 😔")

        else:
            curr_text = st.session_state['completions'][st.session_state['index']]
            st.text_area(label="Your awesome generated post", value=curr_text.strip(), height=200)
            if len(st.session_state['completions']) > 1:
                toolbar()

            email = st.text_input(label="Enter your Email to get this text").strip()
            if email and not validate_email(email):
                st.write("Please verify your email")
            if st.button(label="Send me a copy!"):
                with open('f.json') as f:
                    json.dump({"email": email, "url": st.session_state['url'], 'media': media, 'text': curr_text}, f)

            st.button(label="Reset 🔄", on_click=refresh)


if __name__ == '__main__':
    main()

from constants import *
from utils.requests import generate, summarize
from utils.style import *


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
    with cols[4]:
        st.button(label="🔄", on_click=lambda: compose())


def back():
    del st.session_state['completions']


def refresh():
    del st.session_state['url']
    del st.session_state['article']
    del st.session_state['completions']


def extract():
    with st.spinner("Summarizing article..."):
        try:
            url = st.session_state['url']
            st.session_state['article'] = summarize(url, api_key=api_key)
        except:
            st.session_state['article'] = False


def compose():
    with st.spinner("Generating post..."):
        st.session_state["completions"] = generate(st.session_state['article'], api_key=api_key,
                                                   media=st.session_state['media'])
        st.session_state['index'] = 0


def main():
    apply_style()

    if 'completions' not in st.session_state:
        st.session_state['url'] = st.text_input(label="Enter your article URL",
                                                value=st.session_state.get('url', url_placeholder)).strip()

        if st.button(label='Summarize'):
            extract()

        if 'article' in st.session_state:
            if not st.session_state['article']:
                st.write("This article is not supported, please try another one")

            else:
                st.text_area(label='Summary', value=st.session_state['article'], height=200)

                st.session_state['media'] = st.radio(
                    "Compose a post for this article for 👉",
                    options=['Twitter', 'Linkedin'],
                    horizontal=True
                )

                st.button(label="Compose", on_click=lambda: compose())

    else:
        if len(st.session_state['completions']) == 0:
            st.write("Please try again 😔")

        else:
            curr_text = st.session_state['completions'][st.session_state['index']]
            curr_text += "\n\nRead more here:\n" + st.session_state['url']
            st.text_area(label="Your awesome generated post", value=curr_text.strip(), height=200)
            if len(st.session_state['completions']) > 1:
                toolbar()

            img = generate_qr(st.session_state['media'], curr_text)
            cols = st.columns([0.3, 0.4, 0.3])
            with cols[1]:
                st.write("Scan the QR to post on " + st.session_state['media'])
                st.image(img.get_image())

        cols = st.columns([0.14, 0.2, 0.66])
        with cols[0]:
            st.button(label="⬅️ Back", on_click=back)
        with cols[1]:
            st.button(label="📄 Restart", on_click=refresh)


if __name__ == '__main__':
    main()

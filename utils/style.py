import urllib.parse
import qrcode
import streamlit as st

button_color = "#E91E63"
text_background_color = "#1c344d"
label_color = "#D9D9D9"
primaryColor = "#12202F"
backgroundColor = "#12202F"
textColor = "#D9D9D9"


def apply_style():
    st.image('./assets/Demo_header.png')
    s = f"""
    <style>
    div.stButton > button {{ background-color: {button_color}; color: {label_color} }}
    .stTextInput [data-baseweb=base-input] {{background-color: {text_background_color};}}
    .stTextArea [data-baseweb=base-input] {{background-color: {text_background_color};}}

    </style>
    """
    st.markdown(s, unsafe_allow_html=True)


def generate_qr(media, post):
    if media == "Twitter":
        header = "I created this tweet using "
        url = "https://twitter.com/intent/tweet?text="
        handle = "@AI21_Publishers"
        url += header + handle + ":\n" + post
        url = urllib.parse.quote_plus(url)
    else:
        url = "https://www.linkedin.com/"

    qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_L)
    qr.add_data(url)
    qr.make()
    return qr.make_image(fill_color=textColor, back_color=text_background_color)

import streamlit as st


def apply_style():
    st.image('./assets/Demo_header.png')
    button_color = "#E91E63"
    text_background_color = "#1c344d"
    label_color = "#D9D9D9"
    s = f"""
    <style>
    div.stButton > button {{ background-color: {button_color}; color: {label_color} }}
    .stTextInput [data-baseweb=base-input] {{background-color: {text_background_color};}}
    .stTextArea [data-baseweb=base-input] {{background-color: {text_background_color};}}

    </style>
    """
    st.markdown(s, unsafe_allow_html=True)
import streamlit as st
from pages import home, image_comprhension, grammar_fun, reading_translation

PAGES = {
    "Home": home,
    "Image Comprehension": image_comprhension,
    "Grammar and Fun": grammar_fun,
    "Reading and Translation": reading_translation
}

def main():
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(Pages.keys()))

    page = PAGES(selection)
    page.app()

if __name__ == "__main__":
    main()
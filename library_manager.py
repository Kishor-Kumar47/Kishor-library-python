import streamlit as st
import pandas as pd
import plotly.express as px
import json
import time
from streamlit_lottie import st_lottie

# Load Lottie animations
def load_lottie(url):
    with st.spinner("Loading animation..."):
        try:
            return json.loads(requests.get(url).text)
        except:
            return None

# Initialize session state for library if not exists
if "library" not in st.session_state:
    st.session_state.library = []

def save_book(title, author, genre, status):
    book = {"Title": title, "Author": author, "Genre": genre, "Status": status}
    st.session_state.library.append(book)
    st.success(f"'{title}' has been added to your library!")
    time.sleep(1)
    st.rerun()

def remove_book(title):
    st.session_state.library = [book for book in st.session_state.library if book["Title"] != title]
    st.success(f"'{title}' has been removed from your library!")
    time.sleep(1)
    st.rerun()

# UI Layout
st.set_page_config(page_title="Personal Library Manager", layout="wide")
st.title("📚 Personal Library Manager")
st.sidebar.header("Manage Your Books")

# Add Book Form
with st.sidebar.form("add_book_form"):
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    genre = st.selectbox("Genre", ["Fiction", "Non-Fiction", "Sci-Fi", "Fantasy", "Biography", "History", "Other"])
    status = st.selectbox("Reading Status", ["To Read", "Reading", "Completed"])
    submit = st.form_submit_button("Add Book")
    if submit and title and author:
        save_book(title, author, genre, status)
    elif submit:
        st.warning("Please fill in all fields.")

# Display Library
if st.session_state.library:
    df = pd.DataFrame(st.session_state.library)
    st.subheader("📖 Your Library")
    st.dataframe(df, use_container_width=True)

    # Book Removal
    book_to_remove = st.selectbox("Select a book to remove", [book["Title"] for book in st.session_state.library])
    if st.button("Remove Book"):
        remove_book(book_to_remove)

    # Library Statistics
    st.subheader("📊 Library Insights")
    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.histogram(df, x="Genre", title="Books by Genre", text_auto=True)
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        fig2 = px.pie(df, names="Status", title="Reading Status Distribution", hole=0.4)
        st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("Your library is empty. Start adding books!")

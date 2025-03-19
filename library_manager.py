import streamlit as st
import json
import os
from datetime import datetime
import time
from streamlit_lottie import st_lottie
import requests

# Set page configuration
st.set_page_config(
    page_title="Personal Library Manager",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Lottie animation
def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except requests.RequestException:
        return None

# Custom CSS
st.markdown("""
<style>
    .book-card {
        background: linear-gradient(135deg, #3b82f6, #1e3a8a);
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        color: white;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease-in-out;
    }
    .book-card:hover {
        transform: scale(1.05);
    }
    .book-title {
        font-size: 1.5rem;
        font-weight: bold;
    }
    .book-details {
        font-size: 1rem;
        opacity: 0.9;
    }
    .remove-button {
        background-color: #ef4444 !important;
        color: white !important;
        border-radius: 8px;
        padding: 8px 16px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'library' not in st.session_state:
    st.session_state.library = []
if 'search_results' not in st.session_state:
    st.session_state.search_results = []
if 'book_added' not in st.session_state:
    st.session_state.book_added = False
if 'book_removed' not in st.session_state:
    st.session_state.book_removed = False
if 'current_view' not in st.session_state:
    st.session_state.current_view = "view_library"

# Load library from JSON file
def load_library():
    if os.path.exists('library.json'):
        try:
            with open('library.json', 'r') as file:
                st.session_state.library = json.load(file)
        except json.JSONDecodeError:
            st.session_state.library = []
    else:
        st.session_state.library = []

# Save library to JSON file
def save_library():
    try:
        with open('library.json', 'w') as file:
            json.dump(st.session_state.library, file, indent=4)
    except Exception as e:
        st.error(f"Error saving library: {e}")

# Add a new book
def add_book(title, author, publication_year, genre, read_status):
    if not title.strip() or not author.strip():
        st.warning("Title and author fields cannot be empty.")
        return
    book = {
        'title': title,
        'author': author,
        'publication_year': int(publication_year),
        'genre': genre,
        'read_status': read_status,
        'added_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state.library.append(book)
    save_library()
    st.session_state.book_added = True
    time.sleep(0.5)

# Remove a book
def remove_book(index):
    if 0 <= index < len(st.session_state.library):
        del st.session_state.library[index]
        save_library()
        st.session_state.book_removed = True
        return True
    return False

# Load library on startup
load_library()

# Sidebar navigation
st.sidebar.markdown("<h1 style='text-align: center;'>📚 Navigation</h1>", unsafe_allow_html=True)
lottie_book = load_lottieurl("https://assets9.lottiefiles.com/temp/lf20_aKAfIn.json")
if lottie_book:
    with st.sidebar:
        st_lottie(lottie_book, height=200, key="book_animation")

nav_options = st.sidebar.radio("Choose an option:", ["View Library", "Add Book", "Search Books", "Library Statistics"])
st.session_state.current_view = nav_options.lower().replace(" ", "_")

# Main UI
st.markdown("<h1 style='text-align: center;'>Personal Library Manager</h1>", unsafe_allow_html=True)

if st.session_state.current_view == "view_library":
    st.markdown("<h2>Library Books</h2>")
    if not st.session_state.library:
        st.write("No books in library.")
    else:
        for i, book in enumerate(st.session_state.library):
            st.markdown(f"""
            <div class="book-card">
                <div class="book-title">{book['title']}</div>
                <div class="book-details">by {book['author']} ({book['publication_year']})</div>
                <div class="book-details">Genre: {book['genre']}</div>
                <div class="book-details">Status: {'✔ Read' if book['read_status'] == 'Read' else '❌ Unread'}</div>
                <div style='margin-top: 10px;'>
                    <button class='remove-button' onClick="window.location.reload();">Remove</button>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Remove {book['title']}", key=i):
                remove_book(i)

st.markdown("---")
st.markdown("© 2025 Kishor Kode Personal Library Manager", unsafe_allow_html=True)

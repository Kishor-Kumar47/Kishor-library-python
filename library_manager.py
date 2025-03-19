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

# Search books
def search_books(search_term, search_by):
    search_term = search_term.lower()
    st.session_state.search_results = [
        book for book in st.session_state.library if search_term in book[search_by].lower()
    ]

# Library statistics
def get_library_stats():
    total_books = len(st.session_state.library)
    read_books = sum(1 for book in st.session_state.library if book['read_status'] == "Read")
    percent_read = (read_books / total_books * 100) if total_books > 0 else 0
    return {'total_books': total_books, 'read_books': read_books, 'percent_read': percent_read}

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

if st.session_state.current_view == "add_book":
    st.markdown("<h2>Add a New Book</h2>")
    with st.form(key='add_book_form'):
        title = st.text_input("Book Title")
        author = st.text_input("Author")
        publication_year = st.number_input("Publication Year", min_value=1000, max_value=datetime.now().year, step=1)
        genre = st.selectbox("Genre", ["Fiction", "Non-Fiction", "Science", "Technology", "Fantasy", "Other"])
        read_status = st.radio("Read Status", ["Read", "Unread"])
        submit_button = st.form_submit_button("Add Book")
        if submit_button:
            add_book(title, author, publication_year, genre, read_status)

elif st.session_state.current_view == "search_books":
    st.markdown("<h2>Search Books</h2>")
    search_term = st.text_input("Enter search term")
    search_by = st.selectbox("Search by", ["title", "author", "genre"])
    if st.button("Search"):
        search_books(search_term, search_by)
    if st.session_state.search_results:
        for book in st.session_state.search_results:
            st.write(f"**{book['title']}** by {book['author']}")

elif st.session_state.current_view == "view_library":
    st.markdown("<h2>Library Books</h2>")
    if not st.session_state.library:
        st.write("No books in library.")
    else:
        for i, book in enumerate(st.session_state.library):
            st.write(f"**{book['title']}** by {book['author']} ({book['publication_year']}) - {book['genre']} - {'Read' if book['read_status'] else 'Unread'}")
            if st.button(f"Remove {book['title']}", key=i):
                remove_book(i)

elif st.session_state.current_view == "library_statistics":
    st.markdown("<h2>Library Statistics</h2>")
    stats = get_library_stats()
    st.metric("Total Books", stats['total_books'])
    st.metric("Books Read", stats['read_books'])
    st.metric("Percentage Read", f"{stats['percent_read']:.1f}%")

st.markdown("---")
st.markdown("© 2025 Kishor Kode Personal Library Manager", unsafe_allow_html=True)

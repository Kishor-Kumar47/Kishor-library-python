import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import time
import plotly.express as px
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import requests

# Set page configuration
st.set_page_config(
    page_title="Personal Library Manager",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for improved UI
st.markdown("""
    <style>
        .main-header {
            font-size: 3rem !important;
            color: #1E3A8A;
            font-weight: 700;
            margin-bottom: 1rem;
            text-align: center;
        }
        .sub-header {
            font-size: 1.8rem !important;
            color: #3B82F6;
            font-weight: 600;
            margin-top: 1rem;
            margin-bottom: 1rem;
        }
        .book-card {
            background: linear-gradient(to right, #F3F4F6, #E0E7FF);
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 15px;
            border-left: 6px solid #6366F1;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .book-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
        }
        .book-title {
            font-size: 1.4rem;
            font-weight: bold;
            color: #1E40AF;
        }
        .book-meta {
            font-size: 0.9rem;
            color: #374151;
        }
        .success-message {
            background-color: #D1FAE5;
            padding: 10px;
            border-left: 5px solid #10B981;
            border-radius: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# Load Lottie animation
def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
    except:
        return None
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
    st.session_state.current_view = "library"

# Load library from JSON file safely
def load_library():
    if os.path.exists('library.json'):
        try:
            with open('library.json', 'r') as file:
                data = file.read().strip()
                st.session_state.library = json.loads(data) if data else []
        except (json.JSONDecodeError, ValueError):
            st.session_state.library = []
            st.warning("⚠ Library file was corrupted. Resetting...")
            save_library()

# Save library to JSON file
def save_library():
    try:
        with open('library.json', 'w') as file:
            json.dump(st.session_state.library, file, indent=4)
    except Exception as e:
        st.error(f"❌ Error saving library: {e}")

# Add a new book
def add_book(title, author, publication_year, genre, read_status):
    book = {
        'title': title,
        'author': author,
        'publication_year': publication_year,
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
    results = [book for book in st.session_state.library if search_term in book[search_by.lower()].lower()]
    st.session_state.search_results = results

# Load library on startup
load_library()

# Sidebar navigation
st.sidebar.markdown("<h1 style='text-align: center;'>📚 Navigation</h1>", unsafe_allow_html=True)

lottie_book = load_lottieurl("https://assets9.lottiefiles.com/temp/lf20_aKAfIn.json")
if lottie_book:
    with st.sidebar:
        st_lottie(lottie_book, height=200, key="book_animation")

nav_options = st.sidebar.radio(
    "Choose an option:",
    ["View Library", "Add Book", "Search Books"]
)

st.session_state.current_view = nav_options.lower().replace(" ", "_")

# Main UI
st.markdown("<h1 class='main-header'>Personal Library Manager</h1>", unsafe_allow_html=True)

if st.session_state.current_view == "add_book":
    st.markdown("<h2 class='sub-header'>📖 Add a New Book</h2>", unsafe_allow_html=True)
    
    with st.form(key='add_book_form'):
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("Book Title")
            author = st.text_input("Author")
            publication_year = st.number_input("Publication Year", min_value=1000, max_value=datetime.now().year, step=1)
        with col2:
            genre = st.selectbox("Genre", ["Fiction", "Non-Fiction", "Science", "Technology", "Fantasy", "Other"])
            read_status = st.radio("Read Status", ["Read", "Unread"])
        
        submit_button = st.form_submit_button(label="📥 Add Book")
        if submit_button and title and author:
            add_book(title, author, publication_year, genre, read_status == "Read")
            st.success("✅ Book added successfully!")

elif st.session_state.current_view == "view_library":
    st.markdown("<h2 class='sub-header'>📚 Your Library</h2>", unsafe_allow_html=True)
    
    if not st.session_state.library:
        st.warning("No books in your library. Add some books to get started! 📖")
    else:
        for index, book in enumerate(st.session_state.library):
            with st.container():
                st.markdown(f"""
                    <div class="book-card">
                        <p class="book-title">{book['title']}</p>
                        <p class="book-meta">📖 Author: {book['author']}</p>
                        <p class="book-meta">📅 Year: {book['publication_year']} | 📂 Genre: {book['genre']}</p>
                        <p class="book-meta">✅ Status: {'Read' if book['read_status'] else 'Unread'}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"🗑 Remove {book['title']}", key=f"remove_{index}"):
                    remove_book(index)
                    st.experimental_rerun()

elif st.session_state.current_view == "search_books":
    st.markdown("<h2 class='sub-header'>🔍 Search Books</h2>", unsafe_allow_html=True)
    search_term = st.text_input("Enter search term:")
    search_by = st.selectbox("Search by:", ["Title", "Author"])
    
    if st.button("🔍 Search"):
        search_books(search_term, search_by)
    
    if st.session_state.search_results:
        for book in st.session_state.search_results:
            st.markdown(f"""
                <div class="book-card">
                    <p class="book-title">{book['title']}</p>
                    <p class="book-meta">📖 Author: {book['author']}</p>
                </div>
            """, unsafe_allow_html=True)

st.markdown("© 2025 Personal Library Manager", unsafe_allow_html=True)

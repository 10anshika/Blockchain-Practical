import streamlit as st
import pandas as pd
import json
import os

# ---------- JSON Persistence Helpers ----------
def load_data(file_name, default):
    if os.path.exists(file_name):
        with open(file_name, 'r') as f:
            return json.load(f)
    return default

def save_data(file_name, data):
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4)

# ---------- Load Session State from JSON ----------
if 'books' not in st.session_state:
    st.session_state.books = load_data('books.json', {})
if 'users' not in st.session_state:
    st.session_state.users = load_data('users.json', {})
if 'ledger' not in st.session_state:
    st.session_state.ledger = load_data('ledger.json', [])

# ---------- Function to Display Ledger ----------
def display_ledger():
    if not st.session_state.ledger:
        st.info("No transactions yet.")
        return
    df = pd.DataFrame(st.session_state.ledger, columns=["Book ID", "Book Title", "User ID", "User Name", "Action"])
    st.dataframe(df, use_container_width=True)

# ---------- Title ----------
st.title("📚 Library Book Issuing Ledger")

# ---------- Sidebar: Add Book ----------
st.sidebar.header("➕ Add Book")
book_id = st.sidebar.text_input("Book ID")
book_title = st.sidebar.text_input("Book Title")
if st.sidebar.button("Add Book"):
    if book_id and book_title:
        if book_id in st.session_state.books:
            st.sidebar.warning("Book ID already exists!")
        else:
            st.session_state.books[book_id] = {
                'title': book_title,
                'issued_to': None
            }
            save_data('books.json', st.session_state.books)
            st.sidebar.success(f"Added book '{book_title}'")
    else:
        st.sidebar.warning("Enter both Book ID and Title")

# ---------- Sidebar: Add User ----------
st.sidebar.header("➕ Add User")
user_id = st.sidebar.text_input("User ID")
user_name = st.sidebar.text_input("User Name")
if st.sidebar.button("Add User"):
    if user_id and user_name:
        if user_id in st.session_state.users:
            st.sidebar.warning("User ID already exists!")
        else:
            st.session_state.users[user_id] = user_name
            save_data('users.json', st.session_state.users)
            st.sidebar.success(f"Added user '{user_name}'")
    else:
        st.sidebar.warning("Enter both User ID and Name")

# ---------- Main: Issue a Book ----------
st.header("📦 Issue a Book")
available_books = [bid for bid in st.session_state.books if st.session_state.books[bid]['issued_to'] is None]
if available_books and st.session_state.users:
    with st.form("issue_form"):
        selected_book = st.selectbox("Select Book to Issue", available_books)
        selected_user = st.selectbox("Select User", list(st.session_state.users.keys()))
        issue_submit = st.form_submit_button("Issue Book")
        if issue_submit:
            st.session_state.books[selected_book]['issued_to'] = selected_user
            st.session_state.ledger.append([
                selected_book,
                st.session_state.books[selected_book]['title'],
                selected_user,
                st.session_state.users[selected_user],
                "Issued"
            ])
            save_data('books.json', st.session_state.books)
            save_data('ledger.json', st.session_state.ledger)
            st.success(f"Issued '{st.session_state.books[selected_book]['title']}' to {st.session_state.users[selected_user]}")
else:
    st.warning("No available books or users to issue.")

# ---------- Main: Return a Book ----------
st.header("🔄 Return a Book")
issued_books = [bid for bid in st.session_state.books if st.session_state.books[bid]['issued_to']]
if issued_books:
    with st.form("return_form"):
        return_book = st.selectbox("Select Book to Return", issued_books)
        return_submit = st.form_submit_button("Return Book")
        if return_submit:
            uid = st.session_state.books[return_book]['issued_to']
            st.session_state.books[return_book]['issued_to'] = None
            st.session_state.ledger.append([
                return_book,
                st.session_state.books[return_book]['title'],
                uid,
                st.session_state.users[uid],
                "Returned"
            ])
            save_data('books.json', st.session_state.books)
            save_data('ledger.json', st.session_state.ledger)
            st.success(f"Returned '{st.session_state.books[return_book]['title']}' by {st.session_state.users[uid]}")
else:
    st.info("No books currently issued.")

# ---------- Main: Display Ledger ----------
st.header("📒 Transaction Ledger")
display_ledger()

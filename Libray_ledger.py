import streamlit as st
import pandas as pd

# Initialize session state
if 'books' not in st.session_state:
    st.session_state.books = {}
if 'users' not in st.session_state:
    st.session_state.users = {}
if 'ledger' not in st.session_state:
    st.session_state.ledger = []

# Function to display the ledger
def display_ledger():
    if not st.session_state.ledger:
        st.info("No transactions yet.")
        return

    df = pd.DataFrame(st.session_state.ledger, columns=["Book ID", "Book Title", "User ID", "User Name", "Action"])
    st.dataframe(df, use_container_width=True)

st.title("📚 Library Book Issuing Ledger")

st.sidebar.header("➕ Add Book")
book_id = st.sidebar.text_input("Book ID")
book_title = st.sidebar.text_input("Book Title")
if st.sidebar.button("Add Book"):
    if book_id and book_title:
        st.session_state.books[book_id] = {
            'title': book_title,
            'issued_to': None
        }
        st.sidebar.success(f"Added book '{book_title}'")
    else:
        st.sidebar.warning("Enter both Book ID and Title")

st.sidebar.header("➕ Add User")
user_id = st.sidebar.text_input("User ID")
user_name = st.sidebar.text_input("User Name")
if st.sidebar.button("Add User"):
    if user_id and user_name:
        st.session_state.users[user_id] = user_name
        st.sidebar.success(f"Added user '{user_name}'")
    else:
        st.sidebar.warning("Enter both User ID and Name")

st.header("📦 Issue a Book")
with st.form("issue_form"):
    selected_book = st.selectbox("Select Book to Issue", [bid for bid in st.session_state.books if st.session_state.books[bid]['issued_to'] is None])
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
        st.success(f"Issued '{st.session_state.books[selected_book]['title']}' to {st.session_state.users[selected_user]}")

st.header("🔄 Return a Book")
with st.form("return_form"):
    issued_books = [bid for bid in st.session_state.books if st.session_state.books[bid]['issued_to']]
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
        st.success(f"Returned '{st.session_state.books[return_book]['title']}' by {st.session_state.users[uid]}")

st.header("📒 Transaction Ledger")
display_ledger()

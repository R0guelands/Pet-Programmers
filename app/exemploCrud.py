import streamlit as st
import sqlite3

# Create a connection to the database
conn = sqlite3.connect('data.db')
c = conn.cursor()

# Create a table if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL
    )
''')

# Streamlit app
def main():
    st.title('SQLite CRUD App')

    menu = ['Create', 'Read', 'Update', 'Delete']
    choice = st.sidebar.selectbox('Select Operation', menu)

    if choice == 'Create':
        st.header('Create User')
        name = st.text_input('Name')
        email = st.text_input('Email')
        if st.button('Add User'):
            if name and email:
                create_user(name, email)
                st.success('User added successfully!')
            else:
                st.warning('Please enter both name and email.')

    elif choice == 'Read':
        st.header('View Users')
        users = read_users()
        if users:
            for user in users:
                st.write(f"Name: {user[1]}, Email: {user[2]}")
        else:
            st.info('No users found.')

    elif choice == 'Update':
        st.header('Update User')
        users = read_users()
        if users:
            user_names = [user[1] for user in users]
            selected_name = st.selectbox('Select User', user_names)
            new_email = st.text_input('New Email')
            if st.button('Update Email'):
                if new_email:
                    update_user(selected_name, new_email)
                    st.success('Email updated successfully!')
                else:
                    st.warning('Please enter a new email.')
        else:
            st.info('No users found.')

    elif choice == 'Delete':
        st.header('Delete User')
        users = read_users()
        if users:
            user_names = [user[1] for user in users]
            selected_name = st.selectbox('Select User', user_names)
            if st.button('Delete User'):
                delete_user(selected_name)
                st.success('User deleted successfully!')
        else:
            st.info('No users found.')

# Function to create a new user
def create_user(name, email):
    c.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
    conn.commit()

# Function to read all users
def read_users():
    c.execute('SELECT * FROM users')
    return c.fetchall()

# Function to update a user's email
def update_user(name, new_email):
    c.execute('UPDATE users SET email=? WHERE name=?', (new_email, name))
    conn.commit()

# Function to delete a user
def delete_user(name):
    c.execute('DELETE FROM users WHERE name=?', (name,))
    conn.commit()

if __name__ == '__main__':
    main()

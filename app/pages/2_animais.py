import sqlite3
import streamlit as st
import pandas as pd

# Create a connection to the database
conn = sqlite3.connect('data.db')
c = conn.cursor()

# Create a table if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS pets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        color TEXT NOT NULL,
        kg REAL NOT NULL,
        characteristics TEXT
    );
''')



# Streamlit app
def main():
    st.title('Animais')

    menu = ['Cadastrar', 'Procurar', 'Atualizar', 'Excluir']
    choice = st.sidebar.selectbox('Select Operation', menu)

    if choice == 'Cadastrar':
        st.header('Cadastre o novo animal')
        name = st.text_input('Nome')
        color = st.text_input('Cor')
        kg = st.text_input('Kg')
        characteristics = st.text_input('Caracteristicas')
        if st.button('Add Animal'):
            if name and color and kg:
                create_animal(name, color,kg,characteristics)
                st.success('Animal cadastrado com sucesso!')
            else:
                st.warning('Por favor, insira nome,cor,kg.')

    elif choice == 'Procurar':
        st.header('Visualização dos Animais')
        animals = read_animal()
        if animals:
            df = pd.DataFrame(animals,columns=['Id','Nome','Cor','KG','Características'])
            df_styled = df.style.format({'KG': '{:.1f}'})
            st.table(df_styled)
        else:
            st.info('No users found.')

    elif choice == 'Atualizar':
        st.header('Atualizar cadastro Animais')
        animals = read_animal()
        if animals:
            options = [f'{animal[0]} - {animal[1]} 'for animal in animals]
            selected_animal = st.selectbox('Selecione o animal',options)
            new_characters = st.text_input('Nova caracteristica')
            if st.button('Atualizar'):
                if new_characters:
                    update_animal(selected_animal[0], new_characters)
                    st.success('updated successfully!')
                else:
                    st.warning('Please enter a new email.')
        else:
            st.info('No users found.')

    elif choice == 'Excluir':
        st.header('Excluir Animal')
        animals = read_animal()
        if animals:
            options = [f'{animal[0]} - {animal[1]} ' for animal in animals]
            selected_animal = st.selectbox('Selecione o Animal', options)
            if st.button('Deletar Animal'):
                delete_animal(selected_animal[0])
                st.success('User deleted successfully!')
        else:
            st.info('No users found.')

# Function to create a new user
def create_animal(name, color,kg,characteristics):
    c.execute('INSERT INTO pets (name, color,kg,characteristics) VALUES (?, ?, ?, ?)', (name, color ,kg,characteristics ))
    conn.commit()

# Function to read all users
def read_animal():
    c.execute('SELECT * FROM pets')
    return c.fetchall()

# Function to update a user's email
def update_animal(id, new_characters):
    c.execute('UPDATE pets SET characteristics = ? WHERE id = ?', (new_characters, id))
    conn.commit()

# Function to delete a user
def delete_animal(id):
    c.execute('DELETE FROM pets WHERE id=?', (id))
    conn.commit()

if __name__ == '__main__':
    main()

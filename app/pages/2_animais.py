import sqlite3
import streamlit as st
import pandas as pd

# Create a connection to the database
conn = sqlite3.connect('data.db')
c = conn.cursor()
# Create a table if it doesn't exist
query= ('''
    CREATE TABLE IF NOT EXISTS pets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        color TEXT NOT NULL,
        kg REAL NOT NULL,
        characteristics TEXT
    );
''')
conn.execute(query)

query = ('''
    CREATE TABLE IF NOT EXISTS vaccine (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        idPets INTEGER NOT NULL,
        FEREIGN KEY idPets REFERENCES pets(id)
    );
''')
conn.execute(query)

# Streamlit app
def main():
    # c.execute('DELETE FROM vaccine')
    # conn.commit()
    st.title('Animais')
    menu = ['Cadastrar Animais','Cadastrar Vacinas', 'Procurar', 'Atualizar', 'Excluir']
    choice = st.sidebar.selectbox('Seleciona a operação', menu)
# ----------------------------CADASTRO ANIMAIS----------------------------
    if choice == 'Cadastrar Animais':
        st.header('Cadastre o novo animal')
        name = st.text_input('Nome')
        color = st.text_input('Cor')
        kg = st.text_input('Kg')
        characteristics = st.text_input('Caracteristicas')
        if st.button('Adicionar Animal'):
            if name and color and kg:
                create_animal(name, color,kg,characteristics)
                st.success('Animal cadastrado com sucesso!')
            else:
                st.warning('Por favor, insira nome,cor,kg.')
# ----------------------------CADASTRO VACINAS----------------------------
    elif choice == 'Cadastrar Vacinas':
        st.header('Cadastre as vacinas nos animais')
        animals = read_animal()
        if animals:
            options = [f'{animal[0]} - {animal[1]}' for animal in animals]
            selected_animal = st.selectbox('Selecione o animal ',options)
            name = st.text_input('Nome da vacina')
            id = selected_animal.split('-')[0].strip() 
            if st.button('Cadastrar'):
                if name:
                    create_vaccine(name,id)
                    st.success('Cadastro Realizado com sucesso')
                else:
                    st.success('Erro ao cadastrar')
# ----------------------------PROCURAR----------------------------
    elif choice == 'Procurar':
        st.header('Visualização dos Animais')
        animals = read_animal()
        vaccine = read_animal_vaccine()
        if animals or vaccine:
            df_animals = pd.DataFrame(animals,columns=['Id','Nome','Cor','KG','Características'])
            df_styled = df_animals.style.format({'KG': '{:.1f}'})
            st.table(df_styled)
            st.header('Vacinas Aplicadas')
            st.caption('Filtros')
            checkbox_name = st.checkbox('Nome')
            checkbox_vaccine = st.checkbox('Vacina')
            if checkbox_name:
                animal = read_animal_vaccine()
                if animal:
                    options = set()
                    for a in animal:
                        option = f'{a[0]} - {a[1]}'
                        options.add(option)
                    options = list(options)  # Converter o conjunto de volta para uma lista
                    selected_animal = st.selectbox('Selecione o animal', options)
                    id = selected_animal.split('-')[0].strip()
                    result = search_animal_id(id)
                    df_final = pd.DataFrame(result, columns=['Id', 'Nome', 'Vacina'])
                    st.table(df_final)
            elif checkbox_vaccine:
               vaccine = read_vaccine()
               if vaccine:
                    options = set()
                    for v in vaccine:
                        option = f'{v[0]} - {v[1]}'
                        options.add(option)
                    options = list(options)  # Converter o conjunto de volta para uma lista
                    selected_vaccine = st.selectbox('Selecione o animal', options)
                    id = selected_vaccine.split('-')[0].strip()
                    result = search_animal_vaccine(id)
                    df_final = pd.DataFrame(result, columns=['Id', 'Nome', 'Vacina'])
                    st.table(df_final)

            else:
                animals = read_animal_vaccine()
                df_vaccine = pd.DataFrame(animals,columns=['Id','Nome','Vacina'])
                st.table(df_vaccine)
        else:
            st.info('No animals found.')
# ----------------------------ATUALIZAR----------------------------
    elif choice == 'Atualizar':
        st.header('Atualizar cadastro Animais')
        animals = read_animal()
        if animals:
            options = [f'{animal[0]} - {animal[1]} 'for animal in animals]
            selected_animal = st.selectbox('Selecione o animal',options)
            id = selected_animal.split('-')[0].strip() 
            new_characters = st.text_input('Nova caracteristica')
            if st.button('Atualizar'):
                if new_characters:
                    update_animal(id, new_characters)
                    st.success('updated successfully!')
                else:
                    st.warning('Please enter a new email.')
        else:
            st.info('No users found.')
# ----------------------------EXCLUIR----------------------------
    elif choice == 'Excluir':
        st.header('Excluir Animal')
        animals = read_animal()
        if animals:
            options = [f'{animal[0]} - {animal[1]} ' for animal in animals]
            selected_animal = st.selectbox('Selecione o Animal', options)
            id = selected_animal.split('-')[0].strip() 
            if st.button('Excluir'):
                delete_animal(id)
                delete_animal_vaccine(id)
                st.success('User deleted successfully!')
        else:
            st.info('No users found.')

# Function to create a new user
def create_animal(name, color,kg,characteristics):
    c.execute('INSERT INTO pets (name, color,kg,characteristics) VALUES (?, ?, ?, ?)', (name, color ,kg,characteristics ))
    conn.commit()

def create_vaccine(name,id):
    c.execute('INSERT INTO vaccine (name,idPets) VALUES (?,?)',(name,id,))
    conn.commit()

# Function to read all users
def read_animal():
    c.execute('SELECT * FROM pets')
    return c.fetchall()

def read_animal_vaccine():
    c.execute('SELECT p.id, p.name, v.name FROM pets p INNER JOIN vaccine v ON p.id = v.idPets')
    return c.fetchall()

def search_animal_id(id):
    c.execute('SELECT p.id, p.name, v.name FROM pets p INNER JOIN vaccine v ON p.id = v.idPets WHERE p.id = ?',(id,))
    return c.fetchall()

def search_animal_vaccine(vaccine):
    c.execute('SELECT p.id, p.name, v.name FROM pets p INNER JOIN vaccine v ON p.id = v.idPets WHERE v.id = ?',(vaccine,))
    return c.fetchall()

def read_vaccine():
    c.execute('SELECT id,name,idPets FROM vaccine')
    return c.fetchall()

# Function to update a user's email
def update_animal(id, new_characters):
    c.execute('UPDATE pets SET characteristics = ? WHERE id = ?', (new_characters, id,))
    conn.commit()

# Function to delete a user
def delete_animal(id):
    c.execute('DELETE FROM pets WHERE id=?', (id,))
    conn.commit()

def delete_animal_vaccine(id):
    c.execute('DELETE FROM vaccine WHERE id = ?', (id,))
    conn.commit()

if __name__ == '__main__':
    main()

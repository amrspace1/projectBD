
import streamlit as st
import sqlite3
import pandas as pd

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

st.title("Gestion d'Hôtel - Projet BD 2025")

menu = st.sidebar.selectbox("Menu", ["Clients", "Réservations", "Chambres disponibles", "Ajouter un client", "Ajouter une réservation"])

if menu == "Clients":
    st.subheader("Liste des clients")
    df = pd.read_sql_query("SELECT * FROM Client", conn)
    st.dataframe(df)

elif menu == "Réservations":
    st.subheader("Liste des réservations")
    df = pd.read_sql_query("""
        SELECT R.id, C.nom, R.date_debut, R.date_fin, CH.numero, H.ville
        FROM Reservation R
        JOIN Client C ON R.id_client = C.id
        JOIN Chambre CH ON R.id_chambre = CH.id
        JOIN Hotel H ON CH.id_hotel = H.id
    """, conn)
    st.dataframe(df)

elif menu == "Chambres disponibles":
    st.subheader("Chambres disponibles")
    date_debut = st.date_input("Date de début")
    date_fin = st.date_input("Date de fin")
    if st.button("Rechercher"):
        query = """
            SELECT * FROM Chambre WHERE id NOT IN (
                SELECT id_chambre FROM Reservation
                WHERE date_debut < ? AND date_fin > ?
            )
        """
        df = pd.read_sql_query(query, conn, params=(str(date_fin), str(date_debut)))
        st.dataframe(df)

elif menu == "Ajouter un client":
    st.subheader("Nouveau client")
    nom = st.text_input("Nom")
    adresse = st.text_input("Adresse")
    ville = st.text_input("Ville")
    code_postal = st.number_input("Code postal", step=1)
    email = st.text_input("Email")
    telephone = st.text_input("Téléphone")
    if st.button("Ajouter"):
        cursor.execute("INSERT INTO Client (adresse, ville, code_postal, email, telephone, nom) VALUES (?, ?, ?, ?, ?, ?)",
                       (adresse, ville, code_postal, email, telephone, nom))
        conn.commit()
        st.success("Client ajouté avec succès!")

elif menu == "Ajouter une réservation":
    st.subheader("Nouvelle réservation")
    id_client = st.number_input("ID client", step=1)
    id_chambre = st.number_input("ID chambre", step=1)
    date_debut = st.date_input("Date de début")
    date_fin = st.date_input("Date de fin")
    if st.button("Réserver"):
        cursor.execute("INSERT INTO Reservation (date_debut, date_fin, id_client, id_chambre) VALUES (?, ?, ?, ?)",
                       (str(date_debut), str(date_fin), id_client, id_chambre))
        conn.commit()
        st.success("Réservation ajoutée avec succès!")

conn.close()

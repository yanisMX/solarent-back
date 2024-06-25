import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Informations de connexion à la base de données Neon
PGHOST = 'ep-holy-hall-a2zqeezj.eu-central-1.aws.neon.tech'
PGDATABASE = 'solarent_db'
PGUSER = 'solarent_db_owner'
PGPASSWORD = 'gZQYT7hzo9qM'

DATABASE_URL = f"postgresql+psycopg2://{PGUSER}:{PGPASSWORD}@{PGHOST}/{PGDATABASE}"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

installations_csv = "C:\\Users\\Florian PESCOT\\OneDrive - DUPUY\\Bureau\\COURS\\bdd\\installations-de-production-solaire-par-commune.csv"
ensoleillement_csv = "C:\\Users\\Florian PESCOT\\OneDrive - DUPUY\\Bureau\\COURS\\bdd\\temps-densoleillement-par-an-par-departement-feuille-1.csv"

installations_df = pd.read_csv(installations_csv, delimiter=';')
ensoleillement_df = pd.read_csv(ensoleillement_csv, delimiter=',')

# Renommer les colonnes
installations_df.rename(columns={
    '1_f_commune_pdl': 'city_name',
    '1_f_code_insee_pdl': 'city_code',
    'dep': 'departement_code',
    'nom_dept': 'departement_name',
    'reg': 'state_code',
    'nom_reg': 'state_name',
    'count': 'count',
    'date_des_donnees': 'date',
    's_3_prod_i_regime_d_exploitation': 'exploitation',
    'sum_3_prod_e_kw_puissance_de_raccordement_injection': 'puissance',
    'coordonnees': 'coordinates'
}, inplace=True)

# Ajouter une colonne code_name
installations_df['code_name'] = installations_df['city_name'] + "_" + installations_df['city_code'].astype(str)

# Calculer le total_count par city
city_total_counts = installations_df.groupby('code_name')['count'].sum().reset_index()
city_total_counts.rename(columns={'count': 'total_count'}, inplace=True)

# Joindre les total_count au DataFrame installations_df
installations_df = installations_df.merge(city_total_counts, on='code_name')

# Préparer le DataFrame des départements
departments_df = installations_df[['departement_code', 'departement_name']].drop_duplicates()
departments_df = departments_df.merge(ensoleillement_df, left_on='departement_name', right_on=ensoleillement_df.columns[0])
departments_df.rename(columns={
    'departement_code': 'code',
    'departement_name': 'name',
    ensoleillement_df.columns[1]: 'sun_rate'
}, inplace=True)
departments_df.drop(columns=[ensoleillement_df.columns[0]], inplace=True)  # Supprimer la colonne inutile

# Préparer le DataFrame des états
states_df = installations_df[['state_code', 'state_name']].drop_duplicates()
states_df.rename(columns={
    'state_code': 'code',
    'state_name': 'name'
}, inplace=True)

# Préparer le DataFrame des villes
cities_df = installations_df[['code_name', 'city_name', 'coordinates', 'total_count', 'departement_code', 'state_code']]
cities_df.drop_duplicates(inplace=True)
cities_df.rename(columns={
    'code_name': 'code_name',
    'city_name': 'name',
    'coordinates': 'coordinates',
    'total_count': 'total_count',
    'departement_code': 'departement_code',  # Comme clé étrangère
    'state_code': 'state_code'  # Comme clé étrangère
}, inplace=True)

# Préparer le DataFrame des projets
projects_df = installations_df[['code_name', 'count', 'date', 'puissance', 'exploitation']]
projects_df.rename(columns={
    'code_name': 'city_code'  # Comme clé étrangère
}, inplace=True)

# Insérer les données dans la base de données
states_df.to_sql('state', engine, if_exists='append', index=False)
departments_df.to_sql('department', engine, if_exists='append', index=False)
cities_df.to_sql('city', engine, if_exists='append', index=False)
projects_df.to_sql('project', engine, if_exists='append', index=False)

print("Données insérées avec succès.")

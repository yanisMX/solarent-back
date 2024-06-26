import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session

# Informations de connexion à la base de données Neon
PGHOST = 'ep-holy-hall-a2zqeezj.eu-central-1.aws.neon.tech'
PGDATABASE = 'solarent_db'
PGUSER = 'solarent_db_owner'
PGPASSWORD = 'gZQYT7hzo9qM'

DATABASE_URL = f"postgresql+psycopg2://{PGUSER}:{PGPASSWORD}@{PGHOST}/{PGDATABASE}"

engine = create_engine(DATABASE_URL)
Session = scoped_session(sessionmaker(bind=engine))
session = Session()

# Vérifier la connexion à la base de données
try:
    connection = engine.connect()
    print("Connexion à la base de données réussie.")
    connection.close()
except Exception as e:
    print(f"Erreur de connexion : {e}")

# Chargement des fichiers CSV
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

# Convertir les colonnes code et departement_code en chaînes de caractères
installations_df['state_code'] = installations_df['state_code'].astype(str)
installations_df['departement_code'] = installations_df['departement_code'].astype(str)

# Ajouter une colonne code_name
installations_df['code_name'] = installations_df['city_name'] + "_" + installations_df['city_code'].astype(str)

# Calculer le total_count par city
city_total_counts = installations_df.groupby('code_name')['count'].sum().reset_index()
city_total_counts.rename(columns={'count': 'total_count'}, inplace=True)

# Joindre les total_count au DataFrame installations_df
installations_df = installations_df.merge(city_total_counts, on='code_name')

# Préparer le DataFrame des départements
departments_df = installations_df[['departement_code', 'departement_name']].drop_duplicates().copy()
departments_df = departments_df.merge(ensoleillement_df, left_on='departement_name', right_on=ensoleillement_df.columns[0])
departments_df.rename(columns={
    'departement_code': 'code',
    'departement_name': 'name',
    ensoleillement_df.columns[1]: 'sun_rate'
}, inplace=True)
departments_df.drop(columns=[ensoleillement_df.columns[0]], inplace=True)  # Supprimer la colonne inutile

# Convertir la colonne code en chaîne de caractères
departments_df['code'] = departments_df['code'].astype(str)

# Préparer le DataFrame des états
states_df = installations_df[['state_code', 'state_name']].drop_duplicates().copy()
states_df.rename(columns={
    'state_code': 'code',
    'state_name': 'name'
}, inplace=True)

# Convertir la colonne code en chaîne de caractères
states_df['code'] = states_df['code'].astype(str)

# Préparer le DataFrame des villes
cities_df = installations_df[['code_name', 'city_name', 'coordinates', 'total_count', 'departement_code', 'state_code']].drop_duplicates().copy()
cities_df.rename(columns={
    'code_name': 'code_name',
    'city_name': 'name',
    'coordinates': 'coordinates',
    'total_count': 'total_count',
    'departement_code': 'departement_code',  # Comme clé étrangère
    'state_code': 'state_code'  # Comme clé étrangère
}, inplace=True)

# Filtrer les villes dont le departement_code n'existe pas dans departments_df
valid_departments = departments_df['code'].unique()
cities_df = cities_df[cities_df['departement_code'].isin(valid_departments)]

# Préparer le DataFrame des projets
projects_df = installations_df[['code_name', 'count', 'date', 'puissance', 'exploitation']].copy()
projects_df.rename(columns={
    'code_name': 'city_code'  # Comme clé étrangère
}, inplace=True)

# Convertir les dates au format YYYY-MM-DD
projects_df['date'] = projects_df['date'].apply(lambda x: x + '-01' if pd.notnull(x) else None)

# Remplacer les NaN par des valeurs par défaut appropriées
projects_df['exploitation'] = projects_df['exploitation'].fillna('Unknown')
projects_df['puissance'] = projects_df['puissance'].fillna(0)

# Filtrer les projets dont le city_code n'existe pas dans cities_df
valid_city_codes = cities_df['code_name'].unique()
projects_df = projects_df[projects_df['city_code'].isin(valid_city_codes)]

# Afficher les DataFrames pour vérification
print("States DataFrame:")
print(states_df.head())

print("Departments DataFrame:")
print(departments_df.head())

print("Cities DataFrame:")
print(cities_df.head())

print("Projects DataFrame:")
print(projects_df.head())

# Assertions pour vérifier que les DataFrames ne sont pas vides
assert not states_df.empty, "States DataFrame est vide"
assert not departments_df.empty, "Departments DataFrame est vide"
assert not cities_df.empty, "Cities DataFrame est vide"
assert not projects_df.empty, "Projects DataFrame est vide"

# ORM Setup
Base = declarative_base()

class State(Base):
    __tablename__ = 'state'
    code = Column(String, primary_key=True)
    name = Column(String)

class Department(Base):
    __tablename__ = 'department'
    code = Column(String, primary_key=True)
    name = Column(String)
    sun_rate = Column(Float)

class City(Base):
    __tablename__ = 'city'
    code_name = Column(String, primary_key=True)
    name = Column(String)
    coordinates = Column(String)
    total_count = Column(Integer)
    departement_code = Column(String, ForeignKey('department.code'))
    state_code = Column(String, ForeignKey('state.code'))

class Project(Base):
    __tablename__ = 'project'
    id = Column(Integer, primary_key=True, autoincrement=True)
    count = Column(Integer)
    date = Column(Date)
    puissance = Column(Float)
    exploitation = Column(String)
    city_code = Column(String, ForeignKey('city.code_name'))

Base.metadata.drop_all(engine)  # Supprimer les tables existantes pour les recréer
Base.metadata.create_all(engine)  # Créer les tables avec la nouvelle définition

# Utiliser ORM pour insérer des données avec bulk insert
try:
    session.no_autoflush = True
    
    print("Inserting States...")
    unique_states = states_df.drop_duplicates(subset='code').to_dict(orient='records')
    session.bulk_insert_mappings(State, unique_states)
    session.commit()

    print("Inserting Departments...")
    unique_departments = departments_df.drop_duplicates(subset='code').to_dict(orient='records')
    session.bulk_insert_mappings(Department, unique_departments)
    session.commit()

    print("Inserting Cities...")
    unique_cities = cities_df.drop_duplicates(subset='code_name').to_dict(orient='records')
    session.bulk_insert_mappings(City, unique_cities)
    session.commit()

    print("Inserting Projects...")
    unique_projects = projects_df.drop_duplicates(subset=['city_code', 'date']).to_dict(orient='records')
    session.bulk_insert_mappings(Project, unique_projects)
    session.commit()

    print("Toutes les données ont été insérées avec succès.")
except Exception as e:
    session.rollback()
    print(f"Erreur lors de l'insertion des données : {e}")

print("Données insérées avec succès.")

# Vérifier les données insérées
try:
    states = session.query(State).all()
    departments = session.query(Department).all()
    cities = session.query(City).all()
    projects = session.query(Project).all()

    print(f"Nombre de states insérés: {len(states)}")
    print(f"Nombre de departments insérés: {len(departments)}")
    print(f"Nombre de cities insérés: {len(cities)}")
    print(f"Nombre de projects insérés: {len(projects)}")
except Exception as e:
    print(f"Erreur lors de la récupération des données : {e}")

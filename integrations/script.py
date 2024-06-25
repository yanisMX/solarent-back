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

def vider_tables():
    session.execute(text("TRUNCATE TABLE project, city, department, state RESTART IDENTITY CASCADE;"))
    session.commit()

vider_tables()

installations_csv = "C:\\Users\\Florian PESCOT\\OneDrive - DUPUY\\Bureau\\COURS\\bdd\\installations-de-production-solaire-par-commune.csv"
ensoleillement_csv = "C:\\Users\\Florian PESCOT\\OneDrive - DUPUY\\Bureau\\COURS\\bdd\\temps-densoleillement-par-an-par-departement-feuille-1.csv"

installations_df = pd.read_csv(installations_csv, delimiter=';')
ensoleillement_df = pd.read_csv(ensoleillement_csv, delimiter=',')

installations_df.rename(columns={
    '1_f_commune_pdl': 'city_name',
    '1_f_code_insee_pdl': 'city_code',
    'dep': 'departement_code',
    'nom_dept': 'department_name',
    'reg': 'state_code',
    'nom_reg': 'state_name',
    'count': 'count',
    'date_des_donnees': 'date',
    's_3_prod_i_regime_d_exploitation': 'exploitation',
    'sum_3_prod_e_kw_puissance_de_raccordement_injection': 'puissance',
    'coordonnees': 'coordinates'
}, inplace=True)

installations_df['code_name'] = installations_df['city_name'] + "_" + installations_df['city_code'].astype(str)

city_total_counts = installations_df.groupby('code_name')['count'].sum().reset_index()
city_total_counts.rename(columns={'count': 'total_count'}, inplace=True)

installations_df = installations_df.merge(city_total_counts, on='code_name')

departments_df = installations_df[['departement_code', 'department_name']].drop_duplicates()
departments_df = departments_df.merge(ensoleillement_df, left_on='department_name', right_on=ensoleillement_df.columns[0])
departments_df.rename(columns={ensoleillement_df.columns[1]: 'sun_rate'}, inplace=True)

states_df = installations_df[['state_code', 'state_name']].drop_duplicates()

cities_df = installations_df[['code_name', 'city_name', 'coordinates', 'total_count', 'departement_code', 'state_code']]
cities_df.drop_duplicates(inplace=True)
cities_df.rename(columns={
    'code_name': 'code_name',
    'city_name': 'city_name',
    'coordinates': 'coordinates',
    'total_count': 'total_count',
    'departement_code': 'departement_code',
    'state_code': 'state_code'
}, inplace=True)

projects_df = installations_df[['code_name', 'count', 'date', 'puissance', 'exploitation']]
projects_df.rename(columns={
    'code_name': 'city_code'
}, inplace=True)

states_df.to_sql('state', engine, if_exists='append', index=False)
departments_df.to_sql('department', engine, if_exists='append', index=False)
cities_df.to_sql('city', engine, if_exists='append', index=False)
projects_df.to_sql('project', engine, if_exists='append', index=False)

print("Données insérées avec succès.")

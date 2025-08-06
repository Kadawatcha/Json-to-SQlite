import json
import sqlite3

# Charger les données JSON
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Insérer les données dans SQLite
def transfer_json_to_sqlite(json_data, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Assurez-vous que la table existe déjà dans SQLite
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS counters (
            guild_id TEXT PRIMARY KEY,
            counter_channel_id INTEGER,
            last_number INTEGER,
            last_user_id INTEGER,
            emoji TEXT
        )
    ''')

    # Parcourir les données JSON et insérer dans SQLite
    for guild_id, data in json_data.items():
        cursor.execute('''
            INSERT INTO counters (guild_id, counter_channel_id, last_number, last_user_id, emoji)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(guild_id) DO UPDATE SET
                counter_channel_id=excluded.counter_channel_id,
                last_number=excluded.last_number,
                last_user_id=excluded.last_user_id,
                emoji=excluded.emoji
        ''', (
            guild_id,
            data.get('counter_channel_id'),
            data.get('last_number'),
            data.get('last_user_id'),
            data.get('emoji')
        ))

    conn.commit()
    conn.close()

# Exemple d'utilisation
json_file_path = 'bdd/mon_fichier.json'  # Remplacez par le chemin de votre fichier JSON
sqlite_db_path = 'bdd/mon_fichier.db'  # Chemin vers votre base de données SQLite

json_data = load_json(json_file_path)
transfer_json_to_sqlite(json_data, sqlite_db_path)

print("Migration des données JSON vers SQLite terminée.")
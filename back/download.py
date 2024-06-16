import requests
import pickle
import os
import sqlite3

def get_votes(start_date, end_date):
    base_url = "https://commonsvotes-api.parliament.uk/data/divisions.json/search"
    params = {
        'queryParameters.skip': 0,
        'queryParameters.take': 25,
        'queryParameters.startDate': start_date,
        'queryParameters.endDate': end_date,
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        return response.json()['items']
    else:
        print(f"Error {response.status_code}: {response.text}")
        response.raise_for_status()

def get_division_details(division_id):
    base_url = f"https://commonsvotes-api.parliament.uk/data/division/{division_id}.json"
    
    response = requests.get(base_url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        response.raise_for_status()

def fetch_detailed_votes(start_date, end_date, pickle_file='detailed_votes.pkl'):
    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as file:
            detailed_votes = pickle.load(file)
        print("Loaded data from pickle file.")
    else:
        votes = get_votes(start_date, end_date)
        detailed_votes = [get_division_details(vote['DivisionId']) for vote in votes]
        with open(pickle_file, 'wb') as file:
            pickle.dump(detailed_votes, file)
        print("Fetched data from API and saved to pickle file.")
    
    return detailed_votes

def process_votes(detailed_votes):
    processed_data = []
    for vote in detailed_votes:
        title = vote['Title']
        date = vote['Date']
        conservative_ayes = sum(1 for member in vote['Ayes'] if member['Party'] == 'Conservative')
        conservative_noes = sum(1 for member in vote['Noes'] if member['Party'] == 'Conservative')
        labour_ayes = sum(1 for member in vote['Ayes'] if member['Party'] == 'Labour')
        labour_noes = sum(1 for member in vote['Noes'] if member['Party'] == 'Labour')
        
        processed_data.append({
            'title': title,
            'conservative_ayes': conservative_ayes,
            'conservative_noes': conservative_noes,
            'labour_ayes': labour_ayes,
            'labour_noes': labour_noes,
            'date': date
        })
    return processed_data

def create_database():
    conn = sqlite3.connect('votes.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS votes (
            id INTEGER PRIMARY KEY,
            title TEXT,
            fullText TEXT,
            summary TEXT,
            easyTitle TEXT,
            q1 TEXT,
            a1 TEXT,
            q2 TEXT,
            a2 TEXT,
            q3 TEXT,
            a3 TEXT,
            conservative_ayes INTEGER,
            conservative_noes INTEGER,
            labour_ayes INTEGER,
            labour_noes INTEGER,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_votes(processed_data):
    conn = sqlite3.connect('votes.db')
    c = conn.cursor()
    for vote in processed_data:
        c.execute('''
            INSERT INTO votes (title, conservative_ayes, conservative_noes, labour_ayes, labour_noes, date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (vote['title'], vote['conservative_ayes'], vote['conservative_noes'], vote['labour_ayes'], vote['labour_noes'], vote['date']))
    conn.commit()
    conn.close()

start_date = '2024-05-15'
end_date = '2024-06-15'
detailed_votes = fetch_detailed_votes(start_date, end_date)
processed_data = process_votes(detailed_votes)
create_database()
insert_votes(processed_data)

print("Votes have been processed and stored in the database.")

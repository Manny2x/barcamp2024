import requests
import json

url = 'https://oralquestionsandmotions-api.parliament.uk/oralquestions/list'
headers = {'Accept': 'application/json'}
params = {
    'parameters.answeringDateStart': '2023-06-15',
    'parameters.answeringDateEnd': '2024-06-15',
    'parameters.take': '100',
    'parameters.skip': '0'
}

all_data = []
current_skip = 0
total = 1

# Initialize a dictionary to store questions by party
questions_by_party = {}

while current_skip < total:
    params['parameters.skip'] = str(current_skip)
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    
    if current_skip == 0:
        total = data['PagingInfo']['Total']
        print(f"Total records: {total}")
    
    all_data.extend(data['Response'])
    
    # Process each question and add it to the appropriate party in the dictionary
    for item in data['Response']:
        question = item['QuestionText']
        party = item['AskingMember']['Party']
        
        if party not in questions_by_party:
            questions_by_party[party] = []
        
        questions_by_party[party].append(question)
    
    current_skip += int(params['parameters.take'])
    print(f"Fetched {len(data['Response'])} records, skipping to {current_skip}")

print(f"Total fetched records: {len(all_data)}")

# Save the questions by party to a JSON file
with open('questions_by_party.json', 'w') as f:
    json.dump(questions_by_party, f, indent=4)

# Print a summary of the questions by party
for party, questions in questions_by_party.items():
    print(f"Party: {party}, Number of Questions: {len(questions)}")


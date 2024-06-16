from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from typing import List

class PartyVotes(BaseModel):
    party: str
    colour: str
    ayes: int
    noes: int

class QuestionAnswer(BaseModel):
    question: str
    answer: str

class Votes(BaseModel):
    title: str
    niceTitle: str
    summary: str
    questions: List[QuestionAnswer]
    parties: List[PartyVotes]

app = FastAPI()

# Function to get votes from the database and transform to the new structure
def get_votes_by_title(title: str) -> List[Votes]:
    conn = sqlite3.connect('votes.db')
    c = conn.cursor()
    c.execute('''
        SELECT title, easyTitle, summary, q1, a1, q2, a2, q3, a3, conservative_ayes, conservative_noes, labour_ayes, labour_noes, date 
        FROM votes 
        WHERE title LIKE ?
    ''', ('%' + title + '%',))
    rows = c.fetchall()
    conn.close()
    
    if not rows:
        raise HTTPException(status_code=404, detail="Votes not found")

    votes_dict = {}
    for row in rows:
        vote_title = row[0]
        if vote_title not in votes_dict:
            votes_dict[vote_title] = {
                "title": vote_title,
                "niceTitle": row[1] if row[1] else "",
                "summary": row[2] if row[2] else "",
                "questions": [
                    {"question": row[3] if row[3] else "", "answer": row[4] if row[4] else ""},
                    {"question": row[5] if row[5] else "", "answer": row[6] if row[6] else ""},
                    {"question": row[7] if row[7] else "", "answer": row[8] if row[8] else ""}
                ],
                "parties": []
            }
        
        votes_dict[vote_title]["parties"].extend([
            {"party": "Conservative", "colour": "blue", "ayes": row[9], "noes": row[10]},
            {"party": "Labour", "colour": "red", "ayes": row[11], "noes": row[12]}
        ])
    
    votes_list = [Votes(**vote) for vote in votes_dict.values()]
    return votes_list

# Define the FastAPI endpoint
@app.get("/votes/", response_model=List[Votes])
async def search_votes(title: str):
    return get_votes_by_title(title)

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

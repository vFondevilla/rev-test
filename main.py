from fastapi import FastAPI, HTTPException, Path, Body, Depends
from datetime import datetime, date
from pydantic import BaseModel
import redis
import os

app = FastAPI()

# Initialize Redis connection
redis_client = redis.StrictRedis(host=os.getenv('REDIS_HOST', 'localhost'), port=os.getenv('REDIS_PORT', '6379'), db=0)

class User(BaseModel):
    date_of_birth: date

def get_days_until_birthday(birthday: date) -> int:
    today = date.today()
    upcoming_birthday = date(today.year, birthday.month, birthday.day)

    if today > upcoming_birthday:
        upcoming_birthday = date(today.year + 1, birthday.month, birthday.day)

    return (upcoming_birthday - today).days

@app.put("/hello/{username}", status_code=204)
def save_or_update_user(username: str = Path(..., regex="^[a-zA-Z]+$"), user: User = Body(...)):
    if user.date_of_birth > date.today():
        raise HTTPException(status_code=400, detail="date_of_birth must be a date before the today date")

    # Save to Redis
    redis_client.set(username, user.date_of_birth.isoformat())

@app.get("/hello/{username}")
def hello_birthday(username: str = Path(..., regex="^[a-zA-Z]+$")):
    date_of_birth_str = redis_client.get(username)

    if not date_of_birth_str:
        raise HTTPException(status_code=404, detail="Username not found")

    date_of_birth = datetime.strptime(date_of_birth_str.decode('utf-8'), "%Y-%m-%d").date()
    days_until_birthday = get_days_until_birthday(date_of_birth)

    if days_until_birthday == 0:
        return {"message": f"Hello, {username}! Happy birthday!"}
    else:
        return {"message": f"Hello, {username}! Your birthday is in {days_until_birthday} day(s)"}

if __name__ == "__main__":
    # Start uvicorn manually: uvicorn filename:app --reload
    pass

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from speedometer import models, schemas
from speedometer.database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import random
import time
import threading
import time
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
DATABASE_URL = "mysql://myuser:mypassword@mysql:3306/mydatabase"


origins = [
    "http://localhost:3000",  # React app
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def create_db_engine():
    retries = 5
    while retries > 0:
        try:
            engine = create_engine(DATABASE_URL)
            engine.connect()
            return engine
        except OperationalError:
            retries -= 1
            time.sleep(5)
    raise Exception("Could not connect to the database after multiple attempts")

engine = create_db_engine()
# rest of your FastAPI setup

# Create all tables in the database


# Configure CORS

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to generate speed data
def generate_speed_data():
    while True:
        db = SessionLocal()
        try:
            speed = round(random.uniform(20.0, 35.0), 1)  # Simulate robot speed data
            timestamp = datetime.utcnow()
            speed_data = models.SpeedData(timestamp=timestamp, speed=speed)
            db.add(speed_data)
            db.commit()
            print(f"Generated and posted speed data: {speed_data}")
        finally:
            db.close()
        time.sleep(1)  # Sleep for 1 second between each data insertion

# Function to fetch and print latest speed data
def fetch_speed_data():
    while True:
        db = SessionLocal()
        try:
            latest_speed_data = db.query(models.SpeedData).order_by(models.SpeedData.timestamp.desc()).first()
            print(f"Fetched latest speed data: {latest_speed_data}")
        finally:
            db.close()
        time.sleep(1)  # Sleep for 1 second between each fetch

@app.post("/generate-speed-data/", response_model=schemas.SpeedData)
def manually_generate_speed_data(db: Session = Depends(get_db)):
    speed = round(random.uniform(20.0, 35.0), 1)  # Simulate robot speed data
    timestamp = datetime.utcnow()
    speed_data = models.SpeedData(timestamp=timestamp, speed=speed)
    db.add(speed_data)
    db.commit()
    print(f"Manually generated and posted speed data: {speed_data}")
    return speed_data

@app.get("/speed-data/", response_model=schemas.SpeedData)
def read_latest_speed_data(db: Session = Depends(get_db)):
    latest_speed_data = db.query(models.SpeedData).order_by(models.SpeedData.timestamp.desc()).first()
    print(f"Fetched latest speed data: {latest_speed_data}")
    return latest_speed_data

@app.get("/all-data/", response_model=schemas.SpeedData)
def read_latest_speed_data(db: Session = Depends(get_db)):
    latest_speed_data = db.query(models.SpeedData).order_by(models.SpeedData.timestamp.desc()).first()
    print(f"Fetched latest speed data: {latest_speed_data}")
    return latest_speed_data

# Lifespan context manager for startup and shutdown events
@app.on_event("startup")
async def startup():
    threading.Thread(target=generate_speed_data, daemon=True).start()
    threading.Thread(target=fetch_speed_data, daemon=True).start()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

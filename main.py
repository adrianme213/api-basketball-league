from enum import Enum
from fastapi import FastAPI
from http import HTTPStatus

from db.init_db import get_db_connection
from models.message import Message
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost",
    "http://localhost:8000",
    "*"
]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db_client = get_db_connection()


class DivisionName(str, Enum):
    division1 = "division1"
    division2 = "division2"
    division3 = "division3"


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/status")
async def get_status():
    """Get status of messaging server."""
    return {"status": "running"}


@app.get("/items/{item_id}")
async def read_item(item_id: float):
    return {"item_id": item_id}


@app.get("/division/{division_name}", status_code=HTTPStatus.CREATED.value)
async def get_division_info(division_name: DivisionName):
    if DivisionName.division1.value == division_name:
        return {"model_name": division_name, "message": "1st division - top"}
    elif DivisionName.division2.value == division_name:
        return {"model_name": division_name, "message": "2nd division - almost top"}
    elif DivisionName.division3.value == division_name:
        return {"model_name": division_name, "message": "3rd division - hard work division"}

    return {"model_name": "NOT FOUND", "message": "Unfound league"}


DB = "adrian"
GAMES_COLLECTION = "games"


@app.get("/channels", status_code=HTTPStatus.OK.value, response_model=list[str])
def get_channels():
    """Get all channels in list form."""
    games_collection = db_client[DB][GAMES_COLLECTION]
    distinct_channel_list = games_collection.distinct("channel")
    return distinct_channel_list


@app.get("/games/{channel}", status_code=HTTPStatus.OK.value, response_model=list[Message])
def get_games(channel: str):
    """Get all games for the specified channel."""
    games_collection = db_client[DB][GAMES_COLLECTION]
    games_list = games_collection.find({"channel": channel})
    response_games_list = []
    for msg in games_list:
        response_games_list.append(Message(**msg))
    return response_games_list


@app.post("/post_message", status_code=HTTPStatus.CREATED.value)
def post_message(message: Message):
    """Post a new message to the specified channel."""
    games_collection = db_client[DB][GAMES_COLLECTION]
    result = games_collection.insert_one(message.dict())
    ack = result.acknowledged
    return {"insertion": ack}
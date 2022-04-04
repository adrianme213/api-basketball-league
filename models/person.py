from pydantic import BaseModel


class Person(BaseModel):
    first: str
    last: str
    zip_code: str

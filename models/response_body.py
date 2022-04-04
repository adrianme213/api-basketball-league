from pydantic import BaseModel


class ResponseBody(BaseModel):
    request_id: str
    status_code: int
    body: dict

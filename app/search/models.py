from pydantic import BaseModel


class QueryRequest(BaseModel):
    text: str

class QueryResponse(BaseModel):
    result: str
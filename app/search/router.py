from fastapi import APIRouter, HTTPException
from search.models import QueryRequest, QueryResponse
from search.service import get_framework_recommendation


router = APIRouter()


@router.post("/query", response_model=QueryResponse)
async def query_task(request: QueryRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    result = get_framework_recommendation(request.text)
    return QueryResponse(result=result)

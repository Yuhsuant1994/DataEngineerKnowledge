from fastapi import APIRouter, Query

router = APIRouter()

@router.get("/add")
def add(
    a: int= Query(title="first int", default=1, description="first integer to perform calculation"), 
    b: int= Query(title="second int", default=1, description="second integer to perform calculation")
    ):
    return {"result": a + b}

@router.get("/minus")
def minus(
    a: int= Query(title="first int", default=1, description="first integer to perform calculation"), 
    b: int= Query(title="second int", default=1, description="second integer to perform calculation")
):
    return {"result": a - b}
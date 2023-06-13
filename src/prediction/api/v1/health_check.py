from fastapi import FastAPI, APIRouter, Depends
from fastapi_health import health

def healthy_condition():
    return {"response": 200}


def sick_condition():
    return True

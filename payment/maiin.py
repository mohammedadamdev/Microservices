from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
from starlette.requests import Request


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['hhtp://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

#This should be a dufferebt database
redis = get_redis_connection(
    host="redis-19888.c305.ap-south-1-1.ec2.cloud.redislabs.com",
    port=19888,
    password="aOclS8A4xlIbclWlywLAcnP33q61bUKU",
    decode_responses=True
)

class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str #pending, completed, refunded

    class Meta:
        database = redis

@app.post('/orders')
async def create(request: Request): # id, quantity
    body = await request.json()


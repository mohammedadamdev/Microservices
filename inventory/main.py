from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['hhtp://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

redis = get_redis_connection(
    host="redis-19888.c305.ap-south-1-1.ec2.cloud.redislabs.com",
    port=19888,
    password="aOclS8A4xlIbclWlywLAcnP33q61bUKU",
    decode_responses=True
)

class Product(HashModel):
    name: str
    price: float
    quantity: int
    location: str

    class Meta:
        database = redis


@app.get('/products')
def all():

    return [format(pk) for pk in Product.all_pks()]
    # pk = '01G9FQ7923AR2G4MMJ593AW65Q'
    # return Product.get(pk)

def format(pk:str):
    product = Product.get(pk)

    return{
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity,
        'location': product.location
    }

@app.post('/products')
def create(product: Product):
    return product.save()

@app.get('/products/{pk}')
def get(pk:str):
    return Product.get(pk)

@app.delete('/products/{pk}')
def delete(pk: str):
    return Product.delete(pk)
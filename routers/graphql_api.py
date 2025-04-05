from graphene_sqlalchemy import SQLAlchemyObjectType
from models import Product, User
from database import SessionLocal
from fastapi import FastAPI, APIRouter, Request,Depends
from graphene import Schema, ObjectType, List
from fastapi.responses import JSONResponse
from graphql.error import GraphQLError
from .dependencies import get_current_user


# Create the FastAPI app
app = FastAPI()

# Set up the router for GraphQL
router = APIRouter()

class ProductType(SQLAlchemyObjectType):
    class Meta:
        model = Product

class Query(ObjectType):
    products = List(ProductType)

    def resolve_products(self, info):
        session = SessionLocal()
        return session.query(Product).all()

# Create the schema for GraphQL
schema = Schema(query=Query)

# Define the GraphQL endpoint
@router.post("/graphql")
async def graphql_query(request: Request):
    query = await request.json()
    
    # Execute the query
    result = schema.execute(query.get('query'))
    
    # Prepare the errors in a serializable way
    if result.errors:
        formatted_errors = []
        for error in result.errors:
            if isinstance(error, GraphQLError):
                # You can access error locations, messages, etc. Customize as needed
                formatted_errors.append({
                    "message": str(error),
                    "locations": error.locations,
                    "path": error.path,
                })
            else:
                formatted_errors.append(str(error))
        
        return JSONResponse(content={"data": result.data, "errors": formatted_errors})
    
    # If there are no errors, just return the data
    return JSONResponse(content={"data": result.data})

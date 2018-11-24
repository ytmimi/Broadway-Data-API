import graphene
from api.schema import Query as api_query

class Query(api_query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)

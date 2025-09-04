import graphene
import crm.schema

# Inherit from the app's Query and Mutation classes
class Query(crm.schema.Query, graphene.ObjectType):
    pass

class Mutation(crm.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
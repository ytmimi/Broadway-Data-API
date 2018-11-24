import graphene
from graphql import GraphQLError
from graphene_django.types import DjangoObjectType
from api.models import Show, Production, Grosses


class ShowType(DjangoObjectType):
    class Meta:
        model = Show

class ProductionType(DjangoObjectType):
    class Meta:
        model = Production

class GrossesType(DjangoObjectType):
    class Meta:
        model = Grosses

class Query:
    shows = graphene.List(ShowType)
    show = graphene.Field(
        ShowType,
        show_name = graphene.String(required=True)
    )

    def resolve_shows(self, info):
        return Show.objects.all()

    def resolve_show(self, info, show_name):
        try:
            return Show.objects.get(name=show_name)
        except Show.DoesNotExist:
            raise GraphQLError(f'Now Show: {show_name}')

from django.urls import path
# from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

from graphql_project.schema import schema
from graphql_project.views import test
urlpatterns = [
    path("graphql", GraphQLView.as_view(graphiql=True, schema=schema)),
    path("test/", test.as_view({"get":"list_user"}))
]

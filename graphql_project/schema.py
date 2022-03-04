import graphene
from django.db.models import Exists, OuterRef
from graphene_django import DjangoObjectType

from graphql_project.models import User, Books


class UserView(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "name", "year",)
    has_book_flag = graphene.Boolean() # khai báo để trả về những field ko có trong db
        # fields = "__all__"  # có thể lấy ra cả khó ngoại và thông tin trong bảng khóa ngoại thông qua query trên web

class BooksView(DjangoObjectType):
    class Meta:
        model = Books
        fields = ("user",)


class Query(graphene.ObjectType):
    all_user = graphene.List(UserView)
    get_user_by_year = graphene.List(UserView, year=graphene.Int(required=True))

    extra_field = graphene.String()

    def resolve_extra_field(self, info):
        return "hello"

    def resolve_all_user(self, info):
        users = User.objects.annotate(has_book_flag=Exists(Books.objects.filter(user=OuterRef('id')))).all()
        return users

    def resolve_get_user_by_year(self, info, year):
        return User.objects.filter(year=year)

    all_books = graphene.List(BooksView)
    def resolve_all_books(self, info):
        return Books.objects.all()

schema = graphene.Schema(query=Query)

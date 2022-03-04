import graphene
from django.db.models import Exists, OuterRef
from graphene import relay
from graphene_django import DjangoObjectType

from graphql_project.models import User, Books


# query
class UserView(DjangoObjectType):
    class Meta:
        model = User
        interfaces = (relay.Node,)  # nếu phân trang bắt buộc phải có
        fields = ("id", "name", "year",)

    has_book_flag = graphene.Boolean()  # khai báo để trả về những field ko có trong db
    # fields = "__all__"  # có thể lấy ra cả khó ngoại và thông tin trong bảng khóa ngoại thông qua query trên web


class UserViewConnection(relay.Connection):  # dùng để phân trang
    class Meta:
        node = UserView


class BooksView(DjangoObjectType):
    class Meta:
        model = Books
        fields = ("user",)


class Query(graphene.ObjectType):
    extra_field = graphene.String()

    def resolve_extra_field(self, info):
        return "hello"

    all_user = graphene.List(UserView)

    def resolve_all_user(self, info):
        users = User.objects.annotate(has_book_flag=Exists(Books.objects.filter(user=OuterRef('id')))).all()
        return users

    get_user_by_year = graphene.List(UserView, year=graphene.Int(required=True))

    def resolve_get_user_by_year(self, info, year):
        return User.objects.filter(year=year)

    all_books = graphene.List(BooksView)

    def resolve_all_books(self, info):
        return Books.objects.all()

    # Phân trang
    users = relay.ConnectionField(UserViewConnection)

    def resolve_users(self, info, **kwargs):
        return User.objects.all()


# add, update, delete
class UserViewForCreateUpdate(DjangoObjectType):
    class Meta:
        model = User
        fields = '__all__'


class UserMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        year = graphene.Int()

    # xác đinh dữ liệu sẽ trả về sẽ bao gồm những field nào ( show ra cho người dùng ) xem khi cạp nhật xong
    user_after_create = graphene.Field(UserViewForCreateUpdate)

    @classmethod
    def mutate(cls, root, info, **data):
        # def mutate(cls, root, info, name, year):
        user = User.objects.create(
            name=data.get('name'),
            year=data.get('year')
            # name=name,
            # year=year
        )
        # user.save()
        return UserMutation(user_after_create=user)  # truyền dữ liệu trả về cho người dùng


class UpdateUserMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        name = graphene.String()
        year = graphene.Int()

    user_after_update = graphene.Field(UserViewForCreateUpdate)

    @classmethod
    def mutate(cls, root, info, **data_update):
        # user = User.objects.filter(id=data_update.get('id')).update(
        #     name=data_update.get('name'),
        #     year=data_update.get('year')
        # ) # ko dùng cách này mặc dù có thể update được nhưng không thể trả về định dang object nên sẽ báo lỗi
        user = User.objects.get(id=data_update.get('id'))
        user.name = data_update.get('name')
        user.year = data_update.get('year')
        user.save()

        return UpdateUserMutation(user_after_update=user)

class DeleteUserMutaition:
    class Arguments:
        id: graphene.Int()

    user_delete = graphene.Field(UserViewForCreateUpdate)

    @classmethod
    def mutate(cls, root, info, id):
        user = User.objects.get(id=id)
        user.delete()
        return DeleteUserMutaition(user)

class Mutation(graphene.ObjectType):
    create_user = UserMutation.Field()
    update_user = UpdateUserMutation.Field()
    delete_user = DeleteUserMutaition


schema = graphene.Schema(query=Query, mutation=Mutation)

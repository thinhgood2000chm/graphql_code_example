import graphene
from django.db.models import Exists, OuterRef
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.debug import DjangoDebug

from graphql_project.models import User, Books


# query
class UserView(DjangoObjectType):
    class Meta:
        model = User
        interfaces = (relay.Node,)  # nếu phân trang bắt buộc phải có, sẽ trả về id th eodạng mã hóa
        fields = ("id", "name", "year",)
        # fields = "__all__"

    has_book_flag = graphene.Boolean()  # khai báo để trả về những field ko có trong db
    # fields = "__all__"  # có thể lấy ra cả khó ngoại và thông tin trong bảng khóa ngoại thông qua query trên web


class UserViewConnection(relay.Connection):  # dùng để phân trang
    class Meta:
        node = UserView


class BooksView(DjangoObjectType):
    class Meta:
        model = Books
        fields = ("user",)

    # @classmethod  # Global Filtering
    # def get_queryset(cls, queryset, info):
    #     if info.context.user.is_anonymous:
    #         return queryset.objects.all()
    #     return queryset


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

    all_books = graphene.Field(BooksView)

    def resolve_all_books(self, info):
        return Books.objects.get(id=3)
        # return BooksView.get_queryset(Books, info) # Cách tạo Global Filtering

    # Phân trang
    users = relay.ConnectionField(UserViewConnection)

    def resolve_users(self, info, **kwargs):
        return User.objects.all()


    debug = graphene.Field(DjangoDebug, name='_debug') # hiển thị debug

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


class DeleteUserMutaition(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.Int()

    # user_delete = graphene.Field(UserViewForCreateUpdate)

    @classmethod
    def mutate(cls, root, info, id):
        user = User.objects.get(id=id)
        user.delete()
        return cls(ok=True)


class Mutation(graphene.ObjectType):
    create_user = UserMutation.Field()
    update_user = UpdateUserMutation.Field()
    delete_user = DeleteUserMutaition.Field()


# cách khác để ghi dữ liệu trả về
schema = graphene.Schema(query=Query, mutation=Mutation)

import graphene
from graphene_django import DjangoObjectType, DjangoListField
from .models import Order

class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = "__all__"
class Query(graphene.ObjectType):
    all_order = graphene.List(OrderType)
    order = graphene.Field(OrderType, order_id=graphene.Int())
    def resolve_all_order(self, info, **kwargs):
        return Order.objects.all()

    def resolve_order(self, info, order_id):
        return Order.objects.get(pk=order_id)

class OrderInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    Location = graphene.String()
    Total_Price = graphene.Int()
    Quantity = graphene.Int()
    Status = graphene.String()

class CreateOrder(graphene.Mutation):
    class Arguments:
        order_data = OrderInput(required=True)

    order = graphene.Field(OrderType)

    @staticmethod
    def mutate(root, info, order_data=None):
        order_instance = Order(
            name=order_data.name,
            Location = order_data.Location,
            Total_Price = order_data.Total_Price,
            Quantity = order_data.Quantity,
            Status = order_data.Status,
        )
        order_instance.save()
        return CreateOrder(order=order_instance)


class UpdateOrder(graphene.Mutation):
    class Arguments:
        order_data = OrderInput(required=True)

    order = graphene.Field(OrderType)

    @staticmethod
    def mutate(root, info, order_data=None):
        order_instance = Order.objects.get(pk=order_data.id)

        if order_instance:
            order_instance.name = order_data.name
            order_instance.Description = product_data.Description
            order_instance.SKU = product_data.SKU
            order_instance.Slug = product_data.Slug
            order_instance.Product_Category = product_data.Product_Category
            order_instance.Price = product_data.Price
            order_instance.save()

            return UpdateOrder(product=order_instance)
        return UpdateOrder(product=None)


class DeleteOrder(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    product = graphene.Field(OrderType)

    @staticmethod
    def mutate(root, info, id):
        order_instance = Order.objects.get(pk=id)
        order_instance.delete()

        return None


class Mutation(graphene.ObjectType):
    create_order = CreateOrder.Field()
    update_order = UpdateOrder.Field()
    delete_order = DeleteOrder.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
import graphene
from graphene_django import DjangoObjectType, DjangoListField
from .models import Product
from order_api.models import Order

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = "__all__"

class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = "__all__"
class Query(graphene.ObjectType):
    all_product = graphene.List(ProductType)
    product = graphene.Field(ProductType, product_id=graphene.Int())
    all_order = graphene.List(OrderType)
    order = graphene.Field(OrderType, order_id=graphene.Int())
    def resolve_all_product(self, info, **kwargs):
        return Product.objects.all()

    def resolve_product(self, info, product_id):
        return Product.objects.get(pk=product_id)

    def resolve_all_order(self, info, **kwargs):
        return Order.objects.all()

    def resolve_order(self, info, order_id):
        return Order.objects.get(pk=order_id)

class ProductInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    Description = graphene.String()
    SKU = graphene.String()
    Slug = graphene.String()
    Image_url = graphene.String()
    Product_Category = graphene.String()
    Price = graphene.Int()

class OrderInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    Location = graphene.String()
    Total_Price = graphene.Int()
    Quantity = graphene.Int()
    Status = graphene.String()

class CreateProduct(graphene.Mutation):
    class Arguments:
        product_data = ProductInput(required=True)

    product = graphene.Field(ProductType)

    @staticmethod
    def mutate(root, info, product_data=None):
        product_instance = Product(
            name=product_data.name,
            Description = product_data.Description,
            SKU = product_data.SKU,
            Slug = product_data.Slug,
            Image_url = product_data.Image_url,
            Product_Category = product_data.Product_Category,
            Price = product_data.Price,

        )
        product_instance.save()
        return CreateProduct(product=product_instance)

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


class UpdateProduct(graphene.Mutation):
    class Arguments:
        product_data = ProductInput(required=True)

    product = graphene.Field(ProductType)

    @staticmethod
    def mutate(root, info, product_data=None):
        product_instance = Product.objects.get(pk=product_data.id)

        if product_instance:
            product_instance.name = product_data.name
            product_instance.Description = product_data.Description
            product_instance.SKU = product_data.SKU
            product_instance.Slug = product_data.Slug
            product_instance.Image_url = product_data.Image_url
            product_instance.Product_Category = product_data.Product_Category
            product_instance.Price = product_data.Price
            product_instance.save()

            return UpdateProduct(product=product_instance)
        return UpdateProduct(product=None)

class UpdateOrder(graphene.Mutation):
    class Arguments:
        order_data = OrderInput(required=True)

    order = graphene.Field(OrderType)

    @staticmethod
    def mutate(root, info, order_data=None):
        order_instance = Order.objects.get(pk=order_data.id)

        if order_instance:
            order_instance.name = order_data.name
            order_instance.Location = order_data.Location
            order_instance.Total_Price = order_data.Total_Price
            order_instance.Status = order_data.Status
            order_instance.Quantity = order_data.Quantity

            order_instance.save()



            return UpdateOrder(order=order_instance)
        return UpdateOrder(order=None)


class DeleteProduct(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    product = graphene.Field(ProductType)

    @staticmethod
    def mutate(root, info, id):
        product_instance = Product.objects.get(pk=id)
        product_instance.delete()

        return None

class DeleteOrder(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    order = graphene.Field(OrderType)

    @staticmethod
    def mutate(root, info, id):
        order_instance = Order.objects.get(pk=id)
        order_instance.delete()

        return None


class Mutation(graphene.ObjectType):
    create_product = CreateProduct.Field()
    update_product = UpdateProduct.Field()
    delete_product = DeleteProduct.Field()
    create_order = CreateOrder.Field()
    update_order = UpdateOrder.Field()
    delete_order = DeleteOrder.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
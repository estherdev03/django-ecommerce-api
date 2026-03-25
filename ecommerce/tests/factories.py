import factory

from ecommerce.product.models import Category, Brand, Product, ProductLine, ProductImage


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: "category_%d" % n)
    is_active = True


class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Brand

    name = factory.Sequence(lambda n: "brand_%d" % n)
    is_active = True


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = "test_product"
    description = "test_description"
    is_digital = True
    brand = factory.SubFactory(BrandFactory)
    category = factory.SubFactory(CategoryFactory)
    is_active = True


class ProductLineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductLine

    price = 10.00
    sku = "12345"
    stock_qty = 1
    product = factory.SubFactory(ProductFactory)
    is_active = True


class ProductImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductImage

    alternative_text = "test_image"
    url = "test.jpg"
    product_line = factory.SubFactory(ProductLineFactory)

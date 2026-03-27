from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from django.db.models import Prefetch

# from django.db import connection
# from pygments import highlight
# from pygments.formatters import TerminalFormatter
# from pygments.lexers import SqlLexer
# from sqlparse import format

from .models import Category, Product, ProductLine, ProductImage
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ProductCategorySerializer,
)


class CategoryView(viewsets.ViewSet):
    """
    A simple Viewset for viewing all categories
    """

    queryset = Category.objects.all().is_active()

    @extend_schema(responses=CategorySerializer)
    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data)


class ProductView(viewsets.ViewSet):
    """A simple Viewset for viewing all products"""

    queryset = Product.objects.all().is_active()

    lookup_field = "slug"

    def retrieve(self, request, slug=None):
        serializer = ProductSerializer(
            self.queryset.filter(slug=slug)
            .prefetch_related(Prefetch("attribute_value__attribute"))
            .prefetch_related(Prefetch("product_line__product_image"))
            .prefetch_related(Prefetch("product_line__attribute_value__attribute")),
            many=True,
        )
        data = Response(serializer.data)
        # --------------Analyze number of queries in this method----------------------
        # q = list(connection.queries)
        # for qs in q:
        #     sqlformatted = format(str(qs["sql"]), reindent=True)
        #     print(highlight(sqlformatted, SqlLexer(), TerminalFormatter()))
        # print(len(q))
        # -----------------------------------------------------------------------------
        return data

    @action(
        methods=["get"],
        detail=False,
        url_path=r"category/(?P<slug>[\w-]+)",
    )
    def list_product_by_category_slug(self, request, slug=None):
        """An endpoint to return products by category slug"""
        serializer = ProductCategorySerializer(
            self.queryset.filter(category__slug=slug)
            .prefetch_related(
                Prefetch("product_line", queryset=ProductLine.objects.order_by("order"))
            )
            .prefetch_related(
                Prefetch(
                    "product_line__product_image",
                    queryset=ProductImage.objects.filter(order=1),
                )
            ),
            many=True,
        )
        return Response(serializer.data)

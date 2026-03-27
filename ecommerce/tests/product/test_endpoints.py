import pytest
import json

pytestmark = pytest.mark.django_db


class TestCategoryEndpoints:
    endpoint = "/api/category/"

    def test_category_get(self, category_factory, api_client):
        category_factory.create_batch(4)
        response = api_client().get(self.endpoint)
        assert response.status_code == 200


class TestProductEndpoints:
    endpoint = "/api/product/"

    def test_return_products_by_category_slug(
        self, category_factory, product_factory, api_client
    ):
        obj = category_factory(slug="test_slug")
        product_factory(category=obj, is_active=True)
        response = api_client().get(f"{self.endpoint}category/{obj.slug}/")
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1

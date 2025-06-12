from django.test import TestCase
from .models import Product
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

#base test class to remove redundant setUp() method in each test class
class BaseProductTestCase(TestCase):
    def setUp(self):
        #create fake image
        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\x47\x49\x46\x38\x89\x61',
            content_type='image/jpeg'
        )
        self.product = Product.objects.create(
            name = "Test Name",
            slug = "test_name",
            description = "This is a test product.",
            price = 99.99,
            image = image,
        )

class ProductModelTest(BaseProductTestCase):    
    def test_product_created(self):
        self.assertEqual(self.product.name, "Test Name")
        self.assertEqual(self.product.slug, "test_name")
        self.assertEqual(self.product.description, "This is a test product.")
        self.assertEqual(self.product.price, 99.99)
        #check database to determine there is only one product created
        self.assertEqual(Product.objects.count(), 1)
        self.assertTrue(self.product.image)
        self.assertIn("test_image",self.product.image.name)

    def test_str(self):
        self.assertEqual(str(self.product), "Test Name")

    def test_duplicate_slug_raises_error(self):
        with self.assertRaises(Exception):
            Product.objects.create(
                name="Different Name",
                slug=self.product.slug,
        )
        
class ProductListViewTest(BaseProductTestCase):
    #confirm the correct template is used
    def test_uses_correct_template(self):
        url = reverse("product_list")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "product/product_list.html")

    #ensure successful load
    def test_status_code(self):
        url = reverse("product_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    #ensure context has a list of products
    def test_products_in_context(self):
        url = reverse("product_list")
        response = self.client.get(url)

        #<model_name>_list is the context key for ListView CBV
        products = response.context["product_list"]
        self.assertIn(self.product, products)

    #ensure product details appear in the rendered template
    def test_products_visible(self):
        url = reverse("product_list")
        response = self.client.get(url)
        self.assertContains(response, "Test Name")

class ProductDetailViewTest(BaseProductTestCase):
    #confirm the correct template is used
    def test_uses_correct_template(self):
        url = reverse("product_detail", kwargs={"product_id":self.product.id})
        response = self.client.get(url)
        self.assertTemplateUsed(response, "product/product_detail.html")

    #ensure successful load
    def test_product_list_view_status_code(self):
        url = reverse("product_detail", kwargs={"product_id":self.product.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    #ensure context has a list of products
    def test_products_in_context(self):
        url = reverse("product_detail", kwargs={"product_id":self.product.id})
        response = self.client.get(url)

        #here context key is what is passed in the render function in the view
        prod = response.context["product"]
        self.assertEqual(self.product, prod)

    #ensure product details appear in the rendered template
    def test_products_visible(self):
        url = reverse("product_detail", kwargs={"product_id":self.product.id})
        response = self.client.get(url)
        self.assertContains(response, "Test Name")
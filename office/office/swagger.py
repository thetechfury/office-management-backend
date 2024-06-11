from drf_yasg import openapi

swagger_info = openapi.Info(
    title="My API",
    default_version='v1',
    description="API description",
    terms_of_service="https://www.google.com/policies/terms/",
    contact=openapi.Contact(email="contact@myapi.local"),
    license=openapi.License(name="BSD License"),
)
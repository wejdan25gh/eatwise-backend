from django.urls import path
from .views import upload_product_image, my_product_images, analyze_image, confirm_product, allergy_check

urlpatterns = [
    path("upload-image/", upload_product_image),
    path("my-images/", my_product_images),
    path("analyze/<int:image_id>/", analyze_image),
    path("confirm/<int:product_id>/", confirm_product),
    path("allergy-check/<int:image_id>/", allergy_check),
] 
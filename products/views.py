from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import ProductImage, RecognizedProduct


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def upload_product_image(request):
    image = request.FILES.get("image")

    if not image:
        return Response({"error": "image is required"}, status=400)

    obj = ProductImage.objects.create(
        user=request.user,
        image=image
    )

    return Response({
        "message": "Image uploaded",
        "id": obj.id,
        "image_url": obj.image.url
    })

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_product_images(request):
    images = ProductImage.objects.filter(user=request.user).order_by("-created_at")

    data = [
        {
            "id": img.id,
            "image": img.image.url,
            "created_at": img.created_at,
        }
        for img in images
    ]

    return Response(data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def analyze_image(request, image_id):

    try:
        image = ProductImage.objects.get(id=image_id, user=request.user)
    except ProductImage.DoesNotExist:
        return Response({"error": "image not found"}, status=404)

    
    results = [
        {"name": "Milk", "category": "Dairy", "confidence": 0.92},
        {"name": "Bread", "category": "Bakery", "confidence": 0.87},
    ]

    created = []
    for r in results:
        obj = RecognizedProduct.objects.create(
            image=image,
            name=r["name"],
            category=r["category"],
            confidence=r["confidence"],
            status="pending",
        )
        created.append({
            "id": obj.id,
            "name": obj.name,
            "category": obj.category,
            "confidence": obj.confidence,
            "status": obj.status,
        })

    return Response({
        "image_id": image.id,
        "recognized_products": created
    })



@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def confirm_product(request, product_id):
    """
    Confirm or edit a recognized product.
    Body can include: name, category
    """
    try:
        obj = RecognizedProduct.objects.get(id=product_id, image__user=request.user)
    except RecognizedProduct.DoesNotExist:
        return Response({"error": "product not found"}, status=404)

    name = request.data.get("name")
    category = request.data.get("category")

    if name is not None:
        obj.name = name

    if category is not None:
        obj.category = category

    obj.status = "confirmed"
    obj.save()

    return Response({
        "message": "Product confirmed",
        "product": {
            "id": obj.id,
            "name": obj.name,
            "category": obj.category,
            "confidence": obj.confidence,
            "status": obj.status,
        }
    })


from accounts.models import UserProfile


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def allergy_check(request, image_id):
   
    # Get user's allergies from profile
    profile = UserProfile.objects.filter(user=request.user).first()
    allergies_text = (profile.allergies if profile else "") or ""

    
    allergy_keywords = [a.strip().lower() for a in allergies_text.split(",") if a.strip()]

    # Get the image and its recognized products
    try:
        img = ProductImage.objects.get(id=image_id, user=request.user)
    except ProductImage.DoesNotExist:
        return Response({"error": "image not found"}, status=404)

    products = RecognizedProduct.objects.filter(image=img).order_by("id")

    results = []
    for p in products:
        haystack = f"{p.name} {p.category}".lower()
        matched = [a for a in allergy_keywords if a and a in haystack]

        results.append({
            "product_id": p.id,
            "name": p.name,
            "category": p.category,
            "status": p.status,
            "is_risky": len(matched) > 0,
            "matched_allergies": matched,
        })

    return Response({
        "image_id": img.id,
        "user_allergies": allergy_keywords,
        "results": results
    })
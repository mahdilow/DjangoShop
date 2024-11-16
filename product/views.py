from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Review

def product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    rating_range = range(1, 11)  # Pass range for ratings dropdown in the template

    already_reviewed = False  # Default to False

    # Check if the user has already submitted a review for this product
    if request.user.is_authenticated:
        existing_review = Review.objects.filter(created_by=request.user, product=product).first()
        if existing_review:
            already_reviewed = True  # User has already reviewed, prevent form submission

    # Handle form submission for adding/editing a review
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')  # Redirect to login if the user is not authenticated

        if already_reviewed:
           already_reviewed = False

        try:
            rating = int(request.POST.get('rating', 3))  # Convert to integer for database storage
        except ValueError:
            rating = 3  # Default to 3 if rating conversion fails

        content = request.POST.get('content', '')

        if content:
            # Create a new review if none exists
            Review.objects.create(
                product=product,
                rating=rating,
                content=content,
                created_by=request.user
            )

        return redirect('product', slug=slug)

    return render(request, 'product/product.html', {
        'product': product,
        'rating_range': rating_range,
        'already_reviewed': already_reviewed
    })

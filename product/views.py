from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Review

def product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    rating_range = range(1, 11)  # Pass range for ratings dropdown in the template

    # Handle form submission for adding/editing a review
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')  # Redirect to login if the user is not authenticated

        try:
            rating = int(request.POST.get('rating', 3))  # Convert to integer for database storage
        except ValueError:
            rating = 3  # Default to 3 if rating conversion fails

        content = request.POST.get('content', '')

        if content:
            # Check if a review by the same user already exists
            existing_review = Review.objects.filter(created_by=request.user, product=product).first()
            
            if existing_review:
                # Update the existing review
                existing_review.rating = rating
                existing_review.content = content
                existing_review.save()
            else:
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
        'rating_range': rating_range
    })

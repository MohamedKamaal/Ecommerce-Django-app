from store.models import Category

def categories(request):
    """
    Retrieves all categories from the database and returns them as a context dictionary.
    
    Args:
        request (HttpRequest): The HTTP request object that contains metadata about the request.
        
    Returns:
        dict: A dictionary containing all categories retrieved from the database.
            Key: 'categories' - A queryset of all categories in the store.
    
    Example:
        When this function is called, it fetches all Category objects and prepares them to be
        rendered in a template or used in an API response.
        
    Note:
        This function does not include pagination or any other filter, it simply returns all categories.
    """
    categories = Category.objects.all()
    return {"categories": categories}

def custom_slugify(string, model) -> str:
    slug = string.replace(' ', '-').lower()

    if not model.objects.filter(slug=slug).exists():
        return slug
        
    return f'{slug}-{model.objects.count() + 1}'
    

def get_image_domain(image: str) -> str:
    if image.count('/'):
        first = image.split('/')[0]
        if '.' in first or ':' in first or first == 'localhost':
            return first
    return 'docker.io'

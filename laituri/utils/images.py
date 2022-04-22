def get_image_domain(image):
    return image.split('/')[0] if image.count('/') > 1 else 'docker.io'

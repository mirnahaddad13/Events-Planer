from django.shortcuts import render

class Custom404Middleware:
    """Dev helper: render templates/404.html when a 404 happens."""
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 404:
            return render(request, '404.html', status=404)
        return response
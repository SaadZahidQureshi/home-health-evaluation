from django.shortcuts import render

def custom_404_view(request, exception=None):
    host_name = request.host.name if hasattr(request, "host") else "default"
    
    # Default mapping for each host
    home_url_map = {
        "public": "/",
        "superadmin": "/login-page/",
        "admin": "/login-page/",
    }

    # Pick correct home URL for the current host
    home_url = home_url_map.get(host_name, "/")

    return render(request, "page-not-found.html", {
        "home_url": home_url,
        "host_name": host_name,
    }, status=404)
    # return render(request, "page-not-found.html", status=404)

def custom_500_view(request):
    return render(request, "page-not-found.html", status=500)

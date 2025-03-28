from django.conf import settings


class SeparateAdminSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if it's an admin route
        is_admin_route = request.path.startswith("/admin/")

        if is_admin_route:
            # Use a different session cookie for admin
            request.COOKIES["sessionid"] = request.COOKIES.get(
                settings.ADMIN_SESSION_COOKIE_NAME
            )

        response = self.get_response(request)
        return response

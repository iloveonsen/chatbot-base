from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework.views import APIView


class RouteView(APIView):
    def get(self, request):
        routes = [
            {
                "path": "/api/",
                "description": "list of all available routes"
            }, 
        ]
        return Response(routes)
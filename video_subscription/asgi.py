import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "video_subscription.settings")

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import videos.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            videos.routing.websocket_urlpatterns
        )
    ),
})
from django.urls import path, include
from rest_framework_nested import routers
from .views import ConversationViewSet, MessageViewSet
from .auth import (CostomTokenObtainPairView, CostomTokenRefreshView,
                   LogoutView, RegisterView)

router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')


# Nested router: messages under conversations
conversations_router = routers.NestedDefaultRouter(
    router, r'conversations', lookup='conversation')
conversations_router.register(r'messages',
                              MessageViewSet, basename='conversation-messages')


urlpatterns = [
    path('api/', include(router.urls)),
    path('api/', include(conversations_router.urls)),
    path('token/', CostomTokenObtainPairView.as_view(), name='api_token'),
    path('refresh/', CostomTokenRefreshView.as_view(), name='api_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register')
]

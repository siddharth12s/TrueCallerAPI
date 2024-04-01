from django.urls import path,include
from app.views import  LoginView, RegisterView, ContactsViewSet, MarkUnmarkSpam, Search
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
# router.register(r'user', UserViewSet)
router.register(r'contacts',ContactsViewSet, basename='contacts')


urlpatterns = [
#    path('', include(router.urls)),
   path('login/', LoginView.as_view()),
   path('register/', RegisterView.as_view()),
   path('user/', include(router.urls)),
   path('user/<str:action>/<str:spam_number>/', MarkUnmarkSpam.as_view()),
   path('user/search/', Search.as_view())

]
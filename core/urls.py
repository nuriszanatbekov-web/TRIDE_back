from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    # Негизги баракчаны Свагерге багыттоо
    path('', lambda request: redirect('swagger-ui'), name='index'),

    path('admin/', admin.site.urls),

    # TRIDE API Бөлүмдөрү
    path('api/auth/', include('users.urls')),  # Колдонуучулар бөлүмү
    path('api/schedule/', include('schedule.urls')),  # Машыгуулар бөлүмү

    # Swagger документтери
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
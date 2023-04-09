from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

# from rest_framework_swagger.views import get_swagger_view

# schema_view = get_swagger_view(title='Quiz API')

schema_view = get_schema_view(
    openapi.Info(
        title="Quiz API",
        default_version='v1',
        description="Quiz app Api",
    ),
    public=True,
    permission_classes=[AllowAny],
)

urlpatterns = [
    # path('swagger/', schema_view),
    re_path(r'^doc(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('doc/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('user/', include('agent.urls')),
    path('', include('quiz.urls')),
    path('', include('common.urls')),
]

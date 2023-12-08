from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView, TemplateView

# from rest_framework.schemas import get_schema_view
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi



# for swagger ui
schema_view = get_schema_view(
    openapi.Info(
        title="NodeNet API Documentation",
        default_version='v1',
        description="API Documentation for the NodeNet social distribution web app",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# class SwaggerView(TemplateView):
#     template_name = 'docs.html'  # Specify your template name here
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['schema_url'] = 'api_schema'  # Add your extra content here
#         return context


urlpatterns = [
    path("",RedirectView.as_view(url="nodenet/")), # redirect root to homepage

    path("admin/", admin.site.urls),

    path("nodenet/", include("base.urls")),

    path("__reload__/", include("django_browser_reload.urls")),

    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),


    # path('api_schema', get_schema_view(title='API Schema', description='Guide for the REST API'), name='api_schema'),
    # path('swagger-ui/', SwaggerView.as_view(), name='swagger-ui'),

    path("api/", include("authors.urls")),
    path("api/authors/<str:author_id>/posts/<str:post_id>/", include("comments.urls")),
    #path("api/authors/<str:author_id>/posts/<str:post_id>/image", include("app_posts.urls")),
    path("api/authors/<str:author_id>/", include("app_posts.urls")),
    path("api/authors/<str:author_id>/posts/<str:post_id>/", include("likes.urls")),
    path("api/authors/<str:author_id>/posts/<str:post_id>/comments/<str:comment_id>/", include("likes.urls"),),
    path("api/authors/<str:author_id>/", include("inboxes.urls")),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# for images
# static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

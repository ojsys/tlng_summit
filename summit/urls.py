from django.urls import path

from . import cms, views

urlpatterns = [
    path('', views.home, name='home'),
    path('speakers/', views.speakers, name='speakers'),
    path('sponsorship/', views.sponsorship, name='sponsorship'),
    path('nomination/', views.nominations, name='nominations'),
    path('nomination-success/', views.nomination_success, name='nomination_success'),
    path('register/', views.registration, name='registration'),
    path('registration-success/', views.registration_success, name='registration_success'),
    path('gallery/', views.gallery, name='gallery'),
    path('gallery/<slug:slug>/', views.gallery_album, name='gallery_album'),

    # Live editing endpoints (staff only)
    path('cms/update/', cms.update_field, name='cms_update'),
    path('cms/gallery/<int:pk>/upload/', cms.gallery_upload, name='cms_gallery_upload'),
    path('cms/gallery/<int:pk>/reorder/', cms.gallery_reorder, name='cms_gallery_reorder'),
    path('cms/photo/<int:pk>/delete/', cms.gallery_photo_delete, name='cms_photo_delete'),
]

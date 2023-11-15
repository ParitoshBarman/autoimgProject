from django.contrib import admin
from django.urls import path
from autoimgApp import views
from django.contrib.sitemaps.views import sitemap
from autoimgProject.sitemaps import StaticViewsSitemap

sitemaps = {
    'sitemap': StaticViewsSitemap
}




urlpatterns = [
    path("", views.index, name='home'),
    path("about", views.about, name='about'),
    path("privacy_policy", views.privacy_policy, name='privacy_policy'),
    path("contact", views.contact, name='contact'),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    
]


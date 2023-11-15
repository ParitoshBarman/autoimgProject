from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

class StaticViewsSitemap(Sitemap):
    priority = 1.0
    changefreq = "daily"
    def items(self):
        return ['autoimgApp:home','autoimgApp:about','autoimgApp:contact','autoimgApp:privacy_policy']
    def location(self, item):
        return reverse(item)
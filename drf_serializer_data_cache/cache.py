from django.core.cache import cache, caches
from django.core.exceptions import ImproperlyConfigured

from drf_serializer_data_cache.settings import cache_settings

cache = cache
try:
    cache_backend = cache_settings.SERIALIZER_CACHE_BACKEND
    if cache_backend != "default":
        cache = caches[cache_backend]
except KeyError:
    raise ImproperlyConfigured("'{}' is a invalid CACHE_BACKEND".format(
        cache_settings.DEFAUL_CACHE_BACKEND))

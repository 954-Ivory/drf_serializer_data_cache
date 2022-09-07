# drf_serializer_data_cache

This repo was inspired by: [django-rest-framework-cache](https://github.com/Onyo/django-rest-framework-cache)

Implemented the feature to auto-discover serializer related models(by `bfs`), and clear serializer cache which be
changed.

[当然还有中文版](/README_zh.md)

## Installation

Not yet packaged to pip.

```shell

```

Add 'drf_serializer_data_cache' to your INSTALLED_APPS setting.

```python3
INSTALLED_APPS = (
    ...
    'drf_serializer_data_cache',
)
```

## Usage

You need to let your `ModelSerializer` to inherit the `CachedSerializerMixin`(Tips:`CachedSerializerMixin` must on left,
because of `mro`.):

```python
from rest_framework import serializers
from drf_serializer_data_cache.mixins import SerializerCacheMixin


class YourModelSerializer(SerializerCacheMixin, serializers.ModelSerializer):
    pass
```

## Configuration

To the cache successfully work you must configure the Django CACHES setting. We recomend that you take a look on Django
cache docs here:
[https://docs.djangoproject.com/en/stable/topics/cache/#setting-up-the-cache](https://docs.djangoproject.com/en/stable/topics/cache/#setting-up-the-cache)

### Using cache backend different of the default

If you need use a cache backend different of the default you can specify it on the `SERIALIZER_CACHE_BACKEND`.

To do this edit your `settings.py` like this:

```python
# ...
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379',
    },
    'local_memory': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

REST_FRAMEWORK_CACHE = {
    'SERIALIZER_CACHE_BACKEND': 'local_memory',
}
# ...
```

### Cache timeout

You can set the cache timeout using `SERIALIZER_CACHE_TIMEOUT`.

```python
REST_FRAMEWORK_CACHE = {
    'SERIALIZER_CACHE_TIMEOUT': 86400,  # Default is 1 day
}
```

### Related model signals

By default, This library will automatically connect to serializer related model signals.

When serializer related model instance changed, related cache will be deleted.

You can set it by `AUTO_DELETE_RELATED_CACHES`.

```python
REST_FRAMEWORK_CACHE = {
    'AUTO_DELETE_RELATED_CACHES': False  # Default is True
}
```
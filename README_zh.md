# drf_serializer_data_cache

这个存储库的灵感来自：[django-rest-framework-cache](https://github.com/Onyo/django-rest-framework-cache)

实现了自动发现序列化器相关模型（通过`bfs`算法），并清除被更改的序列化器缓存的功能。

## 安装

还未进行 pip 打包。

```shell

```

将 `drf_serializer_data_cache` 添加至 `INSTALLED_APPS` 中.

```python3
INSTALLED_APPS = (
    ...
    'drf_serializer_data_cache',
)
```

## 使用方法

只需要让你的`ModelSerializer`继承自`SerializerCacheMixin`（提示：遵循`mro`原则，`SerializerCacheMixin`必须在左边）。

```python
from rest_framework import serializers
from drf_serializer_data_cache.mixins import SerializerCacheMixin


class YourModelSerializer(SerializerCacheMixin, serializers.ModelSerializer):
    pass
```

## 设置项

要使缓存成功工作，您必须设置 Django `CACHES`。

建议您在此处查看 Django 缓存文档：
[https://docs.djangoproject.com/en/stable/topics/cache/#setting-up-the-cache](https://docs.djangoproject.com/en/stable/topics/cache/#setting-up-the-cache)

### 使用非默认的缓存后端

如果您需要使用非默认的缓存后端，您可以在 `SERIALIZER_CACHE_BACKEND` 中指定它。

在`settings.py`中设置，如下:

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

### 缓存过期时间

你可以设置`SERIALIZER_CACHE_TIMEOUT`，来设定缓存过期的时间。

```python
REST_FRAMEWORK_CACHE = {
    'SERIALIZER_CACHE_TIMEOUT': 86400,  # 默认为一天
}
```

### 关联模型信号

默认设置下，这个库将自动发现序列化器的相关模型，并通过`signal`进行调度。

当与`ModelSerializer`关联的模型实例发生变化时，将自动清除对应的序列化器缓存。

你可以通过`AUTO_DELETE_RELATED_CACHES`进行设置。

```python
REST_FRAMEWORK_CACHE = {
    'AUTO_DELETE_RELATED_CACHES': False  # 默认是打开的(True)
}
```
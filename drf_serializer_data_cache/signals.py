from django.db.models import signals
from drf_serializer_data_cache.cache import cache
from drf_serializer_data_cache.relations import BFSForIndirectRelation
from drf_serializer_data_cache.utils import get_dispatch_uid, get_cache_key, get_serializer_model_base


class RegistryRelation:
    def __init__(self, source, serializer, predicate):
        self.source = source
        self.serializer = serializer
        self.predicate = predicate


cache_registry = {}


def connect_cache_clear_signals(models, serializer):
    source = get_serializer_model_base(serializer)[0]
    indirect_relations = BFSForIndirectRelation(source)
    for model in models:
        predicate = indirect_relations.get_predicate(model)
        registry_relation = RegistryRelation(source, serializer, predicate)
        registry_item = cache_registry.setdefault(model, set())
        registry_item.add(registry_relation)
        signals.post_save.connect(
            cache_clear_handler, sender=model,
            dispatch_uid=get_dispatch_uid(model)
        )
        signals.pre_delete.connect(
            cache_clear_handler, sender=model,
            dispatch_uid=get_dispatch_uid(model)
        )
        signals.m2m_changed.connect(
            cache_clear_handler, sender=model,
            dispatch_uid=get_dispatch_uid(model)
        )


def cache_clear_handler(sender, instance, **kwargs):
    registry_relations = cache_registry.get(instance.__class__, [])
    keys = []
    for registry_relation in registry_relations:
        source = registry_relation.source
        serializer = registry_relation.serializer
        predicate = registry_relation.predicate
        relation_key = [get_cache_key(i, serializer) for i in source.objects.filter(**{predicate: instance.pk})]
        keys += relation_key
    cache.delete_many(keys)

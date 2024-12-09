from dishka import Provider, provide, Scope
from elasticsearch import AsyncElasticsearch

from app.settings import Settings


class ElasticSearchProvider(Provider):
    @provide(scope=Scope.APP)
    def get_es(self, settings: Settings) -> AsyncElasticsearch:
        return AsyncElasticsearch(hosts=f"{settings.ELASTICSEARCH_HOST}:{settings.ELASTICSEARCH_PORT}")
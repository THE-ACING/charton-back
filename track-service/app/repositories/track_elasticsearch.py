from dishka import Provider, provide, Scope
from elasticsearch import AsyncElasticsearch

from app.settings import Settings


class TrackElasticsearchRepository:
    def __init__(self, es: AsyncElasticsearch, index: str = "track_service"):
        self.__es = es
        self._index = index

    async def search(self, query: str, from_: int = 0, size: int = 10) -> dict:
        return await self.__es.search(
            index=self._index,
            body={
                "query": {
                    "bool": {
                        "should": [
                            {
                                "multi_match": {
                                    "query": query,
                                    "fields": [
                                        "title^3",
                                        "authors.name^2",
                                        "authors.genres^1"
                                    ],
                                    "fuzziness": "AUTO"
                                }
                            },
                            {
                                "multi_match": {
                                    "query": query,
                                    "fields": [
                                        "title.keyword^10",
                                        "authors.name.keyword^8",
                                        "authors.genres.keyword^6"
                                    ],
                                    "type": "phrase"
                                }
                            }
                        ]
                    }
                },
            },
            from_=from_,
            size=size
        )


class TrackElasticsearchProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_track_elasticsearch_repository(self, es: AsyncElasticsearch,
                                           settings: Settings) -> TrackElasticsearchRepository:
        return TrackElasticsearchRepository(es, settings.ELASTICSEARCH_INDEX)

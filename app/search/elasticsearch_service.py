from elasticsearch import Elasticsearch


class ElasticsearchService:
    def __init__(self):
        self.client: Elasticsearch | None = None
        self.index_name = "documents"

    def connect(self):
        if self.client is not None:
            print("Elasticsearch уже подключен")
            return

        self.client = Elasticsearch(
            ["http://localhost:9200"],
            request_timeout=30,
            max_retries=3,
            retry_on_timeout=True,
            headers={
                'Accept': 'application/vnd.elasticsearch+json;compatible-with=9',
                'Content-Type': 'application/json'
            }
        )
        print('Elasticsearch подключен')

    def create_index(self):
        if self.client is None:
            print("Elasticsearch не подключен")
            return

        if self.client.indices.exists(index=self.index_name):
            print("Индекс уже существует")
            return

        self.client.indices.create(
            index=self.index_name,
            body={
                "mappings": {
                    "properties": {
                        "text": {"type": "text"}
                    }
                }
            }
        )
        print("✅ Индекс создан")

    def index_document(self, doc_id: int, body: dict):
        if self.client is None:
            print("Elasticsearch не подключен")
            return

        self.client.index(
            index=self.index_name,
            id=str(doc_id),
            body=body
        )

    def close(self):
        if self.client is not None:
            self.client.close()
            self.client = None
            print("Elasticsearch отключен")


es_service = ElasticsearchService()

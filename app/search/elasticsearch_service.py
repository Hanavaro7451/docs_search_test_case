from elasticsearch import Elasticsearch


class ElasticsearchService:
    def __init__(self):
        self.client = None
        self.index_name = "documents"

    def connect(self):
        self.client = Elasticsearch(
            ["http://localhost:9200"],
            request_timeout=30,
            max_retries=3,
            retry_on_timeout=True,
            meta_header=False
        )
        print('✅ Elasticsearch подключен')

    def create_index(self):
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
        self.client.index(
            index=self.index_name,
            id=doc_id,
            body=body
        )


es_service = ElasticsearchService()

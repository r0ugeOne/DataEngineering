from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.schema_registry_client import Schema



with open("/Users/solo/Projects/DataEngineering/projects/01-Kafka/retail-data-avro.json") as f:
    schema_str = f.read()

schema_registry_conf = {
    'url': 'http://localhost:8081'
}

schema_registry_client = SchemaRegistryClient(schema_registry_conf)

schema = Schema(
    schema_str,
    schema_type="AVRO"
)

schema_id = schema_registry_client.register_schema(schema=schema, subject_name="orders")
print(f"Schema registered with ID: {schema_id}")
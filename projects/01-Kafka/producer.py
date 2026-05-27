import time
import pandas as pd
from confluent_kafka import SerializingProducer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import StringSerializer
from config import get_settings

settings = get_settings()

TOPIC = 'retail_data_Dev'
SUBJECT_NAME = f'{TOPIC}-value'

def delivery_report(err, msg):
    """
    Reports the failure or success of a message delivery.

    Args:
        err (KafkaError): The error that occurred on None on success.

        msg (Message): The message that was produced or failed.

    Note:
        In the delivery report callback the Message.key() and Message.value()
        will be the binary format as encoded by any configured Serializers and
        not the same object that was passed to produce().
        If you wish to pass the original object(s) for key and value to delivery
        report callback we recommend a bound callback or lambda where you pass
        the objects along.

    """
    if err is not None:
        print("Delivery failed for User record {}: {}".format(msg.key(), err))
        return
    print('User record {} successfully produced to {} [{}] at offset {}'.format(
        msg.key(), msg.topic(), msg.partition(), msg.offset()))
    print("=====================")

def get_schema_and_version(client: SchemaRegistryClient, subject: str):

    """Fetch latest schema + version number for auditing/logging."""

    latest = client.get_latest_version(subject)
    print(f"[Schema] Subject: {subject} | Version: {latest.version} | ID: {latest.schema_id}")
    print(f"[Schema] {latest.schema.schema_str}\n{'='*40}")
    return latest.schema.schema_str, latest.version

def build_producer():

    schema_registry_client = SchemaRegistryClient({
        'url': settings.SCHEMA_BOOTSTRAP_SERVER,
        'basic.auth.user.info': f'{settings.SCHEMA_USERNAME}:{settings.SCHEMA_PASSWORD}'
    })

    schema_str , schema_version = get_schema_and_version(schema_registry_client,SUBJECT_NAME)
    avro_serializer = AvroSerializer(schema_registry_client, schema_str)

    return SerializingProducer({
        'bootstrap.servers': settings.BOOTSTRAP_SERVER,
        'sasl.mechanisms': settings.SASL_MECHANISM,
        'security.protocol': settings.SECURITY_PROTOCOL,
        'sasl.username': settings.SASL_USERNAME,
        'sasl.password': settings.SASL_PASSWORD,
        'key.serializer': StringSerializer('utf_8'),
        'value.serializer': avro_serializer,
    })

def produce(df: pd.DataFrame):

    producer = build_producer()

    for index, row in df.iterrows():
        try:
            print(row.to_dict())

            producer.produce(
                topic=TOPIC,
                key=str(index),
                value=row.to_dict(),
                on_delivery=delivery_report,
            )
            producer.poll(0)
        except Exception as e:
            print(f"[Error] Failed to produce record {index}: {e}")
            continue

        time.sleep(4)

    producer.flush()
    print("All data successfully published to Kafka.")


if __name__ == '__main__':
    df = pd.read_csv('/Users/solo/Projects/DataEngineering/projects/01-Kafka/dataset/retail_data.csv')
    df = df.fillna('null')
    print(df.head(5))
    produce(df)
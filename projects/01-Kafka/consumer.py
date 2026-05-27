import json
import logging
from typing import Optional
import pandas as pd
from confluent_kafka import DeserializingConsumer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import StringDeserializer
from config import get_settings

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

settings = get_settings()

TOPIC = 'retail_data_Dev'
SUBJECT_NAME = f'{TOPIC}-value'

def get_schema_and_version(client: SchemaRegistryClient, subject: str) -> tuple:
    """Fetch latest schema + version number for auditing/logging."""
    try:
        latest = client.get_latest_version(subject)
        logger.info(
            f"Schema loaded | Subject: {subject} | Version: {latest.version} | ID: {latest.schema_id}"
        )
        logger.debug(f"Schema content: {latest.schema.schema_str}")
        return latest.schema.schema_str, latest.version
    except Exception as e:
        logger.error(f"Failed to fetch schema for {subject}: {e}")
        raise

def build_consumer() -> DeserializingConsumer:
    """Build and configure Kafka consumer with Avro deserialization."""
    try:
        schema_registry_client = SchemaRegistryClient({
            'url': settings.SCHEMA_BOOTSTRAP_SERVER,
            'basic.auth.user.info': f'{settings.SCHEMA_USERNAME}:{settings.SCHEMA_PASSWORD}'
        })
        
        schema_str, schema_version = get_schema_and_version(schema_registry_client, SUBJECT_NAME)
        avro_deserializer = AvroDeserializer(schema_registry_client, schema_str)

        consumer_config = {
            'bootstrap.servers': settings.BOOTSTRAP_SERVER,
            'sasl.mechanisms': settings.SASL_MECHANISM,  # Fixed: was SALS_MECHANISM
            'security.protocol': settings.SECURITY_PROTOCOL,  # Fixed: was SECURITY_PROTOCAL
            'sasl.username': settings.SASL_USERNAME,  # Fixed: was SALS_USERNAME
            'sasl.password': settings.SASL_PASSWORD,
            'key.deserializer': StringDeserializer('utf_8'),  # Fixed: was key.serializer
            'value.deserializer': avro_deserializer,  # Fixed: was value.serializer
            'group.id': 'group2',
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': True,  # Auto-commit offsets
            'auto.commit.interval.ms': 5000,  # Commit every 5 seconds
            'session.timeout.ms': 30000,  # Session timeout
            'fetch.max.bytes': 52428800,  # 50MB max fetch size
        }

        consumer = DeserializingConsumer(consumer_config)
        logger.info("Kafka consumer initialized successfully")
        return consumer

    except Exception as e:
        logger.error(f"Failed to initialize consumer: {e}")
        raise

def consume():
    """Subscribe to topic and consume messages with error handling."""
    consumer = build_consumer()
    
    try:
        consumer.subscribe([TOPIC])
        logger.info(f"Subscribed to topic: {TOPIC}")

        message_count = 0
        
        while True:
            msg = consumer.poll(timeout=1.0)

            if msg is None:
                continue

            if msg.error():
                # Handle different error codes
                error_code = msg.error().code()
                if error_code == -191:  # EOF
                    logger.debug("Reached end of partition")
                else:
                    logger.error(f'Consumer error [{error_code}]: {msg.error()}')
                continue

            try:
                message_count += 1
                key = msg.key()
                value = msg.value()
                offset = msg.offset()
                partition = msg.partition()

                logger.info(
                    f"Message consumed | Partition: {partition} | Offset: {offset} | "
                    f"Key: {key} | Timestamp: {msg.timestamp()}"
                )
                
                # Process the message (example: convert to DataFrame)
                if isinstance(value, dict):
                    df = pd.DataFrame([value])
                    print(df.to_dict('records'))
                    logger.debug(f"Converted message to DataFrame shape {df.shape}")
                
                # Add your business logic here
                # process_message(value)

            except Exception as e:
                logger.error(f"Error processing message at offset {msg.offset()}: {e}", exc_info=True)
                # Decide: continue or break based on error severity
                continue

            # Optional: Log periodic stats
            if message_count % 100 == 0:
                logger.info(f"Total messages consumed: {message_count}")

    except KeyboardInterrupt:
        logger.info("Consumer interrupted by user (Ctrl+C)")
    except Exception as e:
        logger.error(f"Unexpected error in consumer loop: {e}", exc_info=True)
    finally:
        # Graceful shutdown with timeout
        logger.info("Closing consumer...")
        try:
            consumer.close(timeout_ms=10000)
            logger.info("Consumer closed successfully")
        except Exception as e:
            logger.error(f"Error closing consumer: {e}")


if __name__ == "__main__":
    try:
        consume()
    except Exception as e:
        logger.critical(f"Fatal error: {e}", exc_info=True)
        exit(1)
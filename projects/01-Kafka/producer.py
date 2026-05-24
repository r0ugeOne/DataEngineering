from kafka import KafkaProducer
import json
import time
import random
from datetime import datetime

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

products = [
    "iPhone",
    "Laptop",
    "Headphones",
    "Keyboard",
    "Monitor"
]

while True:

    order = {
        "order_id": random.randint(1000, 9999),
        "product": random.choice(products),
        "price": random.randint(100, 5000),
        "quantity": random.randint(1, 5),
        "timestamp": datetime.now().isoformat()
    }

    producer.send("orders", value=order)

    print(f"Produced: {order}")

    time.sleep(2)
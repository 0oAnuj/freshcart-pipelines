import json
import random
import time
import uuid
from datetime import datetime, timezone

import pika

AMQP_URL = "amqp://guest:guest@localhost:5672/%2F"
EXCHANGE = "rapido-dispatch"


def main():
    connection = pika.BlockingConnection(pika.URLParameters(AMQP_URL))
    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE, exchange_type="topic", durable=True)

    cities = ["bangalore", "chennai"]
    zones = ["koramangala", "indiranagar", "whitefield", "tnagar"]
    order_types = ["ride", "food"]

    print("Starting dispatcher: one message every 2 seconds; bad data every 10th message")
    try:
        for count in range(1, 31):
            city = random.choice(cities)
            zone = random.choice(zones)
            order_type = random.choice(order_types)
            routing_key = f"{city}.{zone}.{order_type}"
            message = {
                "id": str(uuid.uuid4()),
                "city": city,
                "zone": zone,
                "type": order_type,
                "ts": datetime.now(timezone.utc).isoformat(),
            }

            if count % 10 == 0:
                message.pop("zone")
                print(f"[x] BAD message: {routing_key}")
            else:
                print(f"[x] message: {routing_key}")

            channel.basic_publish(
                exchange=EXCHANGE,
                routing_key=routing_key,
                body=json.dumps(message),
                properties=pika.BasicProperties(content_type="application/json"),
            )
            time.sleep(2)
    finally:
        connection.close()


if __name__ == "__main__":
    main()

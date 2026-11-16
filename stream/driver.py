import json
import sys

import pika

AMQP_URL = "amqp://guest:guest@localhost:5672/%2F"
EXCHANGE = "rapido-dispatch"


def main():
    if len(sys.argv) != 3:
        raise SystemExit("Usage: python stream/driver.py NAME PATTERN")

    name, pattern = sys.argv[1:]
    connection = pika.BlockingConnection(pika.URLParameters(AMQP_URL))
    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE, exchange_type="topic", durable=True)

    queue_name = channel.queue_declare(queue="", exclusive=True).method.queue
    channel.queue_bind(exchange=EXCHANGE, queue=queue_name, routing_key=pattern)
    print(f"[{name}] waiting for messages matching {pattern!r}")

    def handle_message(ch, method, properties, body):
        try:
            message = json.loads(body)
        except json.JSONDecodeError:
            print(f"[{name}] invalid JSON; discarding message")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            return

        if not message.get("zone"):
            print(f"[{name}] missing zone; discarding {message.get('id', '<unknown>')}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            return

        print(f"[{name}] accepted {message['id']}: {message}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=handle_message)
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    finally:
        connection.close()


if __name__ == "__main__":
    main()

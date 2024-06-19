import pika
import json


def publish(method, body):
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="project_rabbitmq", port=5672)
        )
        channel = connection.channel()
        properties = pika.BasicProperties(method)
        channel.basic_publish(
            exchange="",
            routing_key="project_queue",
            body=json.dumps(body),
            properties=properties,
        )
        print(f" [x] Sent '{body}'")
    except pika.exceptions.AMQPError as e:
        print(f"Failed to publish message: {e}")
    finally:
        if connection and connection.is_open:
            connection.close()

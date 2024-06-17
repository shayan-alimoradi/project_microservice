import pika
import json

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="project_rabbitmq", port=5672)
)
channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(
        exchange="",
        routing_key="project_queue",
        body=json.dumps(body),
        properties=properties,
    )
    print(f" [x] Sent '{body}'")

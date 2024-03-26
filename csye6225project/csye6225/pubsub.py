import json
from google.cloud import pubsub_v1


def publish_message_to_pubsub(project_id, topic_name, message):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)
    data = json.dumps(message).encode("utf-8")
    future = publisher.publish(topic_path, data)
    future.result()  # Ensure the message is published


import os
import pulsar
import sys

def main():
    service_url = os.environ.get("PULSAR_SERVICE_URL", "pulsar://my-pulsar-broker.pulsar.svc.cluster.local:6650")
    topic = os.environ.get("TOPIC", "persistent://public/default/my-topic")
    subscription_name = os.environ.get("SUBSCRIPTION_NAME", "my-subscription")

    client = pulsar.Client(service_url)
    consumer = client.subscribe(topic, subscription_name, consumer_type=pulsar.ConsumerType.Shared)

    print("Consumer started, waiting for messages...")
    try:
        while True:
            msg = consumer.receive()
            try:
                print("Received message '{}', message ID: {}".format(msg.data().decode('utf-8'), msg.message_id()))
                consumer.acknowledge(msg)
            except Exception as processing_error:
                print("Error processing message: {}".format(processing_error), file=sys.stderr)
                consumer.negative_acknowledge(msg)
    except KeyboardInterrupt:
        print("Consumer interrupted, closing client...")
    finally:
        consumer.close()
        client.close()

if __name__ == "__main__":
    main()

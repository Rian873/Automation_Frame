import os
import asyncio
import pulsar

async def produce_messages_loop(client, topic, messages_per_second):
    producer = client.create_producer(topic)
    message_counter = 0

    try:
        while True:
            start_time = asyncio.get_running_loop().time()
            tasks = []
            for _ in range(messages_per_second):
                message = f"message {message_counter}".encode('utf-8')
                tasks.append(asyncio.to_thread(producer.send, message))
                message_counter += 1

            await asyncio.gather(*tasks)
            elapsed = asyncio.get_running_loop().time() - start_time
            sleep_time = max(0, 1 - elapsed)
            await asyncio.sleep(sleep_time)
    finally:
        producer.close()

def main():
    service_url = os.environ.get("PULSAR_SERVICE_URL", "pulsar://my-pulsar-broker.pulsar.svc.cluster.local:6650")
    topic = os.environ.get("TOPIC", "persistent://public/default/my-topic")
    messages_per_second = int(os.environ.get("MESSAGES_PER_SECOND", "1000"))
    
    client = pulsar.Client(service_url)
    try:
        asyncio.run(produce_messages_loop(client, topic, messages_per_second))
    finally:
        client.close()

if __name__ == "__main__":
    main()

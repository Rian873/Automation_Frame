import pulsar

# Use the proxy's external IP and binary port
client = pulsar.Client('pulsar://20.251.95.246')

consumer = client.subscribe('234', subscription_name='abc')

print("Listening for messages...")
while True:
    msg = consumer.receive()
    print(f'Received: {msg.data().decode("utf-8")}')
    consumer.acknowledge(msg)


client.close()

import pulsar

# Use the proxy's external IP and binary port
client = pulsar.Client('pulsar://20.251.95.246')

producer = client.create_producer('234')

for i in range(10):
    producer.send(f'Hello Pulsar {i}'.encode('utf-8'))
    print(f'Sent: Hello Pulsar {i}')

client.close()
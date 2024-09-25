import asyncio
from model.network.client import Client

if __name__ == '__main__':
    client = Client('192.168.1.88', '8082')
    asyncio.run(client.run())
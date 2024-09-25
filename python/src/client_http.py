import asyncio
import aiohttp
import ssl

class Client:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.url = f'https://{self.ip}:{self.port}/req'
        self.cert_path = '/home/jpires/Dev/Jarvis-AI-Assistant/python/src/server.cert'

        # Create SSL context
        self.ssl_context = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH)
        self.ssl_context.load_verify_locations(self.cert_path)

    async def send_request(self, data):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(self.url, json=data, ssl=self.ssl_context) as response:
                    if response.status == 200:
                        return await response.json()  # Return the JSON response from the server
                    else:
                        print('Failed to send request:', response.status)
                        return None
            except Exception as e:
                print('Error sending request:', e)
                return None

    async def handle_request(self):
        while True:
            data = {
                'device': 'Desktop',
                'status': 'Online'
            }

            print('Sending request...')
            response = await self.send_request(data)

            if response:
                print('Received response:', response)

            await asyncio.get_event_loop().run_in_executor(None, input, 'Press Enter to send another request...')

    async def run(self):
        # Create tasks for handling requests with and without user input
        input_task = asyncio.create_task(self.handle_request())
        request_task = asyncio.create_task(self.handle_request())

        # Wait for both tasks to complete
        await asyncio.gather(input_task, request_task)
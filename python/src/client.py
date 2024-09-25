import websockets
import asyncio
import json
import sys

class Client:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.url = f'ws://{self.ip}:{self.port}'
        self.websocket = None

    # Establish a connection to the server
    async def connect(self):
        while not self.websocket:
            try:
                self.websocket = await websockets.connect(self.url)
                print("Connected to the server")
            except Exception as e:
                print(f"Failed to connect: {e}\nRetrying in 5 seconds...")
                await asyncio.sleep(5)  # Retry every 5 seconds

    # Send a request over WebSocket and wait for the response
    async def send_request(self, data):
        try:
            # Ensure the connection is established
            if self.websocket is None or not self.websocket.open:
                await self.connect()

            if self.websocket:
                # Convert data to JSON if it's a dictionary
                if isinstance(data, dict):
                    data = json.dumps(data)

                # Send the data
                await self.websocket.send(data)
                print(f"Sent: {data}")

        except Exception as e:
            print('Error sending request:', e)
            return None

    # Receive messages from the server
    async def receive_messages(self):
        print("Receiving messages...")
        try:
            while True:
                message = await self.websocket.recv()
                print(f"Received: {message}")
        except websockets.ConnectionClosed:
            print("Connection closed")
        except Exception as e:
            print(f"Error receiving message: {e}")

    # Handle user input asynchronously
    async def handle_input(self):
        while True:
            user_input = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            user_input = user_input.strip()
            try:
                json_data = json.loads(user_input)  # Validate JSON
                await self.send_request(json_data)
            except json.JSONDecodeError:
                print("Invalid JSON format. Please enter a valid JSON string.")

    # Run both sending and receiving tasks in parallel
    async def run(self):
        await self.connect()
        
        # Start receiving messages in the background
        asyncio.create_task(self.receive_messages())

        # Start handling user input in the background
        asyncio.create_task(self.handle_input())

        # Keep the program running
        while True:
            await asyncio.sleep(1)  # Prevent the main loop from exiting
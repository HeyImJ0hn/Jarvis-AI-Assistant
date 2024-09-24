import requests
import asyncio
import aiohttp

class Client:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.url = f'https://{self.ip}:{self.port}/req'
        self.cert_path = '/home/jpires/Dev/Jarvis-AI-Assistant/python/src/server.cert'

    def send_request(self, data):
        try:
            response = requests.post(self.url, json=data, verify=self.cert_path)
            if response.status_code == 200:
                return response.json()  # Return the JSON response from the server
            else:
                print('Failed to send request:', response.status_code, response.text)
                return None
        except requests.exceptions.RequestException as e:
            print('Error sending request:', e)
            return None
        
    def run(self):
        while True:
            data = {
                'device': 'Desktop',
                'status': 'Online'
            }

            print('Sending request...')
            response = self.send_request(data)
            
            if response:
                print('Received response:', response)

            input('Press Enter to send another request...')
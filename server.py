import websockets
import datetime
import asyncio

class Server:
    def __init__(self, local_host = "0.0.0.0", port = 8080):
        self.local_host = local_host
        self.port = port
        self.clients = []

    async def client_messages(self, websocket):
        try:
            now = datetime.datetime.now().strftime("%d/%m%Y %H:%M")
            async for message in websocket:
                print(f"{websocket.remote_address} - {now}: {message}")
                for client in list(self.clients): 
                    try:
                        await client.send(formatted)
                    except websockets.exceptions.ConnectionClosed:
                         #remove a client when the connection is closed by the client so we stop the broadcast to this client
                        try:
                            self.clients.remove(client) 
                        except ValueError:
                           # Client not in self.clients list don´t throw 
                            pass
        except websockets.exceptions.ConnectionClosed:
            print("Connection was lost")
            
    
    async def server_messages(self, websocket):
            try:
                while True:
                    message = await asyncio.to_thread(input, f"{self.local_host}")
                    now = datetime.datetime.now().strftime("%d/%m%Y %H:%M")
                    formatted = f"{now}: {message}"

                # core groupechat feature broadcasting to all clients connected
                                # core groupechat feature broadcasting to all clients connected
                for client in list(self.clients):
                    try:
                        await client.send(formatted)
                    except websockets.exceptions.ConnectionClosed:
                        # Entferne geschlossene Verbindungen aus der Liste
                        try:
                            self.clients.remove(client)
                        except ValueError:
                            pass
        except websockets.exceptions.ConnectionClosed:
            print("Connection was lost")

    async def handle_connections(self, websocket, path=None):
        print(
            f"new connection from {websocket.remote_address}\n Type here to send a message...")
        self.clients.append(websocket)
        try:
            await asyncio.gather(
                self.server_messages(websocket),
                self.client_messages(websocket)
            )
        except Exception as e:
            print(e)

    async def server_start(self):
        async with websockets.serve(self.handle_connections, self.local_host, self.port):
            print(f"Server has started on {self.local_host}:{self.port}")
            await asyncio.Future()


if __name__ == "__main__":
    server = Server()
    asyncio.run(server.server_start())




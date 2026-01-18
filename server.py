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
            now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
            async for message in websocket:
                print(f"{now} -  : {message}")
                 #write meessage into db
        except websockets.exceptions.ConnectionClosed:
            print(f"Connection with {websocket.remote_address} was lost")
    
    async def server_messages(self, websocket):
            try:
                while True:
                    message = await asyncio.to_thread(input, f"")
                    now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
                    await websocket.send(f"{message}")
                    #write meessage into db
            except websockets.exceptions.ConnectionClosed:
                print(f"Connection with {websocket.remote_address} was lost")

    async def handle_connections(self, websocket):
        print(f"New connection from {websocket.remote_address}\nType here to send a message...\n")
        await websocket.send("")
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

    async def account_check(websocket):
        try:
            await websocket.send("Welcome to Wazzap.\nPlease identify yourself to create an account: ")
            while True:
                    await websocket.send("Please enter your username: ")
                    username = await websocket.recv()
                    if not username.strip():
                        await websocket.send("ERROR:Username cannot be empty")
                        continue
                
                #try:
                #   write in db under u 
                #   print("Login successful)
                #   return
                #except db error:
                #  print("Use a different username")
                #    continue
        except websockets.exceptions.ConnectionClosed:
            print(f"Connection with {websocket.remote_address} was lost")

if __name__ == "__main__":
    server = Server()
    asyncio.run(server.server_start())



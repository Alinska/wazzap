import asyncio
import websockets
import socket
import datetime


async def receive_messages(websocket):
    """
    Diese Funktion empfängt Nachrichten vom Server.
    Sie läuft in einer Endlosschleife und gibt jede Nachricht mit Zeitstempel aus.
    """
    try:
        async for message in websocket:
            now = datetime.datetime.now().strftime("%d/%m%Y %H:%M")
            print(f"{websocket.remote_address} - {now}: {message}")
    except websockets.exceptions.ConnectionClosed:
        print("\nVerbindung vom Server geschlossen.")
    except Exception as e:
        print(f"\nFehler beim Empfangen: {e}")


async def send_messages(websocket):
    """
    Diese Funktion sendet Nachrichten an den Server.
    Sie wartet auf Eingabe vom Benutzer und sendet diese dann an den Server.
    """
    try:
        while True:
            now = datetime.datetime.now().strftime("%d/%m%Y %H:%M")
            # Warte auf Eingabe vom Benutzer (blockiert nicht, weil in separatem Thread)
            message = await asyncio.to_thread(input, f"{now} - {socket.gethostname()}: ")
            # Sende die Nachricht an den Server
            await websocket.send(f"{now}: {message}")
    except websockets.exceptions.ConnectionClosed:
        # Hier kein Fehlerdruck nötig, da receive_messages das bereits meldet
        pass
    except Exception as e:
        print(f"\nFehler beim Senden: {e}")


async def connect_to_server():
    """
    Hauptfunktion: Verbindet sich mit dem Server und startet den Chat.

    ABLAUF:
    1. Verbindung zum Server herstellen
    2. Login-Prozess durchführen (Username zuweisen/verifizieren)
    3. Nach erfolgreichem Login: Senden und Empfangen von Nachrichten parallel starten
    """
    uri = "ws://127.0.0.1:8080"
    try:
        async with websockets.connect(uri) as websocket:
            # ===== LOGIN-PHASE =====
            while True:
                try:
                    msg = await websocket.recv()
                except websockets.exceptions.ConnectionClosed:
                    print("\nServer hat die Verbindung während des Logins beendet.")
                    return

                print(msg + "\n")

                if "Login successful" in msg:
                    break

                if "ERROR" in msg:
                    continue

                if "Do you already have a username?" in msg or "Please enter your username:" in msg:
                    response = input().strip()
                    await websocket.send(response)

            # Empfange Login-Signal (leere Nachricht)
            try:
                await websocket.recv()
            except websockets.exceptions.ConnectionClosed:
                return

            # Warte auf Chat-Start
            chat_ready = False
            while not chat_ready:
                try:
                    msg = await websocket.recv()
                except websockets.exceptions.ConnectionClosed:
                    print("\nVerbindung während der Wartephase verloren.")
                    return

                print(msg + "\n")
                if "Chat is now active" in msg or "Waiting" in msg:
                    chat_ready = True

            # ===== CHAT-PHASE =====
            await asyncio.gather(
                receive_messages(websocket),
                send_messages(websocket)
            )
    except ConnectionRefusedError:
        print("\nFehler: Server ist nicht erreichbar (nicht gestartet?)")
    except Exception as e:
        print(f"\nUnerwarteter Fehler: {e}")

# Starte das Programm
asyncio.run(connect_to_server())

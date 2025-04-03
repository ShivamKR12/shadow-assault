from ursina import *
import asyncio
import websockets
import base64
import io
from PIL import Image
import threading
from panda3d.core import loadPrcFileData

# ---- Fix 1: Ensure valid integer window size ----
loadPrcFileData("", "win-size 800 600")  # Use integers for width and height

# ---- Fix 2: Disable audio to avoid OpenAL errors ----
loadPrcFileData("", "audio-library-name null")

# Ursina setup
app = Ursina()

# Example Cube
cube = Entity(model='cube', color=color.orange, scale=(2, 2, 2))

# WebSocket Server
async def send_frames(websocket):
    while True:
        # Capture game frame
        pixels = app.screenshot(name=None)  # Take a screenshot
        img = Image.open(pixels)
        
        # Convert to base64
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        # Send frame over WebSocket
        await websocket.send(img_str)
        await asyncio.sleep(1 / 30)  # 30 FPS

async def websocket_handler(websocket, path):
    try:
        await send_frames(websocket)
    except websockets.exceptions.ConnectionClosedError:
        print("WebSocket connection closed.")
    except Exception as e:
        print(f"WebSocket error: {e}")

async def run_websocket():
    async with websockets.serve(websocket_handler, "0.0.0.0", 8765):
        print("WebSocket server started at ws://0.0.0.0:8765")
        await asyncio.Future()  # Keeps the server running

# ---- Fix 3: Ensure WebSocket runs with asyncio.run() ----
def start_websocket_server():
    asyncio.run(run_websocket())

# Run WebSocket in background
server_thread = threading.Thread(target=start_websocket_server, daemon=True)
server_thread.start()

# Run Ursina (on the main thread)
app.run()

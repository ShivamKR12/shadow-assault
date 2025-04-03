import asyncio
import websockets

async def test_websocket():
    async with websockets.connect("ws://https://jubilant-space-bassoon-jjr4r6ggpr553jppv-8765.app.github.dev") as ws:
        frame = await ws.recv()
        print("Received Frame:", frame[:100])  # Print first 100 chars

asyncio.run(test_websocket())

import asyncio
import json
import websockets
import logging

from world import World
from simulation import Simulation
from vessel import Vessel
from position import Position

# -------------------------
# Logging setup
# -------------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# -------------------------
# Initial simulation setup
# -------------------------
own = Vessel(
    vessel_id="OWN",
    position=Position(0.0, 0.0),
    speed_knots=10.0,
    heading_deg=0.0,
)

targets = [
    Vessel("T1", Position(2.0, 8.0), 8.0, 180.0),
    Vessel("T2", Position(-5.0, 5.0), 12.0, 90.0),
]

world = World(own, targets)
simulation = Simulation(world)


# -------------------------
# WebSocket handler
# -------------------------
async def handler(websocket):
    logger.info("New WebSocket connection established")
    try:
        async for message in websocket:
            data = json.loads(message)
            cmd = data.get("command")
            logger.info(f"Received command: {cmd}")

            if cmd == "start":
                logger.info("Starting simulation")
                simulation.start()

            elif cmd == "pause":
                logger.info("Pausing simulation")
                simulation.pause()

            elif cmd == "step":
                dt = data.get("dt", 0.1)
                logger.info(f"Stepping simulation with dt={dt}")
                simulation.step(dt)

            elif cmd == "speed":
                speed = data["value"]
                logger.info(f"Setting simulation speed to {speed}")
                simulation.set_speed(speed)

            elif cmd == "add_target":
                target_id = data["id"]
                logger.info(f"Adding target vessel: {target_id} at ({data['x']}, {data['y']}) with speed {data['speed']} knots")
                t = Vessel(
                    vessel_id=target_id,
                    position=Position(data["x"], data["y"]),
                    speed_knots=data["speed"],
                    heading_deg=data["heading"],
                )
                world.add_target(t)

            elif cmd == "remove_target":
                target_id = data["id"]
                logger.info(f"Removing target vessel: {target_id}")
                world.remove_target(target_id)

            else:
                logger.warning(f"Unknown command received: {cmd}")

            # Always respond with fresh snapshot
            snapshot = world.snapshot()
            logger.debug("Sending world snapshot to client")
            await websocket.send(json.dumps(snapshot))
    except websockets.exceptions.ConnectionClosed:
        logger.info("WebSocket connection closed")
    except Exception as e:
        logger.error(f"Error in WebSocket handler: {e}", exc_info=True)


# -------------------------
# Server loop
# -------------------------
async def main():
    logger.info("Starting WebSocket server on ws://localhost:8765")
    async with websockets.serve(handler, "localhost", 8765):
        logger.info("WebSocket server is running and ready for connections")
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())

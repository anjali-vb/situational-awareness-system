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
    format="%(asctime)s - %(levelname)s - %(message)s",
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
    Vessel("DANGER1", Position(0.5, 3.0), 15.0, 190.0),  # Approaching head-on, CPA < 0.5nm
]

world = World(own, targets)
simulation = Simulation(world)

# -------------------------
# WebSocket handler
# -------------------------
async def handler(websocket):
    global world, simulation  # Declare at top for reset command
    logger.info("New WebSocket connection established")
    try:
        async for message in websocket:
            data = json.loads(message)
            cmd = data.get("command")
            logger.info(f"Received command: {cmd}")

            # -------------------------
            # Simulation control
            # -------------------------
            if cmd == "start":
                simulation.start()

            elif cmd == "pause":
                simulation.pause()

            elif cmd == "step":
                dt = data.get("dt", 0.1)
                simulation.step(dt)

            elif cmd == "speed":
                simulation.set_speed(data["value"])

            elif cmd == "reset":
                # Reset to initial state
                own = Vessel(
                    vessel_id="OWN",
                    position=Position(0.0, 0.0),
                    speed_knots=10.0,
                    heading_deg=0.0,
                )
                targets = [
                    Vessel("T1", Position(2.0, 8.0), 8.0, 180.0),
                    Vessel("T2", Position(-5.0, 5.0), 12.0, 90.0),
                    Vessel("DANGER1", Position(0.5, 3.0), 15.0, 190.0),
                ]
                world = World(own, targets)
                simulation = Simulation(world)
                logger.info("Simulation reset to initial state")

            # -------------------------
            # Target management
            # -------------------------
            elif cmd == "add_target":
                t = Vessel(
                    vessel_id=data["id"],
                    position=Position(data["x"], data["y"]),
                    speed_knots=data["speed"],
                    heading_deg=data["heading"],
                )
                world.add_target(t)

            elif cmd == "remove_target":
                world.remove_target(data["id"])

            # -------------------------
            # Own vessel course control (NEW)
            # -------------------------
            elif cmd == "update_own_heading":
                heading = data["heading_deg"]
                logger.info(f"Updating own vessel heading to {heading}")
                world.update_own_heading(heading)

            elif cmd == "update_own_speed":
                speed = data["speed_knots"]
                logger.info(f"Updating own vessel speed to {speed}")
                world.update_own_speed(speed)

            # -------------------------
            # Target vessel course control (NEW)
            # -------------------------
            elif cmd == "update_target_heading":
                vessel_id = data["id"]
                heading = data["heading_deg"]
                updated = world.update_target_heading(vessel_id, heading)
                logger.info(
                    f"Updated heading for {updated} target(s) with id={vessel_id}"
                )

            elif cmd == "update_target_speed":
                vessel_id = data["id"]
                speed = data["speed_knots"]
                updated = world.update_target_speed(vessel_id, speed)
                logger.info(
                    f"Updated speed for {updated} target(s) with id={vessel_id}"
                )

            else:
                logger.warning(f"Unknown command received: {cmd}")

            # -------------------------
            # Always send snapshot
            # -------------------------
            snapshot = world.snapshot()
            await websocket.send(json.dumps(snapshot))

    except websockets.exceptions.ConnectionClosed:
        logger.info("WebSocket connection closed")

    except Exception as e:
        logger.error("Error in WebSocket handler", exc_info=True)

# -------------------------
# Server loop
# -------------------------
async def main():
    logger.info("Starting WebSocket server on ws://localhost:8765")
    async with websockets.serve(handler, "localhost", 8765):
        logger.info("WebSocket server is running")
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())

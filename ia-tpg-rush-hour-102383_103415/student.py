import asyncio
import getpass
import json
import os
import traceback

import pygame
import websockets

from RushHourSolver import Solver


pygame.init()
program_icon = pygame.image.load("data/icon2.png")
pygame.display.set_icon(program_icon)

async def agent_loop(server_address="localhost:8080", agent_name="student"):
    """Example client loop."""
    async with websockets.connect(f"ws://{server_address}/player") as websocket:

        # Receive information about static game properties
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))
        nivel_ant = ""
        ia= Solver()
        while 1:
            try:
                state = json.loads(
                    await websocket.recv()
                )  # receive game update, this must be called timely or your game will get out of sync with the server
                if nivel_ant != state["level"]:
                    nivel_ant = state["level"]
                    ia.recalcula(state["grid"])

                key=ia.run(state["grid"], state["cursor"], state["selected"])
                #if key is None:
                #    continue
                await websocket.send(
                        json.dumps({"cmd": "key", "key": key})
                    )  # send key command to server - you must implement this send in the AI agent

            except websockets.exceptions.ConnectionClosedOK:
                print("Server has cleanly disconnected us")
                return
            except Exception as e:
                print(e, traceback.format_exc())




# DO NOT CHANGE THE LINES BELLOW
# You can change the default values using the command line, example:
# $ NAME='arrumador' python3 client.py
loop = asyncio.get_event_loop()
SERVER = os.environ.get("SERVER", "localhost")
PORT = os.environ.get("PORT", "8080")
NAME = os.environ.get("NAME", getpass.getuser())
loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME))
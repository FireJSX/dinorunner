# /// script
# dependencies = [
#  "pygame",
#  "pygame-gui",
#  "pygame-ce",
#  "pygame_gui",
#  "pytmx"
# ]
# ///
import asyncio
from dinorunner.game import main

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
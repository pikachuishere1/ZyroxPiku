import asyncio
import signal
from TEAMZYRO import app  # This is your Pyrogram Client

loop = asyncio.get_event_loop()

async def start_bot():
    await app.start()
    print("Bot started.")
    await asyncio.Event().wait()  # Keeps the bot running

def shutdown():
    print("Received shutdown signal. Stopping bot...")
    loop.create_task(app.stop())  # Ensure proper async stop

if __name__ == "__main__":
    # Handle shutdown signals for Heroku
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, shutdown)

    try:
        loop.run_until_complete(start_bot())
    except (KeyboardInterrupt, SystemExit):
        print("Bot manually interrupted. Exiting...")
    finally:
        loop.run_until_complete(app.stop())  # Final cleanup
        print("Bot stopped.")

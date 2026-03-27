from flask import Flask, request, jsonify
from flask_cors import CORS
import discord
import asyncio
import threading
import os

app = Flask(__name__)

# ✅ Enable CORS (important)
CORS(app)

TOKEN = os.environ.get("DISCORD_BOT_TOKEN")

EMMA_CHANNEL = 1486860629951385811
EXPLOSIVE_CHANNEL = 1486866774556278834

intents = discord.Intents.default()
client = discord.Client(intents=intents)

loop = asyncio.new_event_loop()

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    print("Bot ready 🚀")

def start_bot():
    asyncio.set_event_loop(loop)
    loop.run_until_complete(client.start(TOKEN))

# 🔥 Run bot in background
threading.Thread(target=start_bot, daemon=True).start()

@app.route("/")
def home():
    return "Bot is running ✅"

@app.route("/send", methods=["POST", "OPTIONS"])
def send_message():

    # ✅ Handle preflight (CORS)
    if request.method == "OPTIONS":
        return "", 200

    try:
        data = request.json

        name = data.get("name")
        email = data.get("email")
        message = data.get("message")
        type_ = data.get("type")

        if not name or not email or not message:
            return jsonify({"error": "Missing fields"}), 400

        if type_ == "emma":
            channel_id = EMMA_CHANNEL
            title = "👩 Hire Emma"
            color = 0x8b5cf6
        else:
            channel_id = EXPLOSIVE_CHANNEL
            title = "💣 Hire Explosive"
            color = 0xff0000

        # 🔥 Async send (non-blocking)
        async def send():
            try:
                channel = client.get_channel(channel_id)

                if channel is None:
                    channel = await client.fetch_channel(channel_id)

                embed = discord.Embed(title=title, color=color)
                embed.add_field(name="Name", value=name, inline=True)
                embed.add_field(name="Email", value=email, inline=True)
                embed.add_field(name="Message", value=message, inline=False)

                await channel.send(embed=embed)

            except Exception as e:
                print("DISCORD ERROR:", e)

        asyncio.run_coroutine_threadsafe(send(), loop)

        # ✅ ALWAYS respond instantly
        return jsonify({"success": True})

    except Exception as e:
        print("SERVER ERROR:", e)
        return jsonify({"error": "Server error"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    print(f"Running on port {port}")
    app.run(host="0.0.0.0", port=port)

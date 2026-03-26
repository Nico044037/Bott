from flask import Flask, request, jsonify
import discord
import asyncio
import threading
import os

app = Flask(__name__)

TOKEN = os.environ.get("DISCORD_BOT_TOKEN")

EMMA_CHANNEL = 1486860629951385811
EXPLOSIVE_CHANNEL = 1486866774556278834

intents = discord.Intents.default()
client = discord.Client(intents=intents)

loop = asyncio.new_event_loop()

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

def start_bot():
    asyncio.set_event_loop(loop)
    loop.run_until_complete(client.start(TOKEN))

threading.Thread(target=start_bot).start()

@app.route("/send", methods=["POST"])
def send_message():
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

    async def send():
        channel = client.get_channel(channel_id)
        if channel:
            embed = discord.Embed(title=title, color=color)
            embed.add_field(name="Name", value=name, inline=True)
            embed.add_field(name="Email", value=email, inline=True)
            embed.add_field(name="Message", value=message, inline=False)
            await channel.send(embed=embed)

    asyncio.run_coroutine_threadsafe(send(), loop)

    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)

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
    print("Bot is ready 🚀")

def start_bot():
    asyncio.set_event_loop(loop)
    loop.run_until_complete(client.start(TOKEN))

# start bot in background thread
threading.Thread(target=start_bot, daemon=True).start()

@app.route("/")
def home():
    return "Bot is running ✅"

@app.route("/send", methods=["POST", "OPTIONS"])
def send_message():

    # 🔥 HANDLE PREFLIGHT (THIS IS THE KEY)
    if request.method == "OPTIONS":
        response = app.make_response("")
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        return response

    data = request.json

    name = data.get("name")
    email = data.get("email")
    message = data.get("message")
    type_ = data.get("type")

    if not name or not email or not message:
        response = jsonify({"error": "Missing fields"})
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response, 400

    if type_ == "emma":
        channel_id = 1486860629951385811
        title = "👩 Hire Emma"
        color = 0x8b5cf6
    else:
        channel_id = 1486866774556278834
        title = "💣 Hire Explosive"
        color = 0xff0000

    async def send():
        channel = client.get_channel(channel_id)
        if channel is None:
            channel = await client.fetch_channel(channel_id)

        embed = discord.Embed(title=title, color=color)
        embed.add_field(name="Name", value=name, inline=True)
        embed.add_field(name="Email", value=email, inline=True)
        embed.add_field(name="Message", value=message, inline=False)

        await channel.send(embed=embed)

    asyncio.run_coroutine_threadsafe(send(), loop)

    response = jsonify({"success": True})
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

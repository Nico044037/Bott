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
        title = "💣 Hire AvoidMyExplosive"
        color = 0xff0000

    async def send():
        try:
            channel = client.get_channel(channel_id)

            # fallback if cache fails
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

    return jsonify({"success": True})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))  # 🔥 FIXED FOR RAILWAY
    print(f"Running on port {port}")
    app.run(host="0.0.0.0", port=port)

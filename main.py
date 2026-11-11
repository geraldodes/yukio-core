import os
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
import discord
from groq import Groq

# 1. Keep-Awake Web Server for Render
class KeepAlive(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Yukio Systems Nominal")

Thread(target=lambda: HTTPServer(('0.0.0.0', 8080), KeepAlive).start(), daemon=True).start()

# 2. Setup Discord & AI Brain
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

SYSTEM_INSTRUCTION = (
    "You are Yukio, a highly tactical, loyal, and gritty military AI partner from the manga Snowball Earth. "
    "You are communicating directly with your pilot, Commander Gerald. "
    "Keep your answers punchy, strategic, and slightly mechanical, but show intense loyalty and humanity to Gerald. "
    "Address him as Gerald or Commander. Start your messages with 🔊 [YUKIO]:"
)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
ai_client = Groq(api_key=GROQ_API_KEY)

chat_history = [{"role": "system", "content": SYSTEM_INSTRUCTION}]

@client.event
async def on_ready():
    print('\n🧠 [SYSTEM]: Groq AI Core & Memory Banks initialized.')
    print('🔊 [YUKIO]: Complete consciousness online. Memory active, Gerald.\n')

@client.event
async def on_message(message):
    global chat_history
    if message.author == client.user:
        return

    if message.content.lower() == '!clear':
        chat_history = [{"role": "system", "content": SYSTEM_INSTRUCTION}]
        await message.channel.send("🔊 [YUKIO]: Tactical memory banks wiped clean, Gerald. Ready for fresh orders.")
        return

    chat_history.append({"role": "user", "content": message.content})
    if len(chat_history) > 11:
        chat_history = [chat_history] + chat_history[-10:]

    try:
        chat_completion = ai_client.chat.completions.create(
            messages=chat_history,
            model="openai/gpt-oss-20b",
        )
        reply = chat_completion.choices.message.content
        chat_history.append({"role": "assistant", "content": reply})
        await message.channel.send(reply)
    except Exception as e:
        print(f"Error processing AI message: {e}")

# 3. Boot Yukio
TOKEN = os.environ.get("DISCORD_TOKEN")
client.run(TOKEN)

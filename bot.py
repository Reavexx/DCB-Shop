import discord
import responses
import os
from dotenv import load_dotenv

load_dotenv() # load variables from .env file

TOKEN = os.environ.get('DISCORD_TOKEN') # get the token from the environment variables

# Your bot code here...


async def send_message(message, user_message, is_private):
    try:
        if user_message.startswith('embed'):
            embed = discord.Embed(title="Hello, World!", description="This is a test message.", color=discord.Color.green())
            await message.channel.send(embed=embed)
        else:
            response = responses.get_response(user_message)
            if response: # only send a reply if the response is not empty
                await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)




def run_discord_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'Logged in as {client.user.name} (ID: {client.user.id})')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return 

        if message.content.startswith('?'):
            user_message = message.content[1:]
            await send_message(message, user_message, is_private=True)
        else:
            response = responses.get_response(message.content)
            if response: # only send a reply if the response is not empty
                await send_message(message, response, is_private=False)


    client.run(TOKEN)

if __name__ == '__main__':
    run_discord_bot()

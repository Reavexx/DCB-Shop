import discord
import responses
import os
from dotenv import load_dotenv
from discord.ext import tasks

load_dotenv() # load variables from .env file

TOKEN = "MTA5MzQ1MDU4NjcwNTM3MTE0Ng.GAuibP.hY-sEtaDUXjE24bErx5MlipJ5M5hYNHxkdEfAc" # get the token from the environment variables
STATS_CHANNEL_ID = int(os.environ.get('STATS_CHANNEL_ID'))


async def send_message(message, user_message, is_private):
    try:
        if user_message.startswith('embed'):
            # Parse the user's input to extract the title and description
            parts = user_message.split('|')
            title = parts[0][6:].strip()
            description = parts[1][12:].strip()

            # Create the embed with the title, description, and a green color
            embed = discord.Embed(title=title, description=description, color=discord.Color.blue())

            # Set the image to the file path of your logo
            file = discord.File("C:/Users/dines/Downloads/DCB-shop/shop/Bild_2023-04-27_104345754-removebg-preview.png", filename="image.png")
            embed.set_thumbnail(url="attachment://image.png")

            # Add a footer to the embed
            embed.set_footer(text="Made by Reavex")

            # Send the embed message
            sent_message = await message.channel.send(embed=embed, file=file)

            # Delete the original command message and the sent embed message after 10 seconds
            await asyncio.sleep(10)
            await message.delete()
            await sent_message.delete()

        else:
            response = responses.get_response(user_message)
            if response: # only send a reply if the response is not empty
                await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)






async def on_offend(msg, client):

    block_words = ["black", "Black", "http://", "https://"]
    # If the message wasn't sent by the bot
    if msg.author != client.user:

        # Going through each blocked word to check if it's in the message
        for text in block_words:
            # Checking if the message was sent by a moderator (because it would be nice if moderators
            # could share links in case it would be important for them to do so).
            if "Moderator" not in str(msg.author.roles) and "admin" not in [role.name.lower() for role in msg.author.roles] and text in str(msg.content.lower()):
                await msg.delete() # Deletes the message
                return # So that we don't continue going throuh the loop once we've already found
                       # a blocked word


# Bot Setup
def run_discord_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    activity = discord.Activity(
    type=discord.ActivityType.playing,
    name="Supporting DCB-Shop"
)
    
    client.activity = activity

    @client.event
    async def on_ready():
        print(f'Logged in as {client.user.name} (ID: {client.user.id})')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return 

        await on_offend(message, client) # call on_offend function here

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

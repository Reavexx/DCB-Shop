import discord
import responses
import os
from dotenv import load_dotenv

load_dotenv() # load variables from .env file

TOKEN = os.environ.get('DISCORD_TOKEN') # get the token from the environment variables


# Embed Message
async def send_message(message, user_message, is_private):
    try:
        if user_message.startswith('embed'):
            embed = discord.Embed(title="Guten Tag!", description="This is a test message.", color=discord.Color.green())
            await message.channel.send(embed=embed)
        else:
            response = responses.get_response(user_message)
            if response: # only send a reply if the response is not empty
                await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)

    

async def on_offend(msg, client):

    block_words = ["white", "black", "http://", "https://"]
    # If the message wasn't sent by the bot
    if msg.author != client.user:

        # Going through each blocked word to check if it's in the message
        for text in block_words:
            # Checking if the message was sent by a moderator (because it would be nice if moderators
            # could share links in case it would be important for them to do so).
            if "Moderator" not in str(msg.author.roles) and text in str(msg.content.lower()):
                await msg.delete() # Deletes the message
                return # So that we don't continue going throuh the loop once we've already found
                       # a blocked word

        print("Not Deleting...") # This will be printed if the bot doesn't delete a message

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

import discord
import responses
import os


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
    TOKEN = 'MTA5MzQ1MDU4NjcwNTM3MTE0Ng.GnOkjo.6Cpw9lbjWA7W4EzyIeMlH5etDJwW8ThZOuBJHk'
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

        if message.content.startswith('?'): # check if the message starts with a question mark
            user_message = message.content[1:] # remove the question mark from the message
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, message.content, is_private=False)

    client.run(TOKEN)

if __name__ == '__main__':
    run_discord_bot()

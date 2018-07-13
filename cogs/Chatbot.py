import datetime, time, json, apiai, random, discord, asyncio, os
from time import ctime
from discord.ext import commands

with open("databases/dialogflowtoken.txt") as f:
    chatbottoken = f.read()

CLIENT_ACCESS_TOKEN = chatbottoken
ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

class Chatbot():
    """Commands for the Spectrum Chatbot"""

    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        if not message.author.bot and self.bot.user in message.mentions:
            try:
                if message.content.startswith(("$", "!", "?", "-", "*", "`", "~", "+", "/", ";", "=", "&", ">")): # a bunch of generic checks to see if the bot is not supposed to reply
                    pass
                else:
                    async with message.channel.typing(): 
                        user_message = message.content.replace(message.guild.me.mention,'') if message.guild else message.content

                        request = ai.text_request()
                        request.query = user_message

                        response = json.loads(request.getresponse().read())

                        result = response['result']
                        action = result.get('action')

                    if action == "user.requests.help":
                        await message.author.send("**https://spectrix.pythonanywhere.com/spectrum**\n*Here's my help page!*")
                        await message.channel.send(f"** {message.author.mention} I sent you help in your DMs :mailbox_with_mail:**")
                    elif action == "name.user.get":
                        await message.channel.send(f"{message.author.mention} Your name is {message.author.name}.")
                    elif action == "bot.time":
                        await message.channel.send(f"{message.author.mention} The time for me is currently {ctime()}")
                    elif action == "prefix.get":
                        await message.channel.send(f"{message.author.mention} My default prefix is `$`")

                    else:
                        await message.channel.send(f"{message.author.mention} {response['result']['fulfillment']['speech']}")

                    print(f"Chatted with a user. Server: {message.guild.name}. Time: {datetime.datetime.now().time()}")

            except KeyError:
                await message.channel.send("```Error: 'KeyError', make sure you gave not too little input and not too much ;)```")

    @commands.command(pass_context=True)
    async def devChat(self, ctx, *, chatMsg):
        if ctx.message.author.id == 276707898091110400:
            request = ai.text_request()
            request.query = chatMsg
            response = json.loads(request.getresponse().read())

            result = response['result']
            timestamp = response['timestamp']

            action = result.get('action')
            resolvedQuery = result.get('resolvedQuery')
            intentName = result.get('intentName')
            score = result.get('score')
            fulfillment = result.get('fulfillment')
            speech = fulfillment.get('speech')

            actionIncomplete = result.get('actionIncomplete', False)

            emb = (discord.Embed(colour=0x3be801))
            emb.set_author(name="DevChat for SpectrumV2 Chatbot", icon_url="https://images.discordapp.net/avatars/320590882187247617/138033611e0989895474ac1e8f61cbb8.png?size=512")
            emb.add_field(name="resolvedQuery", value=f"```{resolvedQuery}```", inline=False)
            emb.add_field(name="intentName", value=f"`{intentName}`")
            emb.add_field(name="score", value=f"`{score}`")
            if action == "":
                emb.add_field(name="action", value="`None assigned`")
            else:
                emb.add_field(name="action", value=f"`{action}`")
            if speech == "":
                emb.add_field(name="speech", value='```Somehow nothing. Spectrix, please fix.```', inline=False)
            else:
                emb.add_field(name="speech", value=f'```{speech}```', inline=False)
            emb.set_footer(text=f"Timestamp: {timestamp}")
            await ctx.send(embed=emb)

        else:
            await ctx.send("Sorry, this command is for my devs only. Please just mention me if you'd like to chat!")

def setup(bot):
    bot.add_cog(Chatbot(bot))
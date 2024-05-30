import os
import discord
from discord.ext import commands
from helpers.pagination import send_paginated_message
from helpers.ai import get_response

class Ask(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.chat_logger = bot.chat_logger
        self.conversation_histories = bot.conversation_histories
    
    @commands.command(name="ask")
    async def ask(self, ctx) -> None:
        prompt = ctx.message.content
        username = ctx.author.name
        user_id = ctx.author.id
        self.conversation_histories[user_id].append({"role": "user", "content": prompt})
        async with ctx.channel.typing():
            response = get_response(self.conversation_histories[user_id])
            self.chat_logger.info(f"{username}: {prompt}\nVexel: {response}\n")
            if response:
                self.conversation_histories[user_id].append({"role": "assistant", "content": response})
                if len(response) >= 2000:
                    await send_paginated_message(ctx.channel, response)
                else:
                    await ctx.reply(response)
            else:
                await ctx.reply("Sorry, I couldn't answer you right now. You can use !draw cmnd for now! Thanku.")

    @commands.command(name="reset")
    async def reset(self, ctx) -> None:
        user_id = ctx.author.id
        self.conversation_histories[user_id] = []
        await ctx.reply("Your chat history has been reset.")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Ask(bot))
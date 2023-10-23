import asyncio
import time
from twitchio.ext import commands
from config import access_token, the_initial_channels
from commands import roll_dice, can_you_dig_it


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(token=access_token, prefix='!', initial_channels=the_initial_channels)

    async def event_command_error(self, context: commands.Context, error: Exception):
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.ArgumentParsingFailed):
            await context.send(error.message)
        else:
            print(error)

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    @commands.command(aliases=['dig_it'])
    async def dig(self, ctx: commands.Context):
        if ctx.author.name in ['lvl4sword'] and ctx.author.id in ['451750625']:
            message_content = ctx.message.content.split()
            if len(message_content) == 2:
                the_site = message_content[1]
                the_ips = can_you_dig_it(the_site)
                await ctx.send(f'{the_site} ipv4/ipv6: {the_ips}')
            else:
                await ctx.send(f"This command requires the invocation and a website.")

    @commands.command()
    async def roll(self, ctx: commands.Context):
        if ctx.author.name in ['lvl4sword'] and ctx.author.id in ['451750625']:
            choices = ['2', '4', '6', '8', '10', '12', '20', '50', '100', '1000']
            message_content = ctx.message.content.split()
            if len(message_content) == 2:
                try:
                    how_many_sides = message_content[1]
                    if how_many_sides not in choices:
                        raise ValueError
                except ValueError:
                    await ctx.send(f"The choices are as follows: {', '.join(choices)}")
                else:
                    what_rolled = roll_dice(int(how_many_sides))
                    if how_many_sides == '2':
                        if what_rolled == 1:
                            await ctx.send(f'I flipped a coin and got heads')
                        else:
                            await ctx.send(f'I flipped a coin and got tails')
                    else:
                        await ctx.send(f'I rolled a {what_rolled}')
            else:
                await ctx.send(f"This command requires the invocation and one of the following: {', '.join(choices)}")

    @commands.command(aliases=['cd'])
    async def countdown(self, ctx: commands.Context):
        if ctx.author.name in ['lvl4sword'] and ctx.author.id in ['451750625']:
            message_content = ctx.message.content.split()
            if len(message_content) == 2:
                try:
                    the_seconds = int(message_content[1])
                except ValueError:
                    await ctx.send(f"This command requires the invocation and 60 >= number >= 10")
                else:
                    if 60 >= the_seconds >= 10:
                        start_time = int(time.time())
                        ending_time = start_time + the_seconds
                        total_time = ending_time - start_time
                        if total_time != 10:
                            await ctx.send(f"Countdown will end in {total_time} seconds")
                            await asyncio.sleep(1)
                        for x in range(1000):
                            if int(time.time()) == (ending_time - 10):
                                await ctx.send(f"Countdown will end in 10 seconds")
                            elif int(time.time()) == (ending_time - 5):
                                await ctx.send(f"Countdown will end in 5 seconds")
                            elif int(time.time()) == (ending_time - 4):
                                await ctx.send(f"Countdown will end in 4 seconds")
                            elif int(time.time()) == (ending_time - 3):
                                await ctx.send(f"Countdown will end in 3 seconds")
                            elif int(time.time()) == (ending_time - 2):
                                await ctx.send(f"Countdown will end in 2 seconds")
                            elif int(time.time()) == (ending_time - 1):
                                await ctx.send(f"Countdown will end in 1 second")
                            elif int(time.time()) == (ending_time - 0):
                                await ctx.send(f"Countdown has ended!")
                                break
                            await asyncio.sleep(1)
                    else:
                        await ctx.send(f"This command requires the invocation and 60 >= number >= 10")
            else:
                await ctx.send(f"This command requires the invocation and 60 >= number >= 10")


bot = Bot()
bot.run()

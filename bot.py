import os
import re

import discord
from dotenv import load_dotenv
from discord.ext import commands

import tesseract
import cv2
import database
import embeds
import quickchart_army
import bot_strings as bs

load_dotenv()

db = database.DB()


class ArmyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='/')

    async def on_ready(self):
        print(f'The bot {self.user.display_name} is ready.')

    async def initialize_embed(self):
        embed = discord.Embed(
            color=discord.Colour.purple(),
        )

        return embed

    async def initialize_help_embed(self):
        embed = discord.Embed(
            color=discord.Colour.purple(),
            title='Army Bot Commands',
            description=bs.bot_strings['help_bot_description']
        )

        return embed

    async def initialize_manual_embed(self):
        embed = discord.Embed(
            color=discord.Colour.purple(),
            title='Manual Input',
            description=bs.bot_strings['manual_bot_description']
        )

        return embed

    async def initialize_leaderboard_embed(self):
        embed = discord.Embed(
            color=discord.Colour.purple(),
            title='Housse Hessian Hall Of Fame',
        )

        return embed

    async def initialize_ocr_embed(self):
        embed = discord.Embed(
            color=discord.Colour.purple(),
            title='OCR Input',
            description=bs.bot_strings['ocr_bot_description']
        )

        return embed

    async def initialize_quickchart_embed(self, player: str):
        embed = discord.Embed(
            title=f'{player}\'s Stats',
            color=discord.Colour.purple(),
        )

        return embed

    async def fill_datas(self, message: discord.Message, author: str, commander_name: str, max_troop_size: int,
                         sorted_datas: list, sum_of_troops: int):
        db.prepare_datas_for_database(author, commander_name, max_troop_size)

        try:
            db.fill_troops(sorted_datas, author)
        except TypeError:
            await message.channel.send(
                bs.bot_strings['ocr_error'])
            return

        embed = await self.initialize_embed()
        embeds.construct_main_embed(self, embed, message.author, message.author.avatar_url, commander_name,
                                    str(max_troop_size), str(sum_of_troops + 1), sorted_datas)

        await message.channel.send(embed=embed)

    async def on_message(self, message):
        if message.attachments:
            if message.attachments[0].content_type.startswith('image'):
                if message.content.isdigit() and 96 > int(message.content) > 4:
                    try:
                        datas = [data.rstrip(',.') for data in tesseract.scan_image(message.attachments[0].url)]
                    except cv2.error:
                        await message.channel.send('Image is invalid. Please, retry')
                        return
                    try:
                        commander_name = [data.rsplit(' ', 1)[0] for data in datas if data.endswith('%')][0]
                    except IndexError:
                        await message.channel.send('Image is invalid. Please, retry')
                        return
                    try:
                        total_troops_scanned = sum(
                            [int(re.search('[0-9]{1,2}', data).group(0)) for data in datas if not data.endswith('%')])
                    except AttributeError:
                        await message.channel.send('Image is invalid. Please, retry')
                        return
                    sorted_datas = [data.rsplit(' ', 1) for data in datas if not data.endswith('%')]

                    if total_troops_scanned < int(message.content):
                        await self.fill_datas(message, str(message.author), commander_name, message.content,
                                              sorted_datas, total_troops_scanned)
                    else:
                        await message.channel.send(
                            bs.construct_troop_size_error(total_troops_scanned))

                else:
                    await message.channel.send(bs.bot_strings['wrong_troop_size'])

            else:
                await message.channel.send('You have to upload an image.')
        elif message.content.startswith('/'):
            await self.process_commands(message)
        elif re.fullmatch(r'[A-Za-z]+\([0-9]{1,2}\): ?(([A-Za-z]+ )+[A-Za-z]+\/[0-9]{1,2},? ?)+', message.content):
            commander_infos, commander_name = message.content.split(':')[0], message.content.split('(')[0]
            max_army_size = int(commander_infos.split('(')[1].rstrip(')'))
            sorted_datas = [data.strip(' ').split('/') for data in message.content.split(':')[1].split(',')]
            troop_nb_scanned = sum([int(data[1]) for data in sorted_datas])
            if 96 > max_army_size > 4 and max_army_size > troop_nb_scanned:
                await self.fill_datas(message, str(message.author), commander_name, max_army_size, sorted_datas,
                                      troop_nb_scanned)
            else:
                await message.channel.send(bs.bot_strings['troop_check'])


class ArmyBodCmd(commands.Cog):
    def __init__(self, _bot):
        self.bot = _bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(bs.bot_strings['unknown_command'])

    @commands.command(name='commands', help='Gives you the available commands, and their purpose.')
    async def display_help_embed(self, ctx):
        embed = await self.bot.initialize_help_embed()
        embed.set_thumbnail(url='https://tinyurl.com/38wauca2')

        await ctx.send(embed=embed)

    @commands.command(name='manual', help='Explain how to use the manual input system.')
    async def display_manual_embed(self, ctx):
        embed = await self.bot.initialize_manual_embed()
        embed.set_thumbnail(url='https://tinyurl.com/38wauca2'),
        embed.set_footer(
            text=bs.bot_strings['manual_command_example'])

        await ctx.send(embed=embed)

    @commands.command(name='ocr', help='Explain how to upload an image to register your army.')
    async def display_ocr_embed(self, ctx):
        embed = await self.bot.initialize_ocr_embed()
        embed.set_thumbnail(url='https://tinyurl.com/yettvk3w')

        await ctx.send(embed=embed)

    @commands.command(name='leaderboard', help='Display the Top 20 players in the clan.')
    async def display_leaderboard_embed(self, ctx):
        initialized_embed = await self.bot.initialize_leaderboard_embed()
        datas = db.leaderboard()
        embed = embeds.construct_leaderboard_embed(self, initialized_embed, datas)

        await ctx.send(embed=embed)

    @commands.command(name='stats', help='Allow you to see stats from a player.')
    async def display_quickchart(self, ctx, *arg):
        player = ' '.join(arg)
        datas = db.get_player_stats(player)
        if datas:
            url = quickchart_army.get_quickchart([int(data[1]) for data in datas], [data[0] for data in datas])
            initialized_embed, max_troop_size = await self.bot.initialize_quickchart_embed(player), datas[0][-1]
            percentage_6_tier = round((sum([data[1] for data in datas if data[2] == 6]) * 100) / datas[0][-1] - 1, 1)
            percentage_5_tier = round((sum([data[1] for data in datas if data[2] == 5]) * 100) / datas[0][-1] - 1, 1)
            embed = embeds.construct_quickchart_embed(self, initialized_embed, url, max_troop_size, percentage_6_tier,
                                                      percentage_5_tier)

            await ctx.send(embed=embed)

        else:
            if not arg:
                await ctx.send('/stats PlayerName will allow you to see statistics about a player.')
            else:
                await ctx.send('This Player doesn\'t exist in the database.')


army_bot = ArmyBot()
army_bot.add_cog(ArmyBodCmd(_bot=army_bot))
army_bot.run(os.getenv('TOKEN'))

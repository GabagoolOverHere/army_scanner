import os
import re

import discord
from dotenv import load_dotenv
from discord.ext import commands

import tesseract
import cv2
import database
import embeds

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

    async def initialize_manual_embed(self):
        embed = discord.Embed(
            color=discord.Colour.purple(),
            title='Manual Input',
            description='To manually register your army, follow the following pattern in a SINGLE MESSAGE:\n\n'
                        'Your Commander Name(Your Max Army Size): Troop Name/Number, '
                        'Troop Name/Number, '
                        '...\n\n'
                        'And press Enter.'
        )
        return embed

    async def fill_datas(self, message: discord.Message, author: str, commander_name: str, max_troop_size: int, sorted_datas: list, sum_of_troops: int):
        db.prepare_datas_for_database(author, commander_name,
                                      max_troop_size)
        try:
            db.fill_troops(sorted_datas, author)
        except TypeError:
            await message.channel.send(
                'Oops, looks like I can\'t read all the units properly. Please, try again with another image if you used the scan system, or check for typos in your message if you used manual input.')
            return
        embed = await self.initialize_embed()
        embeds.construct_embed(self,
                               embed,
                               message.author,
                               message.author.avatar_url,
                               commander_name,
                               str(max_troop_size),
                               str(sum_of_troops + 1),
                               sorted_datas)
        await message.channel.send(embed=embed)
        return

    async def on_message(self, message):
        if message.attachments:
            if message.attachments[0].content_type.startswith('image'):
                if message.content.isdigit() and 96 > int(message.content) > 4:
                    try:
                        datas = [data.rstrip(',.') for data in tesseract.scan_image(message.attachments[0].url)]
                    except cv2.error:
                        await message.channel.send('Image is invalid. Please, retry')
                        return
                    commander_name = [data.rsplit(' ', 1)[0] for data in datas if data.endswith('%')][0]
                    total_troops_scanned = sum([int(re.search('[0-9]{1,2}', data).group(0)) for data in datas if
                                     not data.endswith('%')])
                    sorted_datas = [data.rsplit(' ', 1) for data in datas if
                                    not data.endswith('%')]

                    if total_troops_scanned < int(message.content):
                        await self.fill_datas(message, str(message.author), commander_name, message.content, sorted_datas, total_troops_scanned)
                    else:
                        await message.channel.send(
                            f'The number you gave is inferior to the sum of all the troops I scanned ({total_troops_scanned}). Please, retry.')
                        return

                else:
                    await message.channel.send(
                        'Attach a valid max troop size with your image (number between 5 and 95). Please retry.')
                    return

            else:
                await message.channel.send('You have to upload an image.')
                return
        else:
            await self.process_commands(message)
            if not message.content.startswith('/'):
                commander_infos = message.content.split(':')[0]
                commander_name = message.content.split('(')[0]
                max_army_size = int(commander_infos.split('(')[1].rstrip(')'))
                sorted_datas = [data.strip(' ').split('/') for data in message.content.split(':')[1].split(',')]
                troop_nb_scanned = sum([int(data[1]) for data in sorted_datas])
                if 96 > max_army_size > 4 and max_army_size > troop_nb_scanned:
                    await self.fill_datas(message, str(message.author), commander_name, max_army_size, sorted_datas, troop_nb_scanned)
                else:
                    await message.channel.send('Check if your max army size is between 5 and 95 and the number of each troop you typed is correct.')


class ArmyBodCmd(commands.Cog):
    def __init__(self, _bot):
        self.bot = _bot

    @commands.command(name='manual')
    async def display_embed(self, ctx):
        embed = await self.bot.initialize_manual_embed()
        embed.set_thumbnail(url='https://tinyurl.com/38wauca2'),
        embed.set_footer(
            text='Here is an example:\n"Gabagool(91): Imperial Palatine Guard/14, Vlandian Sharpshooter/49, Imperial Legionary/19"')
        await ctx.send(embed=embed)


army_bot = ArmyBot()
army_bot.add_cog(ArmyBodCmd(_bot=army_bot))
army_bot.run(os.getenv('TOKEN'))

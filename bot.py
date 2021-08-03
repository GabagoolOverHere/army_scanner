import os
import re

import discord
from discord.ext import commands
from dotenv import load_dotenv

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

    async def on_message(self, message):
        if message.attachments:
            if message.attachments[0].content_type.startswith('image'):
                if message.content.isdigit() and 96 > int(message.content) > 4:
                    try:
                        datas = [data.rstrip(',.') for data in tesseract.scan_image(message.attachments[0].url)]
                    except cv2.error:
                        await message.channel.send('Image is invalid. Please, retry')
                        return
                    commander_name = [data.rsplit(' ', 1)[0] for data in datas if data.endswith('%')]
                    troop_numbers = [int(re.search('[0-9]{1,2}', data).group(0)) for data in datas if
                                     not data.endswith('%')]
                    sorted_datas = [data.rsplit(' ', 1) for data in datas if
                                    not data.endswith('%')]

                    if sum(troop_numbers) < int(message.content):

                        if db.find_player_by_name(str(message.author)) is None:
                            db.create_player(str(message.author), commander_name[0], int(message.content))
                        else:
                            player_id = db.find_player_by_name(str(message.author))
                            db.update_player(commander_name[0], int(message.content),
                                             player_id[0])
                            db.delete_troops(player_id[0])
                        try:
                            db.fill_troops(sorted_datas, str(message.author))
                        except TypeError:
                            await message.channel.send(
                                'Oops, looks like I can\'t read all the units properly. Please, try again with another image')
                            return
                        embed = await self.initialize_embed()
                        embeds.construct_embed(self,
                                               embed,
                                               message.author,
                                               message.author.avatar_url,
                                               commander_name[0],
                                               message.content,
                                               str(sum(troop_numbers) + 1),
                                               sorted_datas)
                        await message.channel.send(embed=embed)
                    else:
                        await message.channel.send(
                            f'The number you gave is inferior to the sum of all the troops I scanned ({sum(troop_numbers)}). Please, retry.')
                        return

                else:
                    await message.channel.send(
                        'Attach a valid max troop size with your image (number between 5 and 95). Please retry.')
                    return

            else:
                await message.channel.send('You have to upload an image.')
                return

        elif not message.author.bot:
            await message.delete()


army_bot = ArmyBot()
army_bot.run(os.getenv('TOKEN'))

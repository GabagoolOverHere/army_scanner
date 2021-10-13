import discord


def construct_main_embed(self, embed: discord.Embed, author: str, icon: str, commander_name: str, max_troop_size: str, troops_scanned: str, troops: list, thumbnail_url='https://tinyurl.com/38wauca2',
                         footer='React with \U0001F197 (:ok:) if the scan seems to be correct.\n'
                                'React with \U0000274C (:x:) if the scan seems to be incorrect.\n'
                                'Click on your discord name in the message to access the clan\'s stats'):

    embed.set_author(name=author, url='https://house-hessian.de/', icon_url=icon)
    embed.add_field(name='Commander Name:', value=commander_name)
    embed.add_field(name='Max Troop Size:', value=max_troop_size)
    embed.add_field(name='Total Troops Scanned:', value=troops_scanned)
    embed.set_thumbnail(
        url=thumbnail_url)
    for data in troops:
        embed.add_field(name=data[0], value=data[1], inline=True)
    embed.set_footer(
        text=footer)


def construct_leaderboard_embed(self, embed: discord.Embed, datas: list):

    final_datas = ''
    for i, data in enumerate(datas, start=1):
        if i == 1:
            final_datas += f'\U0001F947 {data[0]}: {int(data[1])} points\n'
        elif i == 2:
            final_datas += f'\U0001F948 {data[0]}: {int(data[1])} points\n'
        elif i == 3:
            final_datas += f'\U0001F949 {data[0]}: {int(data[1])} points\n-----------------------\n'
        elif i > 3:
            final_datas += f'#{i} {data[0]}: {int(data[1])} points\n'
    embed.add_field(name='Top 20\n-----------------------', value=final_datas)
    embed.set_thumbnail(url='https://tinyurl.com/38wauca2')
    embed.set_footer(
        text='Points attribution is based on troops tier, quantity, and current PvP meta.')

    return embed


def construct_quickchart_embed(self, embed: discord.Embed, quickchart_url: str, max_troop_size: str, percentage_6_tier: float, percentage_5_tier: float):

    embed.set_image(url=quickchart_url)
    embed.set_thumbnail(url='https://tinyurl.com/38wauca2')
    embed.add_field(name='Max Army Size', value=max_troop_size)
    embed.add_field(name='6 Tier troops', value=f'{percentage_6_tier if percentage_6_tier >= 1 else percentage_6_tier + 1} %')
    embed.add_field(name='5 Tier troops', value=f'{percentage_5_tier if percentage_5_tier >= 1 else percentage_5_tier + 1} %')

    return embed
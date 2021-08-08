import discord


def construct_embed(self, embed: discord.Embed, author: str, icon: str, commander_name: str, max_troop_size: str,
                    troops_scanned: str, troops: list,
                    thumbnail_url='https://tinyurl.com/38wauca2',
                    footer='React with \U0001F197 (:ok:) if the scan seems to be correct.\n'
                           'React with \U0000274C (:x:) if the scan seems to be incorrect.\n'
                           'Click on your discord name in the message to access the clan\'s stats'):
    embed.set_author(name=author, url='https://gabagool.fr', icon_url=icon)
    embed.add_field(name='Commander Name:', value=commander_name)
    embed.add_field(name='Max Troop Size:', value=max_troop_size)
    embed.add_field(name='Total Troops Scanned:', value=troops_scanned)
    embed.set_thumbnail(
        url=thumbnail_url)
    for data in troops:
        embed.add_field(name=data[0] + ':', value=data[1], inline=True)
    embed.set_footer(
        text=footer)

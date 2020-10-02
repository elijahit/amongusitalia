from discord.ext import commands
from discord import Embed, Message
from discord import Color


class Embeds(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def get_standard_embed(name, color, icon, fields, footer):
        embed = Embed(color=color)
        embed.set_author(name=name, icon_url=icon)

        for field in fields:
            embed.add_field(name=field[0], value=field[1])
        embed.set_footer(text=footer)

        return embed


    @staticmethod
    def get_error_message(description=None, color=Color(0xf72525)):
        embed = Embed(description=description, color=color)
        return embed

    @staticmethod
    def get_info_message(description=None, color=Color(0x2d91e3)):
        embed = Embed(description=description, color=color)
        return embed

    @staticmethod
    def get_warning_message(description=None, color=Color(0xe3a02d)):
        embed = Embed(description=description, color=color)
        return embed

    @staticmethod
    def get_success_message(description=None, color=Color(0x14f55f), title=None):
        embed = Embed(description=description, color=color, title=title)
        return embed


def setup(bot):
    bot.add_cog(Embeds(bot))
    print("[!] modulo embeds caricato")

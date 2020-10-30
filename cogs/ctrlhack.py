import datetime as dt

import discord
from discord.ext import commands


class Ctrlhack(commands.Cog):

    def __init__(self, bot):
        # 762080734537056266 TRUE
        # 758790855321845764 TEST
        self.bot = bot
        self.ctr_category = 762080734537056266

    @commands.command()
    async def hackhelp(self, ctx):
        cfg = self.bot.get_cog('Config')
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = cfg.rolea_top8

        if len(user_roles.intersection(admin_roles)) != 0:
            await ctx.message.delete()
            cmd_ls = discord.Embed(title="LISTA COMANDI", description="**Comandi admin** \n\
            !hack (numero stanza matchmaking) **[Convoca una stanza matchmaking per il controllo hack]**\n\
                \n\
                **Per risolvere i bug** \n\
                !FAIL **[elimina TUTTE le chat vocali dalla categoria 'controllo hack']**\n\
                    !RESETLIST **[resetta la lista degli helper con un controllo hack in corso]**")
            cmd_ls.set_author(name="Among Us Ita")
            cmd_ls.set_footer(text=cfg.footer)

            await ctx.channel.send(embed=cmd_ls, delete_after=120)

    @commands.command()
    async def hack(self, ctx, num):
        cfg = self.bot.get_cog('Config')
        db = self.bot.get_cog('Db')
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = cfg.rolea_top8

        if len(user_roles.intersection(admin_roles)) == 0:
            await ctx.message.delete()

            user_send = ctx.message.author
            check = db.fetchall('SELECT * FROM ctrlhack WHERE admin_id = ?', (user_send.id,))

            if len(check) == 0:

                warning = discord.Embed(title="🟥 E' STATO CONVOCATO UN CONTROLLO HACK 🟥",
                                        description=f"{user_send.mention} ha convocato il gruppo: matchmaking {num} per un controllo hack, proseguire?",
                                        color=discord.Color.red(), timestamp=dt.datetime.utcnow())
                warning.set_footer(text=cfg.footer)
                warning.set_author(name="Among Us Ita")

                message_sent = await ctx.channel.send(embed=warning)
                await message_sent.add_reaction("🟢")
                await message_sent.add_reaction("🔴")

                db.execute("INSERT INTO ctrlhack (admin_id, message_id, matchmaking_num) VALUES (?, ?, ?)",
                           (user_send.id, message_sent.id, int(num),))
                await db.commit()
            else:
                warning = discord.Embed(title="🟪 UN ADMIN PUO' AVERE UN MASSIMO DI UN CONTROLLO APERTO 🟪",
                                        description=f"{user_send.mention}, \nchiudi prima tutti i tuoi controlli  poi "
                                                    f"riprova",
                                        color=discord.Color.purple(), timestamp=dt.datetime.utcnow())
                warning.set_footer(text=cfg.footer)
                warning.set_author(name="Among Us Ita")
                await ctx.channel.send(embed=warning, delete_after=5)

    @hack.error
    async def hack_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.message.delete()
            await ctx.send("[!] USA: !hack (numero matchmaking)")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        cfg = self.bot.get_cog("Config")
        db = self.bot.get_cog("Db")
        user_id = payload.user_id
        channel_id = payload.channel_id
        message_id = payload.message_id
        emoji = payload.emoji
        emoji_name = payload.emoji.name
        guild_id = payload.guild_id
        member = payload.member
        # user_roles = [i.id for i in member.roles]

        if member.bot is False:
            check_list = db.fetchall("SELECT * FROM ctrlhack WHERE admin_id = ? AND message_id = ?", (member.id, message_id,))
            channel = self.bot.get_channel(channel_id)
            message = await channel.fetch_message(message_id)
            guild = self.bot.get_guild(guild_id)
            if len(check_list) > 0:
                check = check_list[0]
            else:
                await message.remove_reaction(emoji, member)
                return 0

            if emoji_name == "🟢" and user_id == check[1]:
                num = check[3]

                await message.clear_reaction("🔴")

                guild_now = message.channel.guild
                channel_got = discord.utils.get(guild_now.voice_channels, name=f"matchmaking {num}")

                category = discord.utils.get(guild_now.categories, name="controllo hack")
                category_channels = category.voice_channels

                try:
                    user_send = self.bot.get_user(check[1])

                    warning = discord.Embed(title="🟡 IL TUO CONTROLLO STA PER INIZIARE 🟡",
                                            description=f"{user_send.mention}: torna qui una volta finito per "
                                                        f"chiudere il controllo \n \n*Aspetta che vengano create le "
                                                        f"tue stanze!* \n \n \n**Hai 10 secondi...** \n \n*Durante "
                                                        f"questa operazione non sarà possibile reagire ad altri "
                                                        f"controlli hack*",
                                            color=discord.Color.orange(), timestamp=dt.datetime.utcnow())
                    warning.set_footer(text=cfg.footer)
                    warning.set_author(name="HackBot")
                    await message.edit(embed=warning)

                    i = 1

                    for channel in category_channels:
                        if channel.name.startswith(f"Vocale {i} generale"):
                            i += 1

                    db.execute("UPDATE ctrlhack SET ctrl_num = ? WHERE admin_id = ?", (i, check[1],))
                    await db.commit()

                    await category.create_voice_channel(f"Vocale {i} generale 🥵")
                    await category.create_voice_channel(f"┠ Vocale {i}-1 🥶")
                    await category.create_voice_channel(f"┠ Vocale {i}-2 🥶")
                    await category.create_voice_channel(f"┗ Vocale {i}-3 🥶")

                    hackchannels = [
                        discord.utils.get(guild_now.voice_channels, name=f"Vocale {i} generale 🥵"),
                        discord.utils.get(guild_now.voice_channels, name=f"┠ Vocale {i}-1 🥶"),
                        discord.utils.get(guild_now.voice_channels, name=f"┠ Vocale {i}-2 🥶"),
                        discord.utils.get(guild_now.voice_channels, name=f"┗ Vocale {i}-3 🥶")
                    ]

                    warning = discord.Embed(title="🟨 IL TUO CONTROLLO STA PER INIZIARE 🟨",
                                            description=f"{user_send.mention}: torna qui una volta finito per "
                                                        f"chiudere il controllo \n \n*Entra nella chat vocale (Voca"
                                                        f"le generale {i} 🥵)!* \n \n**Hai 10 secondi...** \n "
                                                        f"\n*Durante questa operazione non sarà possibile reagire ad "
                                                        f"altri controlli hack*",
                                            color=discord.Color.orange(), timestamp=dt.datetime.utcnow())
                    warning.set_footer(text=cfg.footer)
                    warning.set_author(name="HackBot")
                    await message.edit(embed=warning)

                    try:
                        for g in db.fetchall('SELECT * FROM analytics WHERE admin_id = ?', (user_id,)):
                            if g[4] is None:
                                db.execute("UPDATE analytics SET hack = 1 WHERE admin_id = ?", (user_id,))
                            else:
                                db.execute("UPDATE analytics SET hack = hack+1 WHERE admin_id = ?", (user_id,))
                    except Exception as e:
                        print(f"Error: {e}")

                    try:
                        d = db.fetchall('SELECT * FROM analytics WHERE admin_id = ?', (user_id,))
                        if len(d) == 0:
                            db.execute("INSERT INTO analytics (admin_id, hack) VALUES (?, ?)", (user_id, 1,))
                    except Exception as e:
                        print(f"Error2: {e}")

                    await db.commit()

                    for user_in in channel_got.members:
                        await user_in.move_to(hackchannels[0])
                        member_id = user_in.id
                        member_nick = user_in.nick
                        member_name = user_in.name
                        member_discriminator = user_in.discriminator
                        member_device = "📱" if user_in.is_on_mobile() else "💻"
                        if member_nick is None:
                            member_nick = f"{member_name} #{member_discriminator} ({member_name})"
                        db.execute("INSERT INTO userundercontrol (id, user_id, user_name, user_device) VALUES (?, "
                                   "?, ?, ?)", (check[0], member_id, member_nick, member_device,))
                    await db.commit()

                    await message.clear_reaction("🟢")

                    warning = discord.Embed(title="🟩 CONTROLLO IN CORSO 🟩",
                                            description=f"Lo staff {user_send.mention} sta controllando degli utenti "
                                                        f"nella {i}° chat vocale \n \nUna volta chiuso al posto di "
                                                        f"questo messaggio troverete un rapporto dettagliato del "
                                                        f"controllo \n \n**PREMI LA REAZIONE PER CHIUDERE IL "
                                                        f"CONTROLLO**",
                                            color=discord.Color.green(), timestamp=dt.datetime.utcnow())
                    warning.set_footer(text=cfg.footer)
                    warning.set_author(name="Among Us Ita")

                    await message.edit(embed=warning)
                    await message.add_reaction("🔕")

                except Exception as error:
                    user_id = check[1]
                    db.execute("DELETE FROM ctrlhack WHERE admin_id = ?", (user_id,))
                    await db.commit()

                    warning = discord.Embed(title="🧻🚽 OH NO, QUALCOSA E' ANDATO STORTO 🚽🧻",
                                            description=f"{member.mention} la tua richiesta non è andata a buon "
                                                        f"termine, riprova e controlla che la stanza esista \nSe il "
                                                        f"problema persiste non esitare a contattare uno degli "
                                                        f"sviluppatori. \n"
                                                        f"{(guild.get_role(cfg.IDruoliDev[0])).mention} | {(guild.get_role(cfg.IDruoliDev[1])).mention} \n**ERRORE:**{error} \n \nQuesto messaggio si autodistruggerà tra 30 secondi...",
                                            color=discord.Color.dark_orange(), timestamp=dt.datetime.utcnow())
                    warning.set_footer(text=cfg.footer)
                    warning.set_author(name="Among Us Ita")
                    await message.edit(embed=warning, delete_after=30)
                    await message.clear_reactions()

            elif emoji_name == "🔴" and user_id == check[1]:
                await message.clear_reactions()

                user_send = self.bot.get_user(check[1])
                warning = discord.Embed(title="⬛️ IL CONTROLLO HACK E' STATO REVOCATO ⬛️",
                                        description=f"{user_send.mention}: questo messaggio si autodistruggerà tra 3 "
                                                    f"secondi...",
                                        color=discord.Colour.default(), timestamp=dt.datetime.utcnow())
                warning.set_footer(text=cfg.footer)
                warning.set_author(name="Among Us Ita")
                await message.edit(embed=warning, delete_after=3)

                user_send = check[1]
                db.execute("DELETE FROM ctrlhack WHERE admin_id = ?", (user_send,))
                await db.commit()

            elif emoji_name == "🔕" and user_id == check[1]:
                user_send = self.bot.get_user(check[1])
                numero = check[4]

                times = int((dt.datetime.utcnow() - message.embeds[0].timestamp).total_seconds())
                timem = int(round(times / 60)) if times >= 60 else 0
                times -= timem * 60 if timem != 0 else 0
                timeh = int(round(timem / 60)) if timem >= 60 else 0
                timem -= timeh * 60 if timeh != 0 else 0

                sus_users = db.fetchall("SELECT * FROM userundercontrol WHERE id = ?", (check[0],))

                sus_users_true = []

                for c in sus_users:
                    sus_users_true.append(c[2] + ' su ' + c[3])

                if len(sus_users_true) == 0:
                    sus_users_true = ["`Nessuno`"]

                sus_users_true = '\n'.join(sus_users_true)

                warning = discord.Embed(title="⬜️ CONTROLLO HACK FINITO ⬜️",
                                        description=f"**STAFF:** {user_send.mention} \n \n**DURATA:** {abs(timeh)}:{abs(timem)}:{abs(times)}  _(h:mm:ss)_ \n**UTENTI COINVOLTI:** \n{sus_users_true}",
                                        color=discord.Color.lighter_gray(), timestamp=dt.datetime.utcnow())
                warning.set_footer(text=cfg.footer)
                warning.set_author(name="Among Us Ita")
                await message.edit(embed=warning)

                guild_now = message.channel.guild
                category = discord.utils.get(guild_now.categories, name="controllo hack")
                category_channels = category.voice_channels

                for channel in category_channels:
                    if channel.name.startswith(f"Vocale {numero}") or channel.name.startswith(
                            f"┠ Vocale {numero}") or channel.name.startswith(f"┗ Vocale {numero}"):
                        await channel.delete()

                await message.clear_reaction("🔕")
                user_send = check[1]
                db.execute("DELETE FROM ctrlhack WHERE admin_id = ?", (user_send,))
                await db.commit()

            else:
                await message.remove_reaction(emoji, member)

        else:
            pass

    @commands.command()
    async def fail(self, ctx):
        cfg = self.bot.get_cog('Config')
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = cfg.rolea_all

        if len(user_roles.intersection(admin_roles)) != 0:
            await ctx.message.delete()
            for ctx.channel in (discord.utils.get(ctx.guild.categories, name="controllo hack")).voice_channels:
                await ctx.channel.delete()

    @commands.command()
    async def resetlist(self, ctx):
        cfg = self.bot.get_cog('Config')
        db = self.bot.get_cog('Db')
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = cfg.rolea_all

        if len(user_roles.intersection(admin_roles)) != 0:
            await ctx.message.delete()
            db.execute("DELETE FROM ctrlhack")
            db.execute("DELETE FROM user_under_control")
            await db.commit()
            await ctx.channel.send("Database svuotato", delete_after=2)


def setup(bot):
    bot.add_cog(Ctrlhack(bot))
    print("[!] modulo controllohack caricato")

from discord.ext import commands


class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command('help')

        self.aiutoadmin = "•[2 +] **purgeinvite** \n*[Cancella tutti gli inviti al server]*\n\
•[3 +] **editmsg** (idmsg) (testo) \n*[Edita un messaggio inviato con tsay]*\n\
•[5 +] **tuser** (@user) (testo) \n*[Invia EMBED a un utente]*\n\
•[5 +] **purge** (valore=max200) \n*[Elimina messaggi]*\n\
•[5 +] **tsay** (testo) \n*[Scrivi in chat]*\n\
•[5 +] **delwarn** (@user) (idwarn) (testo) \n*[Rimuovi il warn di un utente]*\n"

        self.aiutoadmin2 = "•[6 +] **ban** (@user or Name#0000) (motivo) \n*[Banna un utente]*\n\
•[6 +] **unban** (@Name#0000) (motivo) \n*[Sbanna un utente]*\n\
•[6 +] **kick** (@user) (motivo) \n*[Kicka un utente dal server]*\n\
•[6 +] **pollshelp** \n*[Comandi relativi ai sondaggi]*\n"

        self.aiutoadmin3 = "•[7 +] **addrole** (@ruolo) (@user) (motivo) \n*[Inserisce il ruolo al utente]*\n\
•[7 +] **bugadd** (testo) \n*[Inserisce un bug nel tracker]*\n\
•[7 +] **buglist** \n*[Mostra i bug nel tracker]*\n\
•[8 +] **mvto** (nome stanza) (@user @user) \n*[Sposta gli utenti in una stanza specifica]*\n\
•[8 +] **mvhere** (@user @user) \n*[Sposta gli utenti nella stanza dove ti trovi]*\n\
•[8 +] **hackhelp** \n*[Lista comandi controllo hack]*\n\
•[8 +] **addreact** (idmsg) (emoij) \n*[Aggiungi reazione]*\n\
•[8 +] **muteroom** (nome stanza) o muteroom \n*[Silenzia una stanza VoiP]*\n\
•[8 +] **unmuteroom** (nome stanza) o unmuteroom \n*[Attiva il VoiP in una stanza]*\n\
•[9 +] **find** (@user) \n*[Ricerca user in stanza VoiP]*\n\
•[9 +] **tickethelp** \n*[Lista comandi ticket]*\n\
•[9 +] **analytics** (@user) \n*[Visualizza le analisi dello staffer]*\n\
•[9 +] **warn** (@user) (gravità 1-4) (testo) \n*[Assegnare warn]*\n\
•[9 +] **warnings** (@user) \n*[Visualizza i warn di un utente]*\n"

        self.aiuto = "aiuto **[Mostra la lista dei comandi]**\n\
                insulta (utente) (M/F) **[Insulto random, definire se maschile o femminile]**\n\
                uservoice **[Vedi il totale di utenti nei canali vocali]"

        self.log = 751068836626956350  # Canale logs
        self.sanzioni = 757000456261206057  # canale sanzioni
        self.ingresso = 744613754829799444  # canale ingresso
        self.voicelogs = 751077692446736444  # canale voicelogs
        self.staffroom = 746868296892284948
        self.categories = ["STAFF VOICE"]

        # ADMIN PEX

        self.roledev = 758086640047620136  # 3rd Party
        self.rolea1 = 744631580504359043  # Owner
        self.rolea2 = 744631542608822422  # Admin
        self.rolea3 = 762459421665525802  # Senior Mod
        self.rolea4 = 744631301872680980  # Mod
        self.rolea5 = 762459426128789525  # Senior Helper
        self.rolea6 = 754829854066737182  # Helper
        self.rolea7 = 762459428402233355  # Trial Helper
        self.rolea8 = 762459430528483359  # Gestore
        self.rolea9 = 762460098286190593  # Prova

        self.rolea_all = {self.rolea1, self.rolea2, self.rolea3, self.rolea4, self.rolea5, self.rolea6, self.rolea7,
                          self.rolea8, self.rolea9, self.roledev}
        self.rolea_top8 = {self.rolea1, self.rolea2, self.rolea3, self.rolea4, self.rolea5, self.rolea6, self.rolea7,
                           self.rolea8, self.roledev}
        ##

        #######################################################################################
        # CONTROLLO CANALI
        # self.generale = (self.bot.get_guild(744613238339010632)).get_channel(747841447407124510)
        # self.altro = (self.bot.get_guild(744613238339010632)).get_channel(744613862489456692)
        # self.memes = (self.bot.get_guild(744613238339010632)).get_channel(747877601812676679)
        # self.fanart = (self.bot.get_guild(744613238339010632)).get_channel(747877573131763893)
        # self.botchannel = (self.bot.get_guild(744613238339010632)).get_channel(744640288366264351)
        # self.botchannel2 = (self.bot.get_guild(744613238339010632)).get_channel(755456219732377741)
        # self.musica = (self.bot.get_guild(744613238339010632)).get_channel(747843244888555621)

        # self.matchmaking = (self.bot.get_guild(744613238339010632)).get_channel(748932393154641970)
        # self.matchmakingrep = (self.bot.get_guild(744613238339010632)).get_channel(754724642261958686)

        # CANALI CONTROLLLATI DAL BOT - MATCHMAKING
        # self.canalimatch = set((self.matchmaking, self.matchmakingrep))

        # CANALI CONTROLLATI DAL BOT - ANTI SPAM
        # self.canalispam = set((self.generale, self.altro, self.memes, self.fanart, self.botchannel, self.botchannel2, self.musica))
        #######################################################################################

        # controllo parole scurrilid
        self.badwords = []

        # DEFINE COLORI
        self.lightgreen = 0xc3eb34
        self.red = 0x912519
        self.blue = 0x3268a8
        self.green = 0x008000

        self.autorole = 44444

        self.footer = "Among Us Ita 0.1 **beta**"

        self.IDruoliDev = (758086249436151908,
                           758086640047620136)  # id dei ruoli dei dev nel server test (gestore dev, dev) per il server principale cambiarli in (758086249436151908, 758086640047620136)

        self.welcomemessage = "Ciao *{user}* benvenuto/a in **{server}** come prima cosa ti consigliamo di leggere il {regole}.\n\n\
 \n**Annunci e staff** Generalmente tutte le cose che facciamo tra le quali eventi/sondaggi/candidature per far parte del nostro team saranno annunciati in {annunci}.\n\n\
 \n**Tornei e eventi**\nVi chiederete cosa sia {wtf}.**WTF** è uno degli enti che collabora con noi per quanto riguarda la gestione degli eventi. Grazie a questa organizzazione potrete partecipare a tornei legalizzati con premi in denaro in modo totalmente gratuito.\n\n"

        self.welcomemessage2 = "I {booster} sono degli utenti che hanno deciso di boostare il nostro server. Il boost è un potenziamento che si può ottenere in qualsiasi server discord, in questo caso nel nostro discord avrete dei privilegi che potrete trovare nel canale apposito {annunci}.\n\n\
 \n**Supporto**\nNel caso in cui tu abbia dei problemi o per qualsiasi motivo tu voglia conatattare lo staff dirigiti nel canale {report}.\n\n\
 \n**Attività e gameplay**\nNei canali {matchmaking} e {generale} potrai interaggire attivamente con la community."

        self.welcomemessage3 = "Con ciò ti auguriamo una **buona permanenza** nella community di {server}"


def setup(bot):
    bot.add_cog(Config(bot))
    print("[!] modulo config caricato")

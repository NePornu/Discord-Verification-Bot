import discord
from discord.ext import commands
import logging
import datetime

# Nastavení logování
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

TOKEN = "BOT-TOKEN"
GUILD_ID = 123456789  # ID serveru
VERIFIED_ROLE_ID = 123456789  # ID ověřovací role
MODERATOR_ROLE_ID = 123456789  # ID role moderátora
VERIFICATION_CODE = 'OVERENO'  # Ověřovací kód
MOD_CHANNEL_ID = 123456789  # ID kanálu pro moderátory
LOG_CHANNEL_ID = 123456789  # ID kanálu pro logování ověření

intents = discord.Intents.default()
intents.members = True  # Zajišťuje sledování členů
intents.messages = True  # Zajišťuje sledování zpráv
intents.guilds = True  # Zajišťuje sledování serverů
intents.dm_messages = True  # Zajišťuje sledování zpráv v DM
intents.message_content = True  # Povolení čtení obsahu zpráv (nutné pro příkazy jako "OVERENO")

bot = commands.Bot(command_prefix='*', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Bot je online jako {bot.user}')

@bot.event
async def on_member_join(member):
    try:
        # Získání aktuálního dne v týdnu
        current_day = datetime.datetime.now().weekday()  # 0 = Pondělí, 6 = Neděle
        
        # Ověření pouze ve všední dny (Pondělí - Pátek)
        if current_day < 5:  # 0 - 4 znamená Pondělí až Pátek
            await member.send("👋 Vítej! Pro ověření napiš 'OVERENO' do odpovědi.")
        
            def check(msg):
                return msg.author == member and isinstance(msg.channel, discord.DMChannel)
        
            # Čekání na odpověď bez časového limitu
            response = await bot.wait_for('message', check=check)
            if response.content.strip().upper() == VERIFICATION_CODE.upper():
                await member.send("✅ Ověření probíhá, čekej na potvrzení moderátora.")
                guild = bot.get_guild(GUILD_ID)
                mod_channel = guild.get_channel(MOD_CHANNEL_ID)
                if mod_channel:
                    await mod_channel.send(
                        f'🛡️ Uživatel {member.mention} čeká na potvrzení. Moderátoři, použijte `*potvrdit {member.id}`.'
                    )
                else:
                    logging.warning(f"⚠️ Kanál s ID '{MOD_CHANNEL_ID}' nenalezen.")
            else:
                await member.send("❌ Nesprávné slovo. Zkus to znovu.")
        else:
            await member.send("❌ Ověření je možné pouze ve všední dny. Zkus to prosím později.")
            logging.info(f"⏳ Ověření bylo zamítnuto pro uživatele {member.mention} z důvodu nepracovního dne.")
    except Exception as e:
        logging.error(f'Chyba při ověřování uživatele {member.mention}: {e}')

@bot.command()
@commands.has_role(MODERATOR_ROLE_ID)
async def potvrdit(ctx, *user_ids: int):
    role = ctx.guild.get_role(VERIFIED_ROLE_ID)  # Ověřovací role
    log_channel = ctx.guild.get_channel(LOG_CHANNEL_ID)  # Kanál pro logování
    
    if not role:
        await ctx.send("❌ Ověřovací role nebyla nalezena.")
        return
    
    if not user_ids:
        await ctx.send("❌ Nezadali jste žádné uživatelské ID.")
        return
    
    potvrzeni_uzivatele = []
    chyby = []
    
    for user_id in user_ids:
        member = ctx.guild.get_member(user_id)
        if member:
            if role in member.roles:
                await member.remove_roles(role)
                try:
                    await member.send('❌ Tvoje ověřovací role byla odebrána moderátorem.')
                except Exception:
                    pass
                potvrzeni_uzivatele.append(member.mention)
            else:
                chyby.append(f"{member.mention} nemá ověřovací roli.")
        else:
            chyby.append(f"Uživatel s ID `{user_id}` nebyl nalezen.")
    
    # Výstup pro moderátory
    if potvrzeni_uzivatele:
        await ctx.send(f"✅ Ověřovací role byla odebrána uživatelům: {', '.join(potvrzeni_uzivatele)}.")
    if chyby:
        await ctx.send(f"⚠️ Chyby při ověřování:\n" + "\n".join(chyby))
    
    # Logování do kanálu
    if log_channel and potvrzeni_uzivatele:
        await log_channel.send(
            f"🛡️ Moderátor {ctx.author.mention} odebral ověřovací role uživatelům: {', '.join(potvrzeni_uzivatele)}."
        )


bot.run(TOKEN)

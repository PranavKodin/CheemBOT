import discord
import difflib
from discord.ext import commands
import config
from replies import replies

intents= discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print("bhoww bhowww hukuum maalik!")
    await bot.tree.sync()
image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff')
@bot.event
async def on_message(msg: discord.Message):
    if msg.author == bot.user:
        return
    content = msg.content
    cont = list(replies.keys())
    closest_match = difflib.get_close_matches(content.lower(), cont, n=1, cutoff=0.6)
    
    if closest_match:
        ask = closest_match[0]
        for keyword, response in replies.items(): 
            if ask.lower() == keyword:
                if response.lower().endswith(image_extensions):
                    await msg.channel.send(response)
                break
            await msg.reply(response)
        return
    return None
    

@bot.tree.command()
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("bhoww bhowww!")

@bot.tree.command()
async def profile(inter: discord.Interaction):
    """Profile"""
    embed = discord.Embed(title="Cheems wala kutta Bot", description="hemlo fremds! Chintapak Dum Dum", color= 0xf79d1e)
    embed.set_thumbnail(url = "https://i.pinimg.com/originals/ca/7b/8d/ca7b8da71794636868ab8c58ff043710.gif")
    await inter.response.send_message(embed=embed)
    
@bot.tree.command()
@commands.has_permissions(manage_messages=True)
async def clear(interaction: discord.Interaction, amount: int):
    """Clears a specified number of messages."""
    await interaction.response.defer(thinking=True,ephemeral=True)
    await interaction.channel.purge(limit=amount+1)
    await interaction.followup.send(f"{amount} messages demlete karmdiye")

@clear.error
async def on_error(interaction: discord.Integration, error: commands.CommandError):
    if isinstance(error, commands.MissingPermissions):
        await interaction.followup.send("lomde tere pe permission nhi hai", ephemeral=True)

@bot.tree.command()
async def kick(interaction: discord.Interaction, member: discord.Member, *, reason: str):
    """laat maarke nikalo isko server se."""
    await member.kick(reason=reason)
    await interaction.followup.send(f"{member.display_name} k gemd pe lat marke nikal diya kiyunki {reason}")


@bot.tree.command()
async def dm(interaction: discord.Interaction, member: discord.Member, *, message: str):
    """Sends a DM to a member."""
    await member.send(message)
    await interaction.response.send_message(f"{member.display_name} ko DM bhemj diya")
@bot.event
async def on_guild_channel_create(channel: discord.abc.GuildChannel):
    """Create a guid channel"""
    print("channel created")
    print(channel.name)



bot.run(config.discord_token)

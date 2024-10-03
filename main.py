import discord
from discord.ext import commands, tasks
import requests
from discord import option
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# API URLs for Java and Bedrock Minecraft servers
java_url = "https://api.mcstatus.io/v2/status/java/"
bedrock_url = "https://api.mcstatus.io/v2/status/bedrock/"

# Global variables for tracking the server to be updated
SERVER_TYPE = None
SERVER_IP = None
CHANNEL = None
CONNECTION_INSTRUCTIONS = None
CUSTOM_IMAGE_URL = None

# Command to ping bot
@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong! Your bot is online and ready to go!")

# Slash command to set up status for a Minecraft server (Java or Bedrock)
@bot.slash_command(name="status", description="Get the status of the Minecraft server (Java or Bedrock)")
@option("server_type", description="Choose the type of Minecraft server", choices=["Java", "Bedrock"])
@option("server_ip", description="Enter the server IP")
@option("channel", discord.TextChannel, description="Choose the channel to send updates to", required=False)
@option("connection_instructions", description="Add custom server connection instructions (e.g., IP/Port)", required=False)
@option("custom_image_url", description="Provide a custom image URL for the embed", required=False)  # New option
async def status(ctx, server_type: str, server_ip: str, channel: discord.TextChannel = None, connection_instructions: str = None, custom_image_url: str = None):
    global SERVER_TYPE, SERVER_IP, CHANNEL, CONNECTION_INSTRUCTIONS, CUSTOM_IMAGE_URL

    await ctx.defer()

    # Set global variables
    SERVER_TYPE = server_type
    SERVER_IP = server_ip
    CHANNEL = channel
    CONNECTION_INSTRUCTIONS = connection_instructions
    CUSTOM_IMAGE_URL = custom_image_url  # Store custom image URL

    # Set up and fetch the initial status
    if server_type.lower() == "java":
        url = f"{java_url}{server_ip}"
    else:
        url = f"{bedrock_url}{server_ip}"

    # Fetch server data
    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200 and data:
            # Create a visually appealing embed
            embed = discord.Embed(
                title=f"✨ Minecraft {server_type} Server Status",
                description=f"Here’s the current status of **{server_ip}** 🏞️",
                color=discord.Color.purple()
            )
            
            embed.set_thumbnail(url="https://i.imgur.com/1Q6Pqku.png")  # Default Minecraft icon or related image
            
            if data.get("online"):
                embed.add_field(name="🔌 Status", value="🟢 **Online**", inline=False)
                embed.add_field(name="👥 Players", value=f"**{data['players']['online']}** / {data['players']['max']}", inline=True)
                
                version = data.get('version', {})
                version_name = version.get('name_clean', "Unknown Version")
                embed.add_field(name="⚙️ Version", value=f"**{version_name}**", inline=True)

                motd = data.get('motd', {}).get('clean', [''])[0]
                embed.add_field(name="🌟 MOTD (Message of the Day)", value=f"`{motd}`" if motd else "No MOTD", inline=False)

            else:
                embed.add_field(name="🔌 Status", value="🔴 **Offline**", inline=True)

            # Custom server connection instructions or default message
            if connection_instructions:
                embed.add_field(
                    name="🛠️ Server Connection Info",
                    value=f"```{connection_instructions}```",
                    inline=False
                )
            else:
                embed.add_field(
                    name="🛠️ Server Connection Info",
                    value="`Java: play.minepvp.fun` \n`Bedrock: 19132/default`",  # Default example instructions
                    inline=False
                )
            
            # Set custom image or default image if none provided
            if custom_image_url:
                embed.set_image(url=custom_image_url)
            else:
                embed.set_image(url="https://i.imgur.com/UzAE9pG.png")  # Default background

            embed.set_footer(text="🔄 Server status updates every 1 minute.", icon_url="https://i.imgur.com/1Q6Pqku.png")

            # Send embed to the provided channel, or default to the current context
            target_channel = channel if channel else ctx.channel
            await target_channel.send(embed=embed)

            # Start the loop to update status every minute
            update_status.start()
        else:
            await ctx.followup.send("⚠️ Could not retrieve the server status. Please check the IP and try again.")
    except Exception as e:
        await ctx.followup.send(f"Error fetching server status: {e}")

# Function to fetch server status
def fetch_server_status(server_type, server_ip):
    url = f"{java_url}{server_ip}" if server_type.lower() == "java" else f"{bedrock_url}{server_ip}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print(f"Error fetching server status: {e}")
        return None

# Task to update the server status every minute
@tasks.loop(minutes=1)
async def update_status():
    if SERVER_TYPE and SERVER_IP and CHANNEL:
        data = fetch_server_status(SERVER_TYPE, SERVER_IP)
        if data and data.get("online"):
            embed = discord.Embed(
                title=f"✨ Minecraft {SERVER_TYPE} Server Status",
                description=f"Here's the current status of **{SERVER_IP}** 🏞️",
                color=discord.Color.blurple()
            )
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1291362971641053216/1291366425583161385/image.png?ex=66ffd634&is=66fe84b4&hm=cfeec2e803cb68caf7b1497bbb5f6b8983dbc1c9ac53198a0e471571f67e9ac8&")
            embed.add_field(name="🔌 Status", value="🟢 **Online**", inline=False)
            embed.add_field(name="👥 Players", value=f"**{data['players']['online']}** / {data['players']['max']}", inline=True)

            version = data.get('version', {})
            version_name = version.get('name_clean', "Unknown Version")
            embed.add_field(name="⚙️ Version", value=f"**{version_name}**", inline=True)

            motd = data.get('motd', {}).get('clean', [''])[0]
            embed.add_field(name="🌟 MOTD (Message of the Day)", value=f"`{motd}`" if motd else "No MOTD", inline=False)

            # Custom connection instructions or default example
            if CONNECTION_INSTRUCTIONS:
                embed.add_field(
                    name="🛠️ Server Connection Info",
                    value=f"```{CONNECTION_INSTRUCTIONS}```",
                    inline=False
                )
            else:
                embed.add_field(
                    name="🛠️ Server Connection Info",
                    value="`Java: play.projectmc.fun` \n`Bedrock: 25565`",
                    inline=False
                )

            # Use the custom image URL if provided, else default background
            if CUSTOM_IMAGE_URL:
                embed.set_image(url=CUSTOM_IMAGE_URL)
            else:
                embed.set_image(url="https://cdn.discordapp.com/attachments/1291362971641053216/1291366425583161385/image.png?ex=66ffd634&is=66fe84b4&hm=cfeec2e803cb68caf7b1497bbb5f6b8983dbc1c9ac53198a0e471571f67e9ac8&")  # Default background

            # Edit the latest message in the channel
            async for message in CHANNEL.history(limit=1):
                if message.author == bot.user:
                    await message.edit(embed=embed)

# Event to confirm bot is ready
@bot.event
async def on_ready():
    print("🚀 Bot is ready!")

# Run the bot
bot.run(TOKEN)

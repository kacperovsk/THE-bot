import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
ROLE_NAME = 'FAILRP'  # Default role name if none is specified

# Bot setup
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command(name="add_role")
async def add_role(ctx, role_mention: discord.Role = None):
    # If no role is mentioned, return an error
    if not role_mention:
        await ctx.send("Please mention a role to assign, e.g., `!add_role @split1`")
        return

    # Check if the command is a reply to another message
    if ctx.message.reference:
        # Fetch the replied message
        replied_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)

        added_count = 0
        # Assign the role to all mentions in the replied message
        if replied_message.mentions:
            for member in replied_message.mentions:
                try:
                    await member.add_roles(role_mention)
                    added_count += 1
                except Exception as e:
                    print(f"Failed to assign role to {member}: {e}")
            await ctx.send(f"✅ Successfully assigned the role '{role_mention.name}' to {added_count} members.")
        else:
            await ctx.send("No users mentioned in the replied-to message.")
    else:
        await ctx.send("Please reply to a message with mentions to assign roles.")

@bot.command(name="remove_role")
async def remove_role(ctx, role_mention: discord.Role = None):
    # If no role is mentioned, return an error
    if not role_mention:
        await ctx.send("Please mention a role to remove, e.g., `!remove_role @split1`")
        return

    # Check if the command is a reply to another message
    if ctx.message.reference:
        # Fetch the replied message
        replied_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)

        # Counter for successfully removed roles
        removed_count = 0

        # Remove the role from all mentions in the replied message
        if replied_message.mentions:
            for member in replied_message.mentions:
                try:
                    await member.remove_roles(role_mention)
                    removed_count += 1
                except Exception as e:
                    print(f"Failed to remove role from {member}: {e}")

            # Send a message with the count of members the role was removed from
            await ctx.send(f"✅ Successfully removed the role '{role_mention.name}' from {removed_count} members.")
        else:
            await ctx.send("No users mentioned in the replied-to message.")
    else:
        await ctx.send("Please reply to a message with mentions to remove roles.")

@bot.command(name="remove_all")
async def remove_all(ctx, role: discord.Role = None):
    # If no role is mentioned, return an error
    if not role:
        await ctx.send("Please mention a role to remove from all users, e.g., `!remove_all @split1`")
        return

    # Get all members who have the role
    members_with_role = [member for member in ctx.guild.members if role in member.roles]

    # Counter for successfully removed roles
    removed_count = 0

    # Remove the role from all members who have it
    for member in members_with_role:
        try:
            await member.remove_roles(role)
            removed_count += 1
        except Exception as e:
            print(f"Failed to remove role from {member}: {e}")

    # Send a message with the count of members the role was removed from
    await ctx.send(f"✅ Successfully removed the role '{role.name}' from {removed_count} members.")
# Run the bot
bot.run(TOKEN)

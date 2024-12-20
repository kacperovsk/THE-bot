import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from discord import Role

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


@bot.check
async def check_role(ctx):
    return any(role.name == "Ręka Khora" for role in ctx.author.roles)


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
                if role_mention in member.roles:
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
async def remove_all(ctx, roles: commands.Greedy[Role] = None):
    # If no role is mentioned, return an error
    if not roles:
        await ctx.send("Please mention a role to remove from all users, e.g., `!remove_all @split1`")
        return

    # Get all members who have the role
    members_with_role = [member for member in ctx.guild.members if roles in member.roles]

    # Counter for successfully removed roles
    removed_counts = {}

    for role in roles:
        removed_count = 0

        # Remove the role from all members who have it
        for member in ctx.guild.members:
            if role in member.roles:
                try:
                    await member.remove_roles(role)
                    removed_count += 1
                except Exception as e:
                    print(f"Failed to remove role {role} from {member}: {e}")
            removed_counts[role.name] = removed_count
    # Send a message with the count of members the role was removed from
    result_message = "✅ Role removal summary:\n"
    for role_name, count in removed_counts.items():
        result_message += f"- Removed role '{role_name}' from {count} members.\n"
    await ctx.send(result_message)

ROLE_IDS_GROUPS = {
    "splits": [1318957973057568860, 1318958055668449341, 1318958096852451439]  # Replace with real IDs
}

async def remove_all(ctx, group_name: str = None):
    """
    Removes all roles from a predefined group (e.g., "splits") from all members who have them.
    """
    # Check if the group_name is provided
    if not group_name:
        await ctx.send("Please specify a group of roles to remove, e.g., `!remove_all splits`")
        return

    # Fetch the role IDs for the given group name
    role_ids = ROLE_IDS_GROUPS.get(group_name.lower())
    if not role_ids:
        await ctx.send(f"No roles are configured for the group '{group_name}'.")
        return

    # Fetch the roles from the server by their IDs
    roles_to_remove = [ctx.guild.get_role(role_id) for role_id in role_ids]
    roles_to_remove = [role for role in roles_to_remove if role]  # Filter out invalid roles

    if not roles_to_remove:
        await ctx.send(f"Could not find any valid roles for the group '{group_name}'.")
        return

    removed_counts = {role.name: 0 for role in roles_to_remove}

    # Iterate through all members in the guild
    for member in ctx.guild.members:
        for role in roles_to_remove:
            if role in member.roles:
                try:
                    await member.remove_roles(role)
                    removed_counts[role.name] += 1
                except Exception as e:
                    print(f"Failed to remove role {role.name} from {member}: {e}")

    # Prepare the result summary
    result_message = f"✅ Role removal summary for group '{group_name}':\n"
    for role_name, count in removed_counts.items():
        result_message += f"- Removed role '{role_name}' from {count} members.\n"

    await ctx.send(result_message)
    
# Run the bot
bot.run(TOKEN)

import threading
from flask import Flask, flash, redirect, render_template, request, session, abort, Response
import re, discord
from discord.ext import commands
import asyncio

app = Flask(__name__)
intents = discord.Intents.all()
intents.messages = True

# client = discord.Client(intents=intents)


bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
  print(f"{bot.user} has connected to Discord and listeing at 127.0.0.1 port=5000")
#   server = client.fetch_guild(SERVER_ID)
#   server = bot.get_guild(SERVER_ID)
#   print("bot guild", server)
@app.route("/")
def hello():
    return "hello"


@app.route('/api/v1/discord/users/roles', methods=['PUT'])
async def manage_role():
    data = request.json
    username = data['discordUsername']
    role = data['role']
    action = data['action']

    print(username, role, action)

    
    if action == "ADD":
            IsExist, member = GetInfo(username)
            if IsExist:
                 print("add")
                 await Assign_role(member, role)
            else:
                return Response("Error!, User don't exist.", status=400)
    elif action == "DEL":
        IsExist, member = GetInfo(username)
        if IsExist:
             await Remove_role(member, role)
        else:
            return Response("Error!, User don't exist.", status=400)
    
    
    return Response("Error!, action is not correct.", status=404)

async def Add_roles(member, roles_to_add):
    await member.add_roles(*roles_to_add, reason="Roles assigned by admin.")

async def Assign_role(member, role):
    print("Assigning roles...", member, role)
    roles = set(re.findall("VWU EPM|VWU MG1|VWU PRG1|VWU TGI", role, re.IGNORECASE))
    
    if roles:
        server = bot.get_guild(SERVER_ID)
        print(roles, server.roles)
        
        new_roles =  set([discord.utils.get(server.roles, name=role) for role in roles]) 
        print("new_roles", new_roles)
        current_roles = set(member.roles)
        roles_to_add = new_roles.difference(current_roles)
        print("roles to add", roles_to_add)
        try:
            print("adding...")
            await asyncio.wait_for(Add_roles(member, roles_to_add), timeout=10)
            print("end adding")
            # await member.add_roles(*roles_to_add, reason="Roles assigned by admin.")
        except asyncio.TimeoutError:
            print("Timeout occurred while assigning roles.")
            return Response("Timeout occurred while assigning roles.", status=400)
        except Exception as e:
        # Handle other exceptions
            print("An error occurred:", str(e))
            return Response(f"An error occurred:{str(e)}", status=400)
        else:
            return Response(f"""You've been assigned the following role{"s" if len(roles_to_add) > 1 else ""} on {server.name}: { ', '.join(role.name for role in roles_to_add) }.""", status=200)
    else:
       await Response("No suppoerted roles were found in your message.", status=400)


def GetInfo(username):
   for guild in bot.guilds:
        for member in guild.members:
            print("member", member)
            if username == str(member).split("#")[0]:
                print("exist")
                return True, member
    
   print("not exist")
   return False

async def Remove_role(member, role):
    print("Remove roles...")
    roles = set(re.findall("VWU EPM|VWU MG1|VWU PRG1|VWU TGI", role, re.IGNORECASE))

    if roles:
        server = bot.get_guild(SERVER_ID)
        new_roles =  set([discord.utils.get(server.roles, name=role) for role in roles]) 
        current_roles = set(member.roles)
        roles_to_remove = new_roles.intersection(current_roles)
        try:
            await member.remove_roles(*roles_to_remove, reason="Roles removed by admin.")
        except Exception as e:
            print(e)
            return Response("Error assigning roles.", status=400)
        else:
            await Response(f"""You've been assigned the following role{"s" if len(roles_to_remove) > 1 else ""} on {server.name}: { ', '.join(role.name for role in roles_to_remove) }.""", status=200)
    else:
       await Response("No suppoerted roles were found in your message.", status=400)

def run_discord_bot():
    bot.run(DISCORD_TOKEN)

def run_flask_server():
    app.run(host='127.0.0.1', port=5000)

if __name__ == "__main__":
    # app.run(host="127.0.0.1", port=5000)
    flask_thread = threading.Thread(target=run_flask_server)
    discord_thread = threading.Thread(target=run_discord_bot)

    flask_thread.start()
    discord_thread.start()

    flask_thread.join()
    discord_thread.join()

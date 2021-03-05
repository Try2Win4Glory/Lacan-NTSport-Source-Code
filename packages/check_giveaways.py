from discord.ext import tasks, commands
from mongoclient import DBClient
import copy, time, random
from discord.utils import get

class CheckGiveaways(commands.Cog):
    def __init__(self, client):
        self.check_giveaways.start()
        self.client = client

    @tasks.loop(seconds=3)
    async def check_giveaways(self):
        dbclient = DBClient()
        collection = dbclient.db.giveaways
        documents = await dbclient.get_array(collection, {})
        async for data in documents:
            if int(time.time()) >= data['endtime'] and data['ended'] == False:
                old = copy.deepcopy(data)
                channel = get(self.client.get_all_channels(), id=data['channelID'])
                msg = get(await channel.history(limit=1000).flatten(), id=data['messageID'])
                amt_winners = data['winners']
                if msg == None:
                    data['ended'] = True
                    await dbclient.update_array(collection, old, data)
                    continue
                try:
                    winners = random.choices(data['joined'], k=amt_winners)
                    mentions = ''
                    for winner in winners:
                        mentions += f'<@{winner}>'
                    if data['joined'] == []:
                        await msg.channel.send(f'No one won \n{msg.jump_url}')
                    else:
                        await msg.channel.send(f'<@{mentions}> won {msg.jump_url}')
                        
                except KeyError:
                    await msg.channel.send(f'No one won \n{msg.jump_url}')

                data['ended'] = True
                await dbclient.update_array(collection, old, data)
            else:
                continue


    '''@commands.command()
    async def reroll(self, ctx, id_ : int):
          client = self.client
          channel = client.get_channel(c_id)
          try:
            new_msg = await channel.fetch_message(id_)
          except:
            await ctx.send("The ID that was entered was incorrect, make sure you have entered the correct giveaway message ID.")
          users = await new_msg.reactions[0].users().flatten()
          users.pop(users.index(client.user))

          winner = random.choice(users)

          await channel.send(f"Congratulations the new winner is: {winner.mention} for the giveaway rerolled!")'''
                    

def setup(client):
    client.add_cog(CheckGiveaways(client))
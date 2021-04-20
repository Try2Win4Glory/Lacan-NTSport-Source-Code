'''description'''

from discord.ext import commands
from packages.utils import Embed, ImproperType
from mongoclient import DBClient
import json
class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def db_update(self, ctx):
        return
        dbclient = DBClient()
        collection = dbclient.db.NT_to_discord
        with open('NT_to_discord.json', 'r') as f:
            data = json.loads('{"registered":'+f.read()+'}')
        await dbclient.create_doc(collection, data)
def setup(client):
    client.add_cog(Command(client))
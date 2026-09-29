import os, discord, random, json
from discord.ext import commands
from discord import ui
from datetime import datetime

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

IP = "103.150.61.75:7790"
NAMA_SERVER = "Kembali Roleplay"
FILE_DB = "database_ucp.json"

def load_db():
    if not os.path.exists(FILE_DB):
        return {"pins": []}
    try:
        with open(FILE_DB, "r") as f:
            return json.load(f)
    except:
        return {"pins": []}

def save_db(data):
    with open(FILE_DB, "w") as f:
        json.dump(data, f)

def buat_pin_unik():
    db = load_db()
    while True:
        pin = str(random.randint(100000, 999999))
        if pin not in db["pins"]:
            db["pins"].append(pin)
            save_db(db)
            return pin

class FormUCP(ui.Modal, title="Buat Akun UCP"):
    nama = ui.TextInput(label="Nama UCP", placeholder="Contoh: Sapurumah")
    async def on_submit(self, inter: discord.Interaction):
        pin = buat_pin_unik()
        nama = self.nama.value
        tgl = datetime.now().strftime("%d/%m/%Y %I:%M %p")
        await inter.response.send_message(f"✅ UCP {nama} berhasil! Cek DM kamu!", ephemeral=True)
        teks = f"CEK AKUN | {NAMA_SERVER}\n✅ Berhasil!\n\nNama UCP\n{nama}\n\nKode Verifikasi/PIN\n{pin}\n\nPemilik Akun\nID: {inter.user.id}\nUsername: {inter.user.name}\n\nStatus\nTerverifikasi\n\nJangan beritahu info ini ke orang lain!\n\n{NAMA_SERVER} | {tgl}"
        try:
            await inter.user.send(teks)
        except:
            await inter.followup.send(f"DM ketutup! Kode lu: {pin}", ephemeral=True)

class TombolUCP(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @ui.button(label="Buat UCP Disini", style=discord.ButtonStyle.green, emoji="🔥", custom_id="kembali_final_v2")
    async def buat(self, inter: discord.Interaction, btn: ui.Button):
        await inter.response.send_modal(FormUCP())

@bot.event
async def on_ready():
    bot.add_view(TombolUCP())
    print(f"BOT {bot.user} READY!")

@bot.command()
async def setup(ctx):
    await ctx.channel.purge(limit=5)
    em = discord.Embed(title=f"{NAMA_SERVER} - UCP", description=f"IP: `{IP}`\n\nKlik tombol di bawah buat daftar!", color=0x2b2d31)
    await ctx.send(embed=em, view=TombolUCP())

bot.run(os.getenv("TOKEN"))

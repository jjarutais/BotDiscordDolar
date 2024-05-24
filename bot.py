import discord
from discord.ext import commands, tasks
import requests

# Configurações
TOKEN = ""
CHANNEL_ID = ""
PREFIX = "!"

# Inicializa as intenções padrão
intents = discord.Intents.all()
intents.messages = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} está conectado ao Discord!')
    send_dolar_rate.start()
    print(f"Permissão de conteúdo de mensagens: {intents.messages}")

@tasks.loop(minutes=20)
async def send_dolar_rate():
    try:
        channel = bot.get_channel(int(CHANNEL_ID))
        if channel:
            response = requests.get('https://economia.awesomeapi.com.br/last/USD-BRL')
            response.raise_for_status()  # Levanta um erro para status de resposta HTTP ruins
            data = response.json()
            dolar_rate = float(data['USDBRL']['bid'])
            await channel.send(f'>>@task.loop<<')
            await channel.send(f'O valor do dolar em reais agora é R${dolar_rate:.2f}')
        else:
            print('Canal não encontrado ou sem permissão para enviar mensagens.')
    except requests.exceptions.RequestException as e:
        print(f'Erro ao buscar a taxa de câmbio: {e}')

@bot.command(name='dolar')
async def dolar(ctx):
    try:
        response = requests.get('https://economia.awesomeapi.com.br/last/USD-BRL')
        response.raise_for_status()  # Levanta um erro para status de resposta HTTP ruins
        data = response.json()
        dolar_rate = float(data['USDBRL']['bid'])
        await ctx.send(f'O valor do dólar em reais agora é R${dolar_rate:.2f}')
    except requests.exceptions.RequestException as e:
        print(f'Erro ao buscar a taxa de câmbio: {e}')
        await ctx.send('Ocorreu um erro ao buscar a taxa de câmbio.')

@bot.command(name='euro')
async def euro(ctx):
    try:
        response = requests.get('https://economia.awesomeapi.com.br/last/EUR-BRL')
        response.raise_for_status()  # Levanta um erro para status de resposta HTTP ruins
        data = response.json()
        euro_rate = float(data['EURBRL']['bid'])
        await ctx.send(f'O valor do euro em reais agora é R${euro_rate:.2f}')
    except requests.exceptions.RequestException as e:
        print(f'Erro ao buscar a taxa de câmbio: {e}')
        await ctx.send('Ocorreu um erro ao buscar a taxa de câmbio.')

@bot.command(name='bitcoin')
async def bitcoin(ctx):
    try:
        response = requests.get('https://economia.awesomeapi.com.br/last/BTC-BRL')
        response.raise_for_status()  # Levanta um erro para status de resposta HTTP ruins
        data = response.json()
        bitcoin_rate = float(data['BTCBRL']['bid'])
        await ctx.send(f'O valor do euro em reais agora é R${bitcoin_rate:.2f}')
    except requests.exceptions.RequestException as e:
        print(f'Erro ao buscar a taxa de câmbio: {e}')
        await ctx.send('Ocorreu um erro ao buscar a taxa de câmbio.')

@bot.command(name='ajuda')
async def commands_list(ctx):
    embed = discord.Embed(title="Lista de Comandos", description="Lista de comandos disponíveis para uso", color=discord.Color.blue())
    embed.add_field(name="!dolar", value="Obtenha a taxa de câmbio atual do dólar em reais.", inline=False)
    embed.add_field(name="!euro", value="Obtenha a taxa de câmbio atual do euro em reais.", inline=False)
    embed.add_field(name="!bitcoin", value="Obtenha a taxa de câmbio atual do bitcoin em reais.", inline=False)
    embed.add_field(name="!conversor", value="Converta uma quantia de uma moeda para outra. Exemplo: !conversor 100 USD BRL", inline=False)
    await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Este comando não existe. Use `!ajuda` para ver a lista de comandos disponíveis.")


@bot.command(name='conversor')
async def conversor(ctx, quantidade: str, moeda_origem: str, moeda_destino: str):
    try:
        quantidade = float(quantidade.replace(',', '.'))
    except ValueError:
        await ctx.send("Por favor, insira um valor numérico válido para a quantidade.")
        return

    url = f"https://economia.awesomeapi.com.br/last/{moeda_origem}-{moeda_destino}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Levanta um erro para status de resposta HTTP ruins
        data = response.json()
        taxa_conversao = float(data[f'{moeda_origem}{moeda_destino}']['bid'])
        resultado = quantidade * taxa_conversao

        await ctx.send(f"{quantidade} {moeda_origem} equivale a {resultado:.2f} {moeda_destino}")
    except KeyError:
        await ctx.send("Ocorreu um erro ao processar a conversão: Moeda não encontrada ou formato incorreto.")
    except Exception as e:
        await ctx.send(f"Ocorreu um erro ao processar a conversão: {e}")

bot.run(TOKEN)

import discord
from discord.ext import commands
import asyncio
import aiohttp
import os
from dotenv import load_dotenv
from menu import load_menu, get_menu

# Carrega variáveis de ambiente
load_dotenv()

# Carrega e valida o menu
try:
    load_menu("menu.json")
    print("Menu carregado com sucesso!")
except (FileNotFoundError, ValueError) as e:
    print(f"ERRO ao carregar menu: {e}")
    exit(1)

# Configurações do bot (com valores padrão)
COMMAND_PREFIX = os.getenv("COMMAND_PREFIX", "!")
MENU_TIMEOUT = float(os.getenv("MENU_TIMEOUT", "30.0"))
SUCCESS_HTTP_CODE = int(os.getenv("SUCCESS_HTTP_CODE", "200"))
MENU_COMMAND_NAME = os.getenv("MENU_COMMAND_NAME", "menu")

# Configuração do bot Discord
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)


@bot.event
async def on_ready():
    """Evento quando o bot está pronto."""
    print(f"Bot conectado como {bot.user}")


@bot.command(name="ping")
async def ping(ctx):
    """Comando para verificar se o bot está online."""
    menu = get_menu()
    response = menu.get_message("ping_response")
    await ctx.reply(response)


@bot.command(name=MENU_COMMAND_NAME)
async def menu(ctx):
    """Comando para exibir o menu interativo."""
    menu_config = get_menu()
    
    # Monta o texto do menu
    menu_title = menu_config.get_message("menu_title")
    menu_items = []
    
    for action_id in menu_config.get_all_action_ids():
        action = menu_config.get_action(action_id)
        if action:
            description, _ = action
            menu_items.append(f"{action_id} - {description}")
    
    menu_text = f"{menu_title}\n" + "\n".join(menu_items)
    await ctx.reply(menu_text)
    
    # Função para validar a resposta do usuário
    def check(m):
        valid_ids = menu_config.get_all_action_ids() + [menu_config.cancel_option]
        return (
            m.author == ctx.author 
            and m.channel == ctx.channel 
            and m.content in valid_ids
        )
    
    try:
        msg = await bot.wait_for("message", timeout=MENU_TIMEOUT, check=check)
        choice = msg.content
        
        # Verifica se é cancelamento
        if menu_config.is_cancel_option(choice):
            cancel_msg = menu_config.get_message("cancel")
            return await ctx.send(cancel_msg)
        
        # Obtém a ação escolhida
        action = menu_config.get_action(choice)
        if not action:
            await ctx.send("Opção inválida.")
            return
        
        description, command_url = action
        
        # Envia mensagem de aguarde
        waiting_msg = menu_config.get_message("waiting", action=description)
        await ctx.send(waiting_msg)
        
        # Executa o comando HTTP
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(command_url) as resp:
                    if resp.status == SUCCESS_HTTP_CODE:
                        success_msg = menu_config.get_message("success", action=description)
                        await ctx.send(success_msg)
                    else:
                        error_msg = menu_config.get_message(
                            "error", 
                            action=description, 
                            status=resp.status
                        )
                        await ctx.send(error_msg)
            except aiohttp.ClientError as e:
                error_msg = f"Erro de conexão ao executar {description}: {str(e)}"
                await ctx.send(error_msg)
    
    except asyncio.TimeoutError:
        timeout_msg = menu_config.get_message(
            "timeout",
            prefix=COMMAND_PREFIX,
            command=MENU_COMMAND_NAME
        )
        await ctx.send(timeout_msg)


# Inicia o bot
discord_token = os.getenv("DISCORD_TOKEN")
if not discord_token:
    print("ERRO: DISCORD_TOKEN não encontrado no arquivo .env")
    exit(1)

bot.run(discord_token)

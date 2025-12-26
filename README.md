# 🤖 PowerBot

Bot do Discord para gerenciamento remoto de servidores e serviços de infraestrutura através de comandos simples e intuitivos.

## 📋 Descrição

O **PowerBot** é uma ferramenta de automação desenvolvida em Python que permite à equipe de DevOps ligar e desligar servidores diretamente pelo Discord. Com um menu interativo, é possível ligar e desligar servidores de homologação e produção sem a necessidade de acessar painéis de controle ou servidores individualmente.

## ✨ Funcionalidades

### Comandos Disponíveis

- **`!ping`**: Verifica se o bot está online e respondendo
- **`!menu`**: Exibe o menu interativo com todas as opções de gerenciamento

### Serviços Gerenciados

O bot permite controlar servidores e serviços de infraestrutura através de requisições HTTP. Você pode configurar quantas ações desejar no arquivo `menu.json`, incluindo:

- Ligar/Desligar servidores em ambientes de homologação
- Ligar/Desligar servidores em ambientes de produção
- Controlar serviços e aplicações remotamente
- Executar qualquer ação que possa ser acionada via API HTTP

## 🚀 Como Usar

1. No canal do Discord onde o bot está presente, digite:
   ```
   !menu
   ```

2. O bot exibirá um menu numerado com todas as opções disponíveis

3. Digite o número correspondente à ação desejada

4. Aguarde a confirmação da operação

5. Para cancelar, digite `99`

> ⏱️ **Atenção**: O menu expira em 30 segundos. Se não houver resposta, será necessário digitar `!menu` novamente.

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**
- **discord.py**: Biblioteca para interação com a API do Discord
- **aiohttp**: Cliente HTTP assíncrono para requisições
- **python-dotenv**: Gerenciamento de variáveis de ambiente

## 📦 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- Conta no Discord
- Bot do Discord criado no [Discord Developer Portal](https://discord.com/developers/applications)

### Passos de Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/pedroaop/PowerBot.git
   cd PowerBot
   ```

2. Crie um ambiente virtual (recomendado):
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure as variáveis de ambiente e o menu:
   ```bash
   # Copie o arquivo de exemplo do .env
   cp .env.example .env
   
   # Edite o .env com suas configurações reais
   # (use seu editor de texto preferido)
   
   # Copie o arquivo de exemplo do menu.json
   cp menu.json.example menu.json
   
   # Edite o menu.json com suas ações e URLs reais
   # (use seu editor de texto preferido)
   ```

5. Execute o bot:
   ```bash
   python main.py
   ```

## ⚙️ Configuração

### Arquivo `.env`

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis. Você pode usar o arquivo `.env.example` como referência:

> **Nota**: O arquivo `.env` não é versionado no Git por questões de segurança. Use `.env.example` como template.

```env
# ============================================
# TOKEN DO DISCORD (OBRIGATÓRIO)
# ============================================
DISCORD_TOKEN=seu_token_aqui

# ============================================
# CONFIGURAÇÕES DO BOT (OPCIONAIS)
# Todas têm valores padrão, então são opcionais
# ============================================

# Prefixo dos comandos (padrão: !)
COMMAND_PREFIX=!

# Timeout do menu em segundos (padrão: 30.0)
MENU_TIMEOUT=30.0

# Código HTTP considerado como sucesso (padrão: 200)
SUCCESS_HTTP_CODE=200

# Opção numérica para cancelar (padrão: 99)
CANCEL_OPTION=99

# Nome do comando do menu (padrão: menu)
MENU_COMMAND_NAME=menu
```

> **Nota**: As URLs dos endpoints **não** ficam mais no `.env`. Elas foram movidas para o arquivo `menu.json` (veja abaixo).

### Arquivo `menu.json`

O arquivo `menu.json` contém todas as ações do menu interativo e as mensagens do bot. Este arquivo deve estar na raiz do projeto.

> **Nota**: O arquivo `menu.json` não é versionado no Git por questões de segurança. Use `menu.json.example` como template e copie para `menu.json` com suas configurações reais.

**Estrutura básica:**

```json
{
  "actions": [
    {
      "id": "1",
      "description": "Ligar Servidor Homologação",
      "command": "https://seu-endpoint.com/ligar"
    },
    {
      "id": "2",
      "description": "Desligar Servidor Homologação",
      "command": "https://seu-endpoint.com/desligar"
    }
  ],
  "cancel_option": "99",
  "messages": {
    "menu_title": "**O que você deseja?**",
    "ping_response": "Pong!",
    "cancel": "Operação cancelada.",
    "waiting": "Aguarde {action}...",
    "success": "Sucesso ao {action}!",
    "error": "Erro ao {action}. Código HTTP: {status}.",
    "timeout": "Tempo esgotado. Por favor, digite `{prefix}{command}` novamente."
  }
}
```

**Campos:**
- `actions`: Array com todas as ações do menu. Cada ação tem:
  - `id`: Identificador numérico usado no menu
  - `description`: Texto exibido no menu
  - `command`: URL completa do endpoint a ser chamado
- `cancel_option`: Valor numérico para cancelar (padrão: "99")
- `messages`: Templates de mensagens com placeholders `{action}`, `{status}`, `{prefix}`, `{command}`

> 💡 **Dica**: Você pode adicionar ou remover ações facilmente editando o `menu.json`, sem precisar modificar o código!

### Como obter o Token do Discord

1. Acesse o [Discord Developer Portal](https://discord.com/developers/applications)
2. Crie uma nova aplicação ou selecione uma existente
3. Vá para a aba "Bot"
4. Copie o token (você pode precisar clicar em "Reset Token" se for a primeira vez)
5. Habilite as "Message Content Intent" em "Privileged Gateway Intents"
6. Convide o bot para seu servidor usando o OAuth2 URL Generator

## 📁 Estrutura do Projeto

```
PowerBot/
├── main.py              # Código principal do bot
├── menu.py              # Módulo para gerenciar o menu interativo
├── menu.json            # Configurações do menu (ações e mensagens) - NÃO VERSIONADO
├── menu.json.example    # Exemplo de configuração do menu
├── requirements.txt     # Dependências do projeto
├── .env                 # Variáveis de ambiente (não versionado)
├── .env.example         # Arquivo de exemplo de configuração
├── .gitignore           # Arquivos ignorados pelo Git
└── README.md           # Este arquivo
```

## 🔒 Segurança

> ⚠️ **IMPORTANTE**: 
> - Nunca compartilhe seu arquivo `.env` ou `menu.json` com dados reais
> - Os arquivos `.env` e `menu.json` já estão no `.gitignore` e não serão versionados
> - Use os arquivos de exemplo (`.env.example` e `menu.json.example`) como referência
> - Use URLs seguras (HTTPS) para todas as requisições
> - Limite as permissões do bot apenas ao necessário
> - Controle quem tem acesso aos comandos do bot no servidor Discord
> - Não commite tokens, senhas, URLs de APIs ou qualquer informação sensível

## 🚀 Deploy em Produção (Linux)

Este guia descreve como realizar o deploy do **PowerBot** em um servidor Linux (Ubuntu), utilizando **PM2** para gerenciar o processo e garantir que o bot reinicie automaticamente após reboots ou falhas.

### Estrutura Esperada no Servidor

Certifique-se de que o projeto esteja organizado no servidor:

```
/home/
└── seu-bot/
    ├── main.py
    ├── requirements.txt
    ├── .env
    └── ...outros arquivos...
```

### 1️⃣ Atualização do Sistema

```bash
sudo apt update
sudo apt upgrade -y
reboot
```

### 2️⃣ Verificar Instalação do Python

```bash
python3 --version
which python3
```

### 3️⃣ Instalar Python, pip e venv

```bash
sudo apt install python3-venv python3 pip -y
```

### 4️⃣ Instalar Dependências do Bot

Navegue até a pasta do bot e instale as dependências:

```bash
cd /home/seu-bot
pip install -r requirements.txt
```

### 5️⃣ Instalar Node.js, NPM e PM2

PM2 será utilizado para rodar o bot em background e reiniciar automaticamente quando necessário:

```bash
sudo apt update
sudo apt install nodejs npm -y

# Verificar instalação
node -v
npm -v

# Instalar PM2 globalmente
sudo npm install pm2 -g
pm2 --version
```

### 6️⃣ Iniciar o Bot com PM2

```bash
pm2 start main.py --interpreter python3 --name powerbot
```

**Comandos úteis:**

Listar processos:
```bash
pm2 list
```

Monitorar em tempo real:
```bash
pm2 monit
```

Ver logs:
```bash
pm2 logs powerbot
```

### 7️⃣ Configurar Inicialização Automática

Para garantir que o bot inicie automaticamente após reinicializações do servidor:

```bash
pm2 startup
pm2 save
```

> 💡 **Dica**: Execute `pm2 startup` e siga as instruções exibidas no terminal. Geralmente será necessário copiar e executar um comando com `sudo`.

### 8️⃣ Comandos de Manutenção

**Parar o bot:**
```bash
pm2 stop powerbot
```

**Iniciar novamente:**
```bash
pm2 start powerbot
```

**Reiniciar:**
```bash
pm2 restart powerbot
```

**Renomear o processo:**
```bash
pm2 rename powerbot novo-nome
```

**Remover do PM2:**
```bash
pm2 delete powerbot
```

**Ver informações detalhadas:**
```bash
pm2 show powerbot
```

**Limpar logs:**
```bash
pm2 flush powerbot
```

### 🔄 Atualizar o Bot em Produção

Quando precisar atualizar o código:

```bash
cd /home/seu-bot
git pull origin main
pip install -r requirements.txt --upgrade
pm2 restart powerbot
```

### ✅ Verificar Status do Bot

```bash
pm2 list
pm2 logs powerbot --lines 50
```

## 🐛 Solução de Problemas

### O bot não responde aos comandos
- Verifique se o bot está online no Discord
- Confirme que o token no arquivo `.env` está correto
- Certifique-se de que a "Message Content Intent" está habilitada

### Erro ao executar ações
- Verifique se as URLs no arquivo `menu.json` estão corretas e acessíveis
- Confirme que os servidores/serviços estão configurados para aceitar as requisições
- Verifique os logs do console para mais detalhes do erro
- Valide se o campo `command` de cada ação no `menu.json` contém uma URL válida

### Menu expira muito rápido
- O timeout padrão é de 30 segundos
- Para alterar, modifique a variável `MENU_TIMEOUT` no arquivo `.env` ou use o valor padrão

### Erro ao carregar menu.json
- Verifique se o arquivo `menu.json` existe na raiz do projeto
- Valide a estrutura JSON do arquivo (use um validador JSON online)
- Certifique-se de que todas as ações têm os campos `id`, `description` e `command`
- Verifique se as URLs nos comandos são válidas (começam com `http://` ou `https://`)

## 📝 Licença

Este projeto está licenciado sob a [Apache License 2.0](LICENSE). O código-fonte é livre e pode ser usado, modificado e distribuído conforme os termos da licença.

> ⚠️ **Aviso de Responsabilidade**: 
> - Os mantenedores deste projeto **não se responsabilizam** pelos serviços, comandos, URLs ou ações configuradas no arquivo `menu.json`
> - É de total responsabilidade do usuário garantir que as URLs e comandos configurados sejam seguros e autorizados
> - O uso deste bot para controlar serviços de infraestrutura é por sua conta e risco
> - Recomendamos revisar cuidadosamente todas as configurações antes de usar em produção

## 👥 Contribuindo

Para contribuir com o projeto:

1. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
2. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
3. Push para a branch (`git push origin feature/MinhaFeature`)
4. Abra um Pull Request

---

Desenvolvido com ❤️ para facilitar o gerenciamento de infraestrutura

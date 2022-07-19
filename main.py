import os
from dotenv import load_dotenv
from bot import bot

def main():
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    
    bot.run(TOKEN)
    

if __name__ == "__main__":
    main()
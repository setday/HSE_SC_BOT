import os

from dotenv import load_dotenv

load_dotenv()

def get_bot_key():
    bot_token = os.getenv("BOT_API_TOKEN")
    
    if bot_token:
        return bot_token
    
    raise ValueError("Bot token not found in .env file")

def get_back_id():
    back_chat_id = os.getenv("BACK_CHAT_ID")

    if back_chat_id:
        return int(back_chat_id)
    
    raise ValueError("Back chat id not found in .env file")
    
def get_vote_id():
    vote_chat_id = os.getenv("VOTE_CHAT_ID")

    if vote_chat_id:
        return int(vote_chat_id)
    
    raise ValueError("Vote chat id not found in .env file")

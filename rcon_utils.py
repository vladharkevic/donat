
from mcrcon import MCRcon
from config import RCON_HOST, RCON_PORT, RCON_PASSWORD

def give_privilege(username, privilege):
    try:
        with MCRcon(RCON_HOST, RCON_PASSWORD, port=RCON_PORT) as mcr:
            command = f"lp user {username} parent set {privilege}"
            response = mcr.command(command)
            return response
    except Exception as e:
        return f"Помилка видачі: {e}"

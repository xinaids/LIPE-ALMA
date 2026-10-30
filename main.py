import sys
import os
import multiprocessing

# Frozen-exe setup: must happen before any other import so that module-level
# code (e.g. logging.basicConfig in identifier.py) uses the right CWD.
# --contents-directory . guarantees sys._MEIPASS == dir of the .exe.
if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)

# Writable runtime directories – safe to create both in dev and when frozen.
os.makedirs("Captures", exist_ok=True)

from src.screens.splash.splash import SplashScreen
from src.screens.players.players import PlayerScreen
from src.screens.teams.teams import TeamsScreen
from src.screens.difficulty.difficulty import DifficultyScreen
from src.screens.game_mode.game_mode import GameMode
from src.globals import variables

if __name__ == "__main__":
    # Required so that multiprocessing child processes (used in loading screen)
    # work correctly inside a frozen Windows executable.
    multiprocessing.freeze_support()

    splash = SplashScreen()
    splash.Show()

    cadastro = PlayerScreen()
    jogadores = cadastro.Show()

    if jogadores:
        while True:                                         # loop de times
            teams = TeamsScreen(jogadores)
            if teams.Show() != "jogar":
                break

            sair_do_app = False
            while True:                                     # loop de dificuldade
                difficulty = DifficultyScreen()
                nivel = difficulty.Show()
                if nivel is None:
                    break                                   # VOLTAR → volta para times

                variables.difficulty_movements = nivel

                while True:                                 # loop de rodadas
                    game_mode = GameMode()
                    result = game_mode.Show()
                    if result == "sair" or result is None:
                        sair_do_app = True
                        break
                    elif result == "aumentar":
                        break                               # volta para dificuldade
                    # "continuar" → mantém no loop de rodadas

                if sair_do_app:
                    break                                   # sai do loop de dificuldade

            if sair_do_app:
                break                                       # sai do loop de times
from src.screens.players.players import PlayerScreen
from src.screens.teams.teams import TeamsScreen
from src.screens.difficulty.difficulty import DifficultyScreen
from src.screens.game_mode.game_mode import GameMode
from src.globals import variables

if __name__ == "__main__":
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
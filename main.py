from src.screens.players.players import PlayerScreen
from src.screens.teams.teams import TeamsScreen
from src.screens.game_mode.game_mode import GameMode

if __name__ == "__main__":
    cadastro = PlayerScreen()
    jogadores = cadastro.Show()

    if jogadores:
        teams = TeamsScreen(jogadores)
        if teams.Show() == "jogar":
            game_mode = GameMode()
            game_mode.Show()
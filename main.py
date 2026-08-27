from src.screens.players.players import PlayerScreen
from src.screens.teams.teams import TeamsScreen
from src.screens.home.home import HomeScreen

if __name__ == "__main__":
    cadastro = PlayerScreen()
    jogadores = cadastro.Show()

    if jogadores:
        teams = TeamsScreen(jogadores)
        if teams.Show() == "jogar":
            home = HomeScreen(jogadores)
            home.Show()
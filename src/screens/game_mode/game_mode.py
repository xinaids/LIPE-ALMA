#!/usr/bin/env python
# coding: utf-8

import pygame
import pygame_gui
from src.screens.players import players
from src.screens.loading import loading
from src.screens.game.condition_game import ConditionGame
from src.screens.game.sequence_game import SequenceGame
from src.constants.constants import DEVELOP_MODE
from src.screens.dialog.dialog import DialogScreen
from src.constants.dialog import *
from src.globals import variables

class GameMode:
    def __init__(self):
        self.window_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        
        self.background = pygame.image.load("images/background.jpg")
        self.window_surface.blit(self.background, (0, 0))
        self.manager = pygame_gui.UIManager(
            (self.window_surface.get_width(), self.window_surface.get_height()),
            "src/styles/style.json",
        )

        self.player_screen = players.PlayerScreen()
        self.dialog_screen = DialogScreen()

    def Show(self):
        if not variables.Initial_Game_Dialog_Showed:
            self.dialog_screen.Show(*pygame.display.get_window_size(), DIALOG_START_GAME)
            variables.Initial_Game_Dialog_Showed = True

        self.game = SequenceGame()

        if not DEVELOP_MODE and not variables.Is_Traninig_Realized:
            self.loading = loading.Loading(self.window_surface, self.background)
            self.loading.Show()

        self.dialog_screen.Show(*pygame.display.get_window_size(), DIALOG_SEQUENCE)
        result = self.game.start(*pygame.display.get_window_size())
        pygame.event.clear()
        return result
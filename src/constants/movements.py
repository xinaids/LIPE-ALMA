#!/usr/bin/env python
# coding: utf-8

# Constantes que definem os movimentos
LEFT_HAND = 1
RIGHT_HAND = 2
OPEN_ARMS = 3
LIGHT_SQUAT = 4

MOVEMENTS = (LEFT_HAND, RIGHT_HAND, OPEN_ARMS, LIGHT_SQUAT)

MOVEMENTS_ORDER = {
    LEFT_HAND: "Braço Esquerdo",
    RIGHT_HAND: "Braço Direito",
    OPEN_ARMS: "Abra os Braços",
    LIGHT_SQUAT: "Dobre os Joelhos",
}

MOVEMENTS_MESSAGE = {
    LEFT_HAND: "Braço Esquerdo",
    RIGHT_HAND: "Braço Direito",
    OPEN_ARMS: "Braços Abertos",
    LIGHT_SQUAT: "Joelhos Dobrados",
}

MOVEMENTS_IMAGES = {
    LEFT_HAND: "left_hand.png",
    RIGHT_HAND: "right_hand.png",
    OPEN_ARMS: "open_arms.png",   # placeholder — substituir pela imagem definitiva
    LIGHT_SQUAT: "crouch.png",
}

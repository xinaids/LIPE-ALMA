#!/usr/bin/env python
# coding: utf-8

import src.constants.movements as mov
import src.poses.poses as poses
import random
import cv2
from cv2.typing import MatLike
import time
import os
from src.constants.constants import DIRECTORY_LOGS_IMAGE
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    filename="execucoes.log",
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class Identifier(poses.Poses):
    def __init__(self, list_valid_movements: list[int]):

        self.MOVEMENTS_METHODS = [
            self.hand_left,
            self.hand_right,
            self.open_arms_identifier,
            self.crouch_identifier,
        ]

        self.body_unit = 0.0
        self.standing_mid_y = 0.0

        # fracao da "unidade de corpo" usada como margem para agachar.
        # valor menor (0.20) porque idosos nao precisam descer muito.
        self.CROUCH_FACTOR = 0.20

        # tempo minimo (em segundos) entre deteccoes — maior para idosos
        # que nao alternam movimentos rapidamente.
        self.DETECTION_COOLDOWN = 1.2
        self._last_detection_time = time.time()

        self._open_arms_confirm_count = 0
        self._crouch_confirm_count = 0
        # mais frames necessarios = menos falsos positivos para movimentos lentos.
        self.CONFIRM_FRAMES_REQUIRED = 5

        super().__init__()

    def __str__(self):
        pass

    def _cooldown_ok(self) -> bool:
        """Retorna True se ja passou tempo suficiente desde a ultima deteccao."""
        return (time.time() - self._last_detection_time) >= self.DETECTION_COOLDOWN

    def _marcar_deteccao(self):
        """Registra o instante de uma deteccao (para o cooldown)."""
        self._last_detection_time = time.time()
        self._open_arms_confirm_count = 0
        self._crouch_confirm_count = 0

    def arm_detection(self):
        """Bloqueia detecção por DETECTION_COOLDOWN após o fim da fase de demo.
        Chame sempre que is_showing_movements transitar de True para False."""
        self._last_detection_time = time.time()
        self._open_arms_confirm_count = 0
        self._crouch_confirm_count = 0

    def process_image(self, img: MatLike):

        self.copy_image = img.copy()
        result_processing = self.pose.process(self.copy_image)

        self.points = result_processing.pose_landmarks

        if self.points:
            self.mpDraw.draw_landmarks(
                self.copy_image, self.points, self.mpPose.POSE_CONNECTIONS
            )

            self.handRX = float(
                self.points.landmark[self.mpPose.PoseLandmark.RIGHT_WRIST].x
            )
            self.handRY = float(
                self.points.landmark[self.mpPose.PoseLandmark.RIGHT_WRIST].y
            )
            self.handLX = float(
                self.points.landmark[self.mpPose.PoseLandmark.LEFT_WRIST].x
            )
            self.handLY = float(
                self.points.landmark[self.mpPose.PoseLandmark.LEFT_WRIST].y
            )
            self.noseX = float(self.points.landmark[self.mpPose.PoseLandmark.NOSE].x)
            self.noseY = float(self.points.landmark[self.mpPose.PoseLandmark.NOSE].y)
            self.shoulderRY = float(
                self.points.landmark[self.mpPose.PoseLandmark.RIGHT_SHOULDER].y
            )
            self.shoulderLY = float(
                self.points.landmark[self.mpPose.PoseLandmark.LEFT_SHOULDER].y
            )

    def hand_left(self) -> bool:
        # lembrando: no MediaPipe, y MENOR = mais alto na tela.
        # a regra e simplesmente: mao esquerda acima do nariz e a direita nao.
        # isso e invariante ao tamanho do aluno (compara o aluno com ele mesmo).
        left_up = self.handLY < self.noseY
        right_up = self.handRY < self.noseY

        return left_up and not right_up

    def hand_right(self) -> bool:
        left_up = self.handLY < self.noseY
        right_up = self.handRY < self.noseY

        return right_up and not left_up

    def open_arms_identifier(self) -> bool:
        shoulder_y = (self.shoulderRY + self.shoulderLY) / 2
        arms_wide = abs(self.handRX - self.handLX) > 0.45
        arms_level = (self.handLY < shoulder_y + 0.05) and (self.handRY < shoulder_y + 0.05)
        if arms_wide and arms_level:
            self._open_arms_confirm_count += 1
            self._crouch_confirm_count = 0
            return self._open_arms_confirm_count >= self.CONFIRM_FRAMES_REQUIRED
        else:
            self._open_arms_confirm_count = 0
            return False

    def crouch_identifier(self) -> bool:
        actual_mid_y = (self.shoulderRY + self.shoulderLY) / 2
        upper_bound = self.standing_mid_y + (self.body_unit * self.CROUCH_FACTOR)
        if actual_mid_y > upper_bound:
            self._crouch_confirm_count += 1
            self._open_arms_confirm_count = 0
            return self._crouch_confirm_count >= self.CONFIRM_FRAMES_REQUIRED
        else:
            self._crouch_confirm_count = 0
            return False

    def is_correct_positioned(self) -> bool:
        if self.shoulderRY == 0 or self.shoulderLY == 0:
            return False

        mid_shoulders = (self.shoulderRY + self.shoulderLY) / 2

        if (mid_shoulders > 0.9) or (mid_shoulders < 0.1):
            return False

        self.standing_mid_y = mid_shoulders

        # distancia nariz <-> ombros: usada como escala do corpo do aluno.
        # evita que o limiar de pular/agachar dependa do tamanho na tela.
        self.body_unit = abs(mid_shoulders - self.noseY)

        return True

    def sort_movements(self, list_movements: list[int], qtd: int = 1):
        self.list_commands = []
        for _ in range(qtd):
            self.list_commands.append(random.choice(list_movements))

        self.reset_seq_command()

    def identify(self) -> bool:
        match self.command:
            case mov.LEFT_HAND:
                return self.hand_left()

            case mov.RIGHT_HAND:
                return self.hand_right()

            case mov.OPEN_ARMS:
                return self.open_arms_identifier()

            case mov.LIGHT_SQUAT:
                return self.crouch_identifier()

    def identify_list_movements(self, serial_id: int, player_name: str = "") -> bool | None:
        self.identified_movement = None
        if self.command is None:
            return None

        # ── cooldown: ignora frames ate passar o tempo minimo ──
        if not self._cooldown_ok():
            return None

        if self.body_unit < 0.05:
            return None

        if self.MOVEMENTS_METHODS[self.command - 1]():
            self.identified_movement = self.command
            self._marcar_deteccao()
            self.save_log(
                mov.MOVEMENTS_ORDER[self.command], mov.MOVEMENTS_ORDER[self.command], serial_id, player_name
            )
            return True

        for i, fn in enumerate(self.MOVEMENTS_METHODS):
            if fn():
                self.identified_movement = i + 1
                self._marcar_deteccao()
                self.save_log(
                    mov.MOVEMENTS_ORDER[self.command],
                    mov.MOVEMENTS_ORDER[i + 1],
                    serial_id,
                    player_name,
                )
                return False

        return None

    def save_log(self, mov_command: str, move_identified: str, serial_id: int, player_name: str = ""):
        timestamp = time.time()

        logging.info(
            f"{serial_id} - {str(timestamp)}, Jogador: {player_name}, Movimento Esperado: {mov_command}, Retornado: {move_identified}, handRX: {self.handRX}, handRY: {self.handRY}, handLX: {self.handLX}, handLY: {self.handLY}, noseX: {self.noseX}, noseY: {self.noseY}, shoulderRY: {self.shoulderRY}, shoulderLY: {self.shoulderLY}, standing_mid_y: {self.standing_mid_y}, body_unit: {self.body_unit}"
        )

        Path(DIRECTORY_LOGS_IMAGE).mkdir(exist_ok=True)

        cv2.imwrite(
            DIRECTORY_LOGS_IMAGE
            + os.sep
            + "#"
            + str(serial_id)
            + "_"
            + str(timestamp)
            + ".jpg",
            self.copy_image,
        )

    def has_next_movement(self) -> bool:
        return self.seq_command < self.qtd_movements() - 1

    def qtd_movements(self) -> int:
        return len(self.list_commands)

    def reset_seq_command(self):
        self.seq_command = 0
        if self.list_commands:  # so acessa se nao for vazia
            self.command = self.list_commands[self.seq_command]
        else:
            self.command = None

    def command_at(self, pos: int):
        if 0 <= pos < len(self.list_commands):
            return self.list_commands[pos]
        return None  # evita IndexError

    def next_movement(self):
        self.seq_command += 1
        self.command = self.list_commands[self.seq_command]
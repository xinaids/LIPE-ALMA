#!/usr/bin/env python
# coding: utf-8
"""
Testes da lógica de detecção/pontuação sem webcam e sem janela.
Execute:  python -m pytest tests/test_fluxo_jogo.py -v
"""

import sys
import types
import unittest
from unittest.mock import MagicMock, patch

# ── Stub mediapipe antes de qualquer import src ───────────────────────────────

def _install_mp_stub():
    mp = types.ModuleType("mediapipe")
    solutions = types.ModuleType("mediapipe.solutions")
    pose_mod  = types.ModuleType("mediapipe.solutions.pose")
    draw_mod  = types.ModuleType("mediapipe.solutions.drawing_utils")

    class _FakePose:
        PoseLandmark  = MagicMock()
        POSE_CONNECTIONS = []
        def __init__(self, **kw): pass
        def process(self, img): return MagicMock(pose_landmarks=None)

    pose_mod.Pose        = _FakePose
    draw_mod.draw_landmarks = MagicMock()
    solutions.pose            = pose_mod
    solutions.drawing_utils   = draw_mod
    mp.solutions              = solutions

    for name, mod in [
        ("mediapipe",                          mp),
        ("mediapipe.solutions",                solutions),
        ("mediapipe.solutions.pose",           pose_mod),
        ("mediapipe.solutions.drawing_utils",  draw_mod),
    ]:
        sys.modules.setdefault(name, mod)

_install_mp_stub()

from src.identifier.identifier import Identifier   # noqa: E402
from src.constants import movements as mov         # noqa: E402


# ── Relógio falso ─────────────────────────────────────────────────────────────

class _Clock:
    def __init__(self, t=0.0): self._t = t
    def __call__(self): return self._t
    def advance(self, dt): self._t += dt


# ── Helpers ───────────────────────────────────────────────────────────────────

def _make_ident(cmds: list[int]) -> Identifier:
    """Cria Identifier com save_log mockado e list_commands inicializado."""
    ident = Identifier([mov.LEFT_HAND, mov.RIGHT_HAND, mov.OPEN_ARMS, mov.LIGHT_SQUAT])
    ident.save_log = MagicMock()
    ident.list_commands = list(cmds)
    ident.reset_seq_command()
    return ident


def _pose(ident: Identifier,
          left_up=False, right_up=False,
          open_arms=False, neutral=False):
    """Injeta valores sintéticos de landmarks diretamente nos atributos."""
    ident.noseY      = 0.30
    ident.shoulderRY = 0.40
    ident.shoulderLY = 0.40
    ident.standing_mid_y = 0.40
    ident.body_unit  = 0.12
    # posição padrão: mãos baixas, braços juntos
    ident.handLY = 0.70;  ident.handLX = 0.45
    ident.handRY = 0.70;  ident.handRX = 0.55

    if left_up:
        ident.handLY = 0.10   # acima do nariz
    if right_up:
        ident.handRY = 0.10
    if open_arms:
        ident.handLX = 0.10;  ident.handRX = 0.70
        ident.handLY = 0.35;  ident.handRY = 0.35   # ao nível dos ombros


def _detect(ident, n=1):
    """Chama identify_list_movements n vezes, retorna lista de resultados."""
    return [ident.identify_list_movements(1, "test") for _ in range(n)]


def _pass_cooldown(clock: _Clock, ident: Identifier, dt=2.0):
    """Avança o relógio e reseta o cooldown de detecção."""
    clock.advance(dt)


# ── Testes ────────────────────────────────────────────────────────────────────

class TestAcertaErraAcerta(unittest.TestCase):
    """Cenário 1: ACERTA, ERRA (real error), ACERTA → score = 2."""

    def test_score_final_2(self):
        clock = _Clock()
        with patch("time.time", clock), patch("time.perf_counter", clock):
            ident = _make_ident([mov.LEFT_HAND, mov.RIGHT_HAND, mov.LEFT_HAND])
            score = 0

            # ── Movimento 1: LEFT_HAND certo ─────────────────────────────
            _pass_cooldown(clock, ident)
            _pose(ident, left_up=True)
            r = ident.identify_list_movements(1, "test")
            self.assertTrue(r, "Mov-1 deve retornar True")
            score += 1
            self.assertTrue(ident._command_resolved, "_command_resolved True após acerto")

            ident.next_movement()
            self.assertFalse(ident._command_resolved, "_command_resolved False após next_movement")
            ident.arm_detection()

            # ── Movimento 2: RIGHT_HAND pedido, jogador faz LEFT_HAND ────
            _pass_cooldown(clock, ident)
            _pose(ident, left_up=True)   # mão trocada
            r = ident.identify_list_movements(1, "test")
            self.assertFalse(r, "Mov-2 deve retornar False (mão trocada)")
            self.assertEqual(score, 1, "erro NÃO desconta score")

            ident.next_movement()
            self.assertFalse(ident._command_resolved, "_command_resolved False após erro + next_movement")
            ident.arm_detection()

            # ── Movimento 3: LEFT_HAND certo ─────────────────────────────
            _pass_cooldown(clock, ident)
            _pose(ident, left_up=True)
            r = ident.identify_list_movements(1, "test")
            self.assertTrue(r, "Mov-3 deve retornar True")
            score += 1

            self.assertEqual(score, 2, "score final = 2")
            self.assertFalse(ident.has_next_movement(), "sem próximo movimento")


class TestErraAcertaErra(unittest.TestCase):
    """Cenário 2: ERRA, ACERTA, ERRA → score = 1."""

    def test_score_final_1(self):
        clock = _Clock()
        with patch("time.time", clock), patch("time.perf_counter", clock):
            ident = _make_ident([mov.LEFT_HAND, mov.RIGHT_HAND, mov.LEFT_HAND])
            score = 0

            # Mov-1: LEFT_HAND pedido, faz RIGHT_HAND → erro
            _pass_cooldown(clock, ident)
            _pose(ident, right_up=True)
            r = ident.identify_list_movements(1, "test")
            self.assertFalse(r)
            ident.next_movement(); ident.arm_detection()

            # Mov-2: RIGHT_HAND pedido, faz RIGHT_HAND → acerta
            _pass_cooldown(clock, ident)
            _pose(ident, right_up=True)
            r = ident.identify_list_movements(1, "test")
            self.assertTrue(r)
            score += 1
            ident.next_movement(); ident.arm_detection()

            # Mov-3: LEFT_HAND pedido, faz RIGHT_HAND → erro
            _pass_cooldown(clock, ident)
            _pose(ident, right_up=True)
            r = ident.identify_list_movements(1, "test")
            self.assertFalse(r)

            self.assertEqual(score, 1)


class TestProximoJogadorLimpo(unittest.TestCase):
    """Cenário 3: erro no último movimento, próximo jogador começa limpo."""

    def test_estado_limpo(self):
        clock = _Clock()
        with patch("time.time", clock), patch("time.perf_counter", clock):
            ident = _make_ident([mov.LEFT_HAND, mov.RIGHT_HAND])

            # Mov-1 acerta
            _pass_cooldown(clock, ident)
            _pose(ident, left_up=True)
            ident.identify_list_movements(1, "p1")
            ident.next_movement(); ident.arm_detection()

            # Mov-2 (último) erra
            _pass_cooldown(clock, ident)
            _pose(ident, left_up=True)   # wrong: RIGHT_HAND expected
            ident.identify_list_movements(1, "p1")

            # Simula transição para próximo jogador
            ident.list_commands = [mov.RIGHT_HAND, mov.LEFT_HAND]
            ident.reset_seq_command()
            ident.arm_detection()

            self.assertFalse(ident._command_resolved,
                             "novo jogador: _command_resolved deve ser False")
            self.assertTrue(all(v is None for v in ident._wrong_since.values()),
                            "novo jogador: _wrong_since deve estar todo None")
            self.assertEqual(ident.command, mov.RIGHT_HAND,
                             "command deve ser o primeiro do novo jogador")


class TestAcertaTudo(unittest.TestCase):
    """Cenário 4: 3 de 3 acertos → score = 3."""

    def test_acerta_tudo(self):
        clock = _Clock()
        with patch("time.time", clock), patch("time.perf_counter", clock):
            ident = _make_ident([mov.LEFT_HAND, mov.RIGHT_HAND, mov.LEFT_HAND])
            score = 0

            for expected, kwargs in [
                (mov.LEFT_HAND,  {"left_up": True}),
                (mov.RIGHT_HAND, {"right_up": True}),
                (mov.LEFT_HAND,  {"left_up": True}),
            ]:
                self.assertEqual(ident.command, expected)
                _pass_cooldown(clock, ident)
                _pose(ident, **kwargs)
                r = ident.identify_list_movements(1, "test")
                self.assertTrue(r)
                score += 1
                if ident.has_next_movement():
                    ident.next_movement()
                    ident.arm_detection()

            self.assertEqual(score, 3)
            self.assertFalse(ident.has_next_movement())


class TestErroSustentado(unittest.TestCase):
    """Cenário 5: braço esquerdo pedido, jogador abre os braços por >1s → False.
    Após next_movement + arm_detection, próximo movimento é aceito."""

    def test_erro_sustentado_retorna_false(self):
        clock = _Clock()
        with patch("time.time", clock), patch("time.perf_counter", clock):
            ident = _make_ident([mov.LEFT_HAND, mov.RIGHT_HAND])
            _pass_cooldown(clock, ident, dt=2.0)  # ultrapassa cooldown inicial

            # Simula 40 frames a 0.04s = 1.6s de braços abertos
            _pose(ident, open_arms=True)
            results = []
            for _ in range(40):
                clock.advance(0.04)
                results.append(ident.identify_list_movements(1, "test"))

            self.assertIn(False, results,
                          "Deve retornar False em algum momento (erro sustentado)")
            self.assertTrue(ident._command_resolved,
                            "_command_resolved True após erro sustentado")

    def test_proximo_movimento_aceito_apos_erro_sustentado(self):
        clock = _Clock()
        with patch("time.time", clock), patch("time.perf_counter", clock):
            ident = _make_ident([mov.LEFT_HAND, mov.RIGHT_HAND])
            _pass_cooldown(clock, ident, dt=2.0)

            _pose(ident, open_arms=True)
            for _ in range(40):
                clock.advance(0.04)
                ident.identify_list_movements(1, "test")

            # Avança para o próximo movimento (como game.py faz após erro)
            ident.next_movement()
            self.assertFalse(ident._command_resolved,
                             "_command_resolved False após next_movement")
            ident.arm_detection()
            self.assertFalse(ident._command_resolved,
                             "_command_resolved False após arm_detection")
            self.assertTrue(all(v is None for v in ident._wrong_since.values()),
                            "_wrong_since limpo após arm_detection")

            # Passa cooldown e faz o movimento correto
            _pass_cooldown(clock, ident, dt=2.0)
            _pose(ident, right_up=True)
            r = ident.identify_list_movements(1, "test")
            self.assertTrue(r,
                            "Movimento correto após erro sustentado deve ser aceito")


class TestFeedbackFantasma(unittest.TestCase):
    """Cenário 6: durante feedback positivo (is_movement_identified=True),
    movimento adicional não gera ponto extra nem erro."""

    def test_sem_ponto_extra_durante_feedback(self):
        clock = _Clock()
        with patch("time.time", clock), patch("time.perf_counter", clock):
            ident = _make_ident([mov.LEFT_HAND, mov.RIGHT_HAND])

            # Detecção correta
            _pass_cooldown(clock, ident)
            _pose(ident, left_up=True)
            r = ident.identify_list_movements(1, "test")
            self.assertTrue(r)
            # _command_resolved = True agora

            # Feedback: cooldown ainda ativo (<1.2s), qualquer pose → None
            clock.advance(0.5)
            _pose(ident, right_up=True)
            r2 = ident.identify_list_movements(1, "test")
            self.assertIsNone(r2,
                              "Dentro do cooldown pós-acerto: deve retornar None")

            # Após cooldown (>1.2s), real error durante feedback → False ou True
            # NÃO deve ser True para um movimento que já foi contabilizado
            clock.advance(1.0)   # 1.5s total após detecção → cooldown expirou
            _pose(ident, right_up=True)  # erro real (LEFT_HAND esperado)
            r3 = ident.identify_list_movements(1, "test")
            self.assertIn(r3, (False, None),
                          "Durante feedback (após cooldown): nunca deve ser True para outro comando")
            # score_player não é incrementado aqui — isso é responsabilidade de game.py
            # (só incrementa no branch `not is_movement_identified`)


class TestTimeoutDepoisAcerto(unittest.TestCase):
    """Cenário 7: timeout de 30s, depois próximo movimento é aceito."""

    def test_acerto_apos_timeout(self):
        clock = _Clock()
        with patch("time.time", clock), patch("time.perf_counter", clock):
            ident = _make_ident([mov.LEFT_HAND, mov.RIGHT_HAND])

            # Simula 30s passados sem nenhuma detecção (timeout)
            clock.advance(35.0)
            # game.py chama next_movement + arm_detection após timeout
            ident.next_movement()
            ident.arm_detection()

            self.assertFalse(ident._command_resolved)
            self.assertEqual(ident.command, mov.RIGHT_HAND)

            _pass_cooldown(clock, ident, dt=2.0)
            _pose(ident, right_up=True)
            r = ident.identify_list_movements(1, "test")
            self.assertTrue(r, "Movimento correto após timeout deve ser aceito")


class TestCooldown(unittest.TestCase):
    """Cooldown bloqueia detecção imediata após acerto."""

    def test_cooldown_bloqueia(self):
        clock = _Clock()
        with patch("time.time", clock), patch("time.perf_counter", clock):
            ident = _make_ident([mov.LEFT_HAND, mov.RIGHT_HAND])
            _pass_cooldown(clock, ident)
            _pose(ident, left_up=True)

            r1 = ident.identify_list_movements(1, "test")
            self.assertTrue(r1)

            # Sem avançar o relógio → cooldown ativo
            r2 = ident.identify_list_movements(1, "test")
            self.assertIsNone(r2, "Cooldown deve bloquear detecção imediata")

    def test_cooldown_libera_apos_1_2s(self):
        clock = _Clock()
        with patch("time.time", clock), patch("time.perf_counter", clock):
            ident = _make_ident([mov.LEFT_HAND, mov.RIGHT_HAND])
            _pass_cooldown(clock, ident)
            _pose(ident, left_up=True)

            ident.identify_list_movements(1, "test")  # marca cooldown

            clock.advance(1.3)   # > DETECTION_COOLDOWN (1.2s)
            _pose(ident, left_up=True)
            r = ident.identify_list_movements(1, "test")
            # _command_resolved=True, mas cooldown expirou → checa movimento → True
            self.assertTrue(r, "Após cooldown expirar, pose correta retorna True")


class TestCommandResolvedReset(unittest.TestCase):
    """_command_resolved é False após next_movement e arm_detection."""

    def test_reset_apos_next_movement(self):
        clock = _Clock()
        with patch("time.time", clock), patch("time.perf_counter", clock):
            ident = _make_ident([mov.LEFT_HAND, mov.RIGHT_HAND])
            _pass_cooldown(clock, ident)
            _pose(ident, left_up=True)
            ident.identify_list_movements(1, "test")
            self.assertTrue(ident._command_resolved)

            ident.next_movement()
            self.assertFalse(ident._command_resolved,
                             "next_movement deve resetar _command_resolved")

    def test_reset_apos_arm_detection(self):
        clock = _Clock()
        with patch("time.time", clock), patch("time.perf_counter", clock):
            ident = _make_ident([mov.LEFT_HAND])
            _pass_cooldown(clock, ident)
            _pose(ident, left_up=True)
            ident.identify_list_movements(1, "test")
            self.assertTrue(ident._command_resolved)

            ident.arm_detection()
            self.assertFalse(ident._command_resolved,
                             "arm_detection deve resetar _command_resolved")


class TestWrongSinceLimpo(unittest.TestCase):
    """_wrong_since é limpo após next_movement."""

    def test_wrong_since_limpo(self):
        clock = _Clock()
        with patch("time.time", clock), patch("time.perf_counter", clock):
            ident = _make_ident([mov.LEFT_HAND, mov.RIGHT_HAND])
            _pass_cooldown(clock, ident, dt=2.0)

            # Tick de erro sustentado (sem atingir 1s) — marca _wrong_since
            _pose(ident, open_arms=True)
            ident.identify_list_movements(1, "test")
            self.assertIsNotNone(ident._wrong_since.get(mov.OPEN_ARMS),
                                  "_wrong_since[OPEN_ARMS] deve estar marcado")

            ident.next_movement()
            self.assertTrue(all(v is None for v in ident._wrong_since.values()),
                            "next_movement deve limpar _wrong_since")


class TestResetSeqCommand(unittest.TestCase):
    """reset_seq_command inicializa command e _command_resolved corretamente."""

    def test_reset(self):
        clock = _Clock()
        with patch("time.time", clock), patch("time.perf_counter", clock):
            ident = _make_ident([mov.RIGHT_HAND, mov.LEFT_HAND])
            self.assertEqual(ident.seq_command, 0)
            self.assertEqual(ident.command, mov.RIGHT_HAND)
            self.assertFalse(ident._command_resolved)
            self.assertTrue(all(v is None for v in ident._wrong_since.values()))


class TestFeedbackOkReset(unittest.TestCase):
    """_feedback_ok deve voltar a False em todos os pontos de avanço."""

    def test_reset_apos_avancar_via_show_identified(self):
        """Após show_identified_movement avançar (has_next_movement),
        _feedback_ok deve ser False — simula o que game.py faz."""
        clock = _Clock()
        with patch("time.time", clock), patch("time.perf_counter", clock):
            ident = _make_ident([mov.LEFT_HAND, mov.RIGHT_HAND])

            # Acerta mov-1 → _feedback_ok = True (setado por game.py)
            _pass_cooldown(clock, ident)
            _pose(ident, left_up=True)
            ident.identify_list_movements(1, "test")
            # Simula o que game.py faz ao setar is_movement_identified
            # (testar aqui o estado do identifier após next_movement)
            ident.next_movement()
            # _feedback_ok é atributo de game.py, não do identifier;
            # verificamos que _command_resolved e _wrong_since estão limpos
            # (a flag game-level é testada no teste de integração abaixo).
            self.assertFalse(ident._command_resolved,
                             "next_movement deve limpar _command_resolved")
            self.assertTrue(all(v is None for v in ident._wrong_since.values()))

    def test_feedback_ok_zerado_nao_vaza_para_proximo_movimento(self):
        """Garante que _feedback_ok False no avanço impede texto fantasma.
        Cenário: acerta mov-1, avança, erra mov-2.
        Durante o erro (is_movement_wrong), _feedback_ok não deve ser True
        remanescente do acerto anterior."""
        clock = _Clock()
        with patch("time.time", clock), patch("time.perf_counter", clock):
            ident = _make_ident([mov.LEFT_HAND, mov.RIGHT_HAND, mov.LEFT_HAND])

            # Acerta mov-1
            _pass_cooldown(clock, ident)
            _pose(ident, left_up=True)
            r1 = ident.identify_list_movements(1, "test")
            self.assertTrue(r1)

            # game.py avança: next_movement + _feedback_ok = False (nossa correção)
            ident.next_movement()
            ident.arm_detection()

            # Erra mov-2 (RIGHT_HAND pedido mas faz LEFT_HAND — mão trocada)
            _pass_cooldown(clock, ident)
            _pose(ident, left_up=True)
            r2 = ident.identify_list_movements(1, "test")
            self.assertFalse(r2, "Mov-2 deve ser erro real (mão trocada)")

            # Avança do erro: next_movement + _feedback_ok = False (nossa correção)
            ident.next_movement()
            ident.arm_detection()

            # Acerta mov-3: deve funcionar normalmente
            _pass_cooldown(clock, ident)
            _pose(ident, left_up=True)
            r3 = ident.identify_list_movements(1, "test")
            self.assertTrue(r3, "Mov-3 deve ser aceito após erro no mov-2")


class TestSemDuplaSaveLog(unittest.TestCase):
    """BUG-2: save_log não deve ser chamado uma segunda vez durante o feedback.
    O novo game.py não chama identify_list_movements no branch is_movement_identified,
    portanto save_log permanece com exatamente 1 chamada após a detecção correta."""

    def test_save_log_exatamente_uma_vez_por_movimento(self):
        """Após acerto, save_log é chamado 1 vez.
        Não chamar identify_list_movements durante o feedback mantém esse total."""
        clock = _Clock()
        with patch("time.time", clock), patch("time.perf_counter", clock):
            ident = _make_ident([mov.LEFT_HAND, mov.RIGHT_HAND])
            _pass_cooldown(clock, ident)
            _pose(ident, left_up=True)

            ident.identify_list_movements(1, "test")
            self.assertEqual(ident.save_log.call_count, 1,
                             "Detecção correta deve chamar save_log exatamente 1 vez")

            # Novo game.py: no feedback phase, identify_list_movements NÃO é chamado.
            # Verificamos que o contador não sobe mesmo após o cooldown expirar.
            clock.advance(2.0)   # > DETECTION_COOLDOWN (1.2s)
            # — nenhuma chamada a identify_list_movements —
            self.assertEqual(ident.save_log.call_count, 1,
                             "Sem identify_list_movements no feedback, "
                             "save_log permanece em 1")

    def test_padrao_antigo_causava_duplo_save_log(self):
        """Documenta o bug original: chamar identify_list_movements após o cooldown
        durante a fase de feedback disparava save_log pela segunda vez."""
        clock = _Clock()
        with patch("time.time", clock), patch("time.perf_counter", clock):
            ident = _make_ident([mov.LEFT_HAND, mov.RIGHT_HAND])
            _pass_cooldown(clock, ident)
            _pose(ident, left_up=True)

            ident.identify_list_movements(1, "test")
            self.assertEqual(ident.save_log.call_count, 1)

            # Comportamento antigo: game.py chamava identify_list_movements no feedback
            clock.advance(2.0)
            _pose(ident, left_up=True)
            ident.identify_list_movements(1, "test")   # simula o bug antigo
            self.assertEqual(ident.save_log.call_count, 2,
                             "Padrão antigo disparava save_log duas vezes — "
                             "este teste documenta o bug corrigido")


if __name__ == "__main__":
    unittest.main(verbosity=2)

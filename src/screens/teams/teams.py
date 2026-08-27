import pygame
from src.datatypes.player import Player

pygame.init()


class TeamsScreen:
    def __init__(self, jogadores: list[Player], largura: int = 1920, altura: int = 1080):
        pygame.init()
        self.largura = largura
        self.altura = altura
        self.time_a = [p for i, p in enumerate(jogadores) if i % 2 == 0]
        self.time_b = [p for i, p in enumerate(jogadores) if i % 2 == 1]

    def Show(self) -> str:
        tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("Times")

        try:
            fundo = pygame.image.load("images/lipe2.0.png").convert()
            fundo = pygame.transform.scale(fundo, (self.largura, self.altura))
        except Exception:
            fundo = None

        fonte_time = pygame.font.Font(None, 72)
        fonte_nome = pygame.font.Font(None, 52)
        fonte_btn  = pygame.font.Font(None, 64)

        BRANCO    = (255, 255, 255)
        VM_PAINEL = ( 90,  15,  15)
        VM_BORDA  = (220,  60,  60)
        AZ_PAINEL = ( 15,  15,  90)
        AZ_BORDA  = ( 60,  60, 220)

        margem  = 50
        gap     = 20
        pw      = (self.largura - 2 * margem - gap) // 2
        py      = 80
        ph      = self.altura - py - 160
        panel_a = pygame.Rect(margem,            py, pw, ph)
        panel_b = pygame.Rect(margem + pw + gap, py, pw, ph)

        btn_total_w = 400 + 40 + 200
        btn_x0    = self.largura // 2 - btn_total_w // 2
        btn_y     = self.altura - 120
        btn_jogar = pygame.Rect(btn_x0,              btn_y, 400, 80)
        btn_sair  = pygame.Rect(btn_x0 + 400 + 40,  btn_y, 200, 80)

        clock     = pygame.time.Clock()
        rodando   = True
        resultado = "sair"

        while rodando:
            mouse = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    rodando = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    rodando = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if btn_jogar.collidepoint(mouse):
                        resultado = "jogar"
                        rodando = False
                    elif btn_sair.collidepoint(mouse):
                        resultado = "sair"
                        rodando = False

            if fundo:
                tela.blit(fundo, (0, 0))
            else:
                tela.fill((20, 20, 30))

            overlay = pygame.Surface((self.largura, self.altura))
            overlay.set_alpha(150)
            overlay.fill((0, 0, 0))
            tela.blit(overlay, (0, 0))

            for panel, cor_fundo, cor_borda, time_label, jogadores in (
                (panel_a, VM_PAINEL, VM_BORDA, "TIME A", self.time_a),
                (panel_b, AZ_PAINEL, AZ_BORDA, "TIME B", self.time_b),
            ):
                pygame.draw.rect(tela, cor_fundo, panel, border_radius=16)
                pygame.draw.rect(tela, cor_borda,  panel, 4, border_radius=16)

                titulo = fonte_time.render(time_label, True, cor_borda)
                tela.blit(titulo, (panel.x + (panel.w - titulo.get_width()) // 2, panel.y + 20))

                y = panel.y + 110
                for p in jogadores:
                    surf = fonte_nome.render(p.Name, True, BRANCO)
                    tela.blit(surf, (panel.x + 30, y))
                    y += 70

            cor_jogar = (0, 220, 0) if btn_jogar.collidepoint(mouse) else (0, 160, 0)
            cor_sair  = (220,  0, 0) if btn_sair.collidepoint(mouse)  else (160,  0, 0)
            pygame.draw.rect(tela, cor_jogar, btn_jogar, border_radius=12)
            pygame.draw.rect(tela, cor_sair,  btn_sair,  border_radius=12)

            for btn, texto in ((btn_jogar, "JOGAR"), (btn_sair, "SAIR")):
                surf = fonte_btn.render(texto, True, BRANCO)
                tela.blit(surf, (btn.x + (btn.w - surf.get_width()) // 2,
                                  btn.y + (btn.h - surf.get_height()) // 2))

            pygame.display.flip()
            clock.tick(60)

        return resultado

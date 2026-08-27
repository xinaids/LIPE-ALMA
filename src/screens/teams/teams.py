import pygame
from src.datatypes.player import Player

pygame.init()


class TeamsScreen:
    def __init__(self, jogadores: list[Player], largura: int = 1920, altura: int = 1080):
        pygame.init()
        self.largura = largura
        self.altura = altura
        self.time_a = [p for p in jogadores if getattr(p, 'Team', None) == "A"]
        self.time_b = [p for p in jogadores if getattr(p, 'Team', None) == "B"]
        if not self.time_a and not self.time_b:
            self.time_a = [p for i, p in enumerate(jogadores) if i % 2 == 0]
            self.time_b = [p for i, p in enumerate(jogadores) if i % 2 == 1]

    def Show(self) -> str:
        tela = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.largura, self.altura = tela.get_size()
        pygame.font.init()

        BRANCO    = (255, 255, 255)
        VM_PAINEL = ( 90,  15,  15)
        VM_BORDA  = (220,  60,  60)
        AZ_PAINEL = ( 15,  15,  90)
        AZ_BORDA  = ( 60,  60, 220)

        fonte_titulo = pygame.font.Font(None, int(self.largura * 0.04))
        fonte_time   = pygame.font.Font(None, int(self.largura * 0.035))
        fonte_nome   = pygame.font.Font(None, int(self.largura * 0.028))
        fonte_btn    = pygame.font.Font(None, int(self.largura * 0.03))

        panel_h  = int(self.altura * 0.75)
        panel_a  = pygame.Rect(20,                      80, self.largura // 2 - 30, panel_h)
        panel_b  = pygame.Rect(self.largura // 2 + 10,  80, self.largura // 2 - 30, panel_h)

        btn_y     = self.altura - 80
        btn_jogar = pygame.Rect(self.largura // 4,                    btn_y, self.largura // 4, 60)
        btn_sair  = pygame.Rect(self.largura // 2 + self.largura // 8, btn_y, self.largura // 4, 60)

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

            tela.fill((20, 20, 30))

            # título topo
            surf_titulo = fonte_titulo.render("LIPE-ALMA", True, BRANCO)
            tela.blit(surf_titulo, (self.largura // 2 - surf_titulo.get_width() // 2, 20))

            # painéis
            for panel, cor_fundo, cor_borda, label, jogadores in (
                (panel_a, VM_PAINEL, VM_BORDA, "TIME A", self.time_a),
                (panel_b, AZ_PAINEL, AZ_BORDA, "TIME B", self.time_b),
            ):
                pygame.draw.rect(tela, cor_fundo, panel)
                pygame.draw.rect(tela, cor_borda,  panel, 3)

                surf_label = fonte_time.render(label, True, BRANCO)
                tela.blit(surf_label, (panel.x + (panel.w - surf_label.get_width()) // 2, panel.y + 15))

                y = panel.y + 15 + surf_label.get_height() + 10
                for p in jogadores:
                    surf_nome = fonte_nome.render(p.Name, True, BRANCO)
                    tela.blit(surf_nome, (panel.x + 20, y))
                    y += 50

            # botões
            cor_jogar = (0, 220, 0) if btn_jogar.collidepoint(mouse) else (0, 160, 0)
            cor_sair  = (220,  0, 0) if btn_sair.collidepoint(mouse)  else (160,  0, 0)
            pygame.draw.rect(tela, cor_jogar, btn_jogar)
            pygame.draw.rect(tela, cor_sair,  btn_sair)

            for btn, texto in ((btn_jogar, "JOGAR"), (btn_sair, "SAIR")):
                surf = fonte_btn.render(texto, True, BRANCO)
                tela.blit(surf, (btn.x + (btn.w - surf.get_width()) // 2,
                                  btn.y + (btn.h - surf.get_height()) // 2))

            pygame.display.flip()
            clock.tick(60)

        return resultado

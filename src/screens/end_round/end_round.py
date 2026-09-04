import pygame


class EndRoundScreen:
    def __init__(self, score_a: int, score_b: int):
        self.score_a = score_a
        self.score_b = score_b

    def Show(self) -> str:
        tela = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        largura, altura = tela.get_size()
        pygame.font.init()

        BRANCO       = (255, 255, 255)
        COR_CONTINUAR = (30, 140, 30)
        COR_AUMENTAR  = (200, 120, 0)
        COR_SAIR      = (140, 30, 30)
        HOVER_DELTA   = 40

        fonte_titulo = pygame.font.Font(None, int(largura * 0.05))
        fonte_placar = pygame.font.Font(None, int(largura * 0.065))
        fonte_btn    = pygame.font.Font(None, int(largura * 0.032))

        btn_w  = int(largura * 0.22)
        btn_h  = int(altura  * 0.15)
        gap    = int(largura * 0.04)
        total  = 3 * btn_w + 2 * gap
        x0     = (largura - total) // 2
        btn_y  = int(altura * 0.65)

        btn_continuar = pygame.Rect(x0,                    btn_y, btn_w, btn_h)
        btn_aumentar  = pygame.Rect(x0 + btn_w + gap,     btn_y, btn_w, btn_h)
        btn_sair      = pygame.Rect(x0 + 2 * (btn_w + gap), btn_y, btn_w, btn_h)

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
                    if btn_continuar.collidepoint(mouse):
                        resultado = "continuar"
                        rodando = False
                    elif btn_aumentar.collidepoint(mouse):
                        resultado = "aumentar"
                        rodando = False
                    elif btn_sair.collidepoint(mouse):
                        resultado = "sair"
                        rodando = False

            tela.fill((20, 20, 30))

            surf_titulo = fonte_titulo.render("FIM DE RODADA", True, BRANCO)
            tela.blit(surf_titulo, (largura // 2 - surf_titulo.get_width() // 2, int(altura * 0.08)))

            surf_a = fonte_placar.render(f"Time Vermelho:  {self.score_a}", True, (220, 80, 80))
            surf_b = fonte_placar.render(f"Time Azul:  {self.score_b}",     True, (80, 120, 220))
            tela.blit(surf_a, (largura // 2 - surf_a.get_width() // 2, int(altura * 0.30)))
            tela.blit(surf_b, (largura // 2 - surf_b.get_width() // 2, int(altura * 0.42)))

            for btn, cor_base, linhas in (
                (btn_continuar, COR_CONTINUAR, ["CONTINUAR"]),
                (btn_aumentar,  COR_AUMENTAR,  ["AUMENTAR", "DIFICULDADE"]),
                (btn_sair,      COR_SAIR,      ["SAIR"]),
            ):
                hover = btn.collidepoint(mouse)
                cor   = tuple(min(c + HOVER_DELTA, 255) for c in cor_base) if hover else cor_base
                pygame.draw.rect(tela, cor, btn, border_radius=14)
                pygame.draw.rect(tela, BRANCO, btn, 3, border_radius=14)

                line_h   = fonte_btn.get_height()
                total_h  = len(linhas) * line_h + (len(linhas) - 1) * 4
                y_start  = btn.y + (btn.h - total_h) // 2
                for i, linha in enumerate(linhas):
                    surf = fonte_btn.render(linha, True, BRANCO)
                    tela.blit(surf, (btn.x + (btn.w - surf.get_width()) // 2,
                                     y_start + i * (line_h + 4)))

            pygame.display.flip()
            clock.tick(60)

        return resultado

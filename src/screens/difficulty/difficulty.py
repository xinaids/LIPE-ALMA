import pygame

pygame.init()


class DifficultyScreen:
    def __init__(self, largura: int = 1920, altura: int = 1080):
        pygame.init()
        self.largura = largura
        self.altura = altura

    def Show(self) -> int | None:
        tela = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.largura, self.altura = tela.get_size()
        pygame.font.init()

        BRANCO     = (255, 255, 255)
        COR_FACIL  = ( 30, 140,  30)
        COR_MEDIO  = (200, 120,   0)
        COR_DIFICIL= (180,  20,  20)
        COR_VOLTAR = ( 60,  60,  80)
        COR_HOVER  = (255, 255, 100)

        fonte_titulo = pygame.font.Font(None, int(self.largura * 0.045))
        fonte_sub    = pygame.font.Font(None, int(self.largura * 0.028))
        fonte_btn    = pygame.font.Font(None, int(self.largura * 0.038))
        fonte_voltar = pygame.font.Font(None, int(self.largura * 0.025))

        btn_w  = int(self.largura * 0.22)
        btn_h  = int(self.altura  * 0.18)
        gap    = int(self.largura * 0.04)
        total  = 3 * btn_w + 2 * gap
        x0     = (self.largura - total) // 2
        btn_y  = int(self.altura * 0.40)

        btn_facil   = pygame.Rect(x0,               btn_y, btn_w, btn_h)
        btn_medio   = pygame.Rect(x0 + btn_w + gap, btn_y, btn_w, btn_h)
        btn_dificil = pygame.Rect(x0 + 2 * (btn_w + gap), btn_y, btn_w, btn_h)

        btn_voltar  = pygame.Rect(int(self.largura * 0.03),
                                   self.altura - int(self.altura * 0.10),
                                   int(self.largura * 0.12),
                                   int(self.altura  * 0.07))

        DESCRICOES = {
            "FÁCIL":   "3 movimentos",
            "MÉDIO":   "4 movimentos",
            "DIFÍCIL": "5 movimentos",
        }

        clock     = pygame.time.Clock()
        rodando   = True
        resultado = None

        while rodando:
            mouse = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    rodando = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    rodando = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if btn_facil.collidepoint(mouse):
                        resultado = 3
                        rodando = False
                    elif btn_medio.collidepoint(mouse):
                        resultado = 4
                        rodando = False
                    elif btn_dificil.collidepoint(mouse):
                        resultado = 5
                        rodando = False
                    elif btn_voltar.collidepoint(mouse):
                        resultado = None
                        rodando = False

            tela.fill((20, 20, 30))

            # título
            surf_titulo = fonte_titulo.render("ESCOLHA A DIFICULDADE", True, BRANCO)
            tela.blit(surf_titulo, (self.largura // 2 - surf_titulo.get_width() // 2,
                                     int(self.altura * 0.12)))

            # botões de dificuldade
            for btn, cor_base, label in (
                (btn_facil,   COR_FACIL,   "FÁCIL"),
                (btn_medio,   COR_MEDIO,   "MÉDIO"),
                (btn_dificil, COR_DIFICIL, "DIFÍCIL"),
            ):
                hover = btn.collidepoint(mouse)
                cor   = tuple(min(c + 40, 255) for c in cor_base) if hover else cor_base
                pygame.draw.rect(tela, cor, btn, border_radius=14)
                pygame.draw.rect(tela, BRANCO, btn, 3, border_radius=14)

                surf_label = fonte_btn.render(label, True, BRANCO)
                tela.blit(surf_label, (btn.x + (btn.w - surf_label.get_width()) // 2,
                                        btn.y + btn.h // 2 - surf_label.get_height()))

                surf_desc = fonte_sub.render(DESCRICOES[label], True, BRANCO)
                tela.blit(surf_desc, (btn.x + (btn.w - surf_desc.get_width()) // 2,
                                       btn.y + btn.h // 2 + 6))

            # botão voltar
            cor_v = tuple(min(c + 30, 255) for c in COR_VOLTAR) if btn_voltar.collidepoint(mouse) else COR_VOLTAR
            pygame.draw.rect(tela, cor_v, btn_voltar, border_radius=10)
            pygame.draw.rect(tela, BRANCO, btn_voltar, 2, border_radius=10)
            surf_v = fonte_voltar.render("VOLTAR", True, BRANCO)
            tela.blit(surf_v, (btn_voltar.x + (btn_voltar.w - surf_v.get_width()) // 2,
                                btn_voltar.y + (btn_voltar.h - surf_v.get_height()) // 2))

            pygame.display.flip()
            clock.tick(60)

        return resultado

import pygame


class SplashScreen:
    def Show(self):
        tela = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        largura, altura = tela.get_size()
        pygame.font.init()

        BRANCO     = (255, 255, 255)
        CINZA_SUB  = (180, 180, 180)
        COR_JOGAR  = ( 30, 140,  30)
        FUNDO      = ( 20,  20,  30)

        fonte_titulo = pygame.font.Font(None, int(largura * 0.10))
        fonte_sub    = pygame.font.Font(None, int(largura * 0.030))
        fonte_btn    = pygame.font.Font(None, int(largura * 0.038))

        btn_w = int(largura * 0.22)
        btn_h = int(altura  * 0.13)
        btn_jogar = pygame.Rect(
            (largura - btn_w) // 2,
            int(altura * 0.65),
            btn_w,
            btn_h,
        )

        clock   = pygame.time.Clock()
        rodando = True

        while rodando:
            mouse = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if btn_jogar.collidepoint(mouse):
                        rodando = False

            tela.fill(FUNDO)

            surf_titulo = fonte_titulo.render("LIPE-ALMA", True, BRANCO)
            tela.blit(surf_titulo, (
                largura // 2 - surf_titulo.get_width() // 2,
                int(altura * 0.28),
            ))

            surf_sub = fonte_sub.render("Movimento e Memória Ativa", True, CINZA_SUB)
            tela.blit(surf_sub, (
                largura // 2 - surf_sub.get_width() // 2,
                int(altura * 0.28) + surf_titulo.get_height() + int(altura * 0.02),
            ))

            hover = btn_jogar.collidepoint(mouse)
            cor   = (min(COR_JOGAR[0] + 40, 255), min(COR_JOGAR[1] + 40, 255), min(COR_JOGAR[2] + 40, 255)) if hover else COR_JOGAR
            pygame.draw.rect(tela, cor, btn_jogar, border_radius=14)
            pygame.draw.rect(tela, BRANCO, btn_jogar, 3, border_radius=14)

            surf_btn = fonte_btn.render("JOGAR", True, BRANCO)
            tela.blit(surf_btn, (
                btn_jogar.x + (btn_jogar.w - surf_btn.get_width()) // 2,
                btn_jogar.y + (btn_jogar.h - surf_btn.get_height()) // 2,
            ))

            pygame.display.flip()
            clock.tick(60)

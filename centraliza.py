def centraliza_janela(janela):
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()

    largura = largura_tela - 50
    altura = altura_tela - 50

    posx = (largura_tela // 2) - (largura // 2)
    posy = (altura_tela // 2) - (altura // 2)

    janela.geometry(f"{largura}x{altura}+{posx}+{posy}")
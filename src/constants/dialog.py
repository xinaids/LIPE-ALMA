from src.datatypes.dialog import Animation, Dialog
from src.animation.explosion import ExplosionAnimation
import os

CHARACTER_DIALOG = "images" + os.sep + "robot" + os.sep + "lipe.png"
CHARACTER_DIALOG2 = "images" + os.sep + "robot" + os.sep + "lipe2.png"

DIALOG_START_GAME = [
    Dialog(
        Text="Olá! Eu sou o Lipe, seu parceiro de exercícios.",
        Character_Dir=CHARACTER_DIALOG,
    ),
    Dialog(
        Text="Vamos fazer alguns movimentos juntos para ativar corpo e mente.",
        Character_Dir=CHARACTER_DIALOG,
    ),
    Dialog(
        Text="Vou mostrar um movimento na tela — observe com atenção.",
        Character_Dir=CHARACTER_DIALOG,
    ),
    Dialog(
        Text="Depois é sua vez de repetir, no seu ritmo.",
        Character_Dir=CHARACTER_DIALOG,
    ),
    Dialog(
        Text="Não se preocupe em errar — o importante é se mover e se divertir!",
        Character_Dir=CHARACTER_DIALOG,
    ),
    Dialog(
        Text="Vamos começar?",
        Character_Dir=CHARACTER_DIALOG,
        Bold=True,
    ),
]

DIALOG_SEQUENCE = [
    Dialog(
        Text="Vou mostrar uma sequência de movimentos.",
        Character_Dir=CHARACTER_DIALOG,
    ),
    Dialog(
        Text="Observe cada um com calma.",
        Character_Dir=CHARACTER_DIALOG,
    ),
    Dialog(
        Text="Depois, repita na mesma ordem que você viu.",
        Character_Dir=CHARACTER_DIALOG,
    ),
    Dialog(
        Text="Fique à vontade para ir devagar. Vamos lá!",
        Character_Dir=CHARACTER_DIALOG,
        Bold=True,
    ),
]

DIALOG_CONDITION = [
    Dialog(
        Text=f"Imagine que você está brincando e alguém te pergunta: 'Está chovendo lá fora?'.",
        Character_Dir=CHARACTER_DIALOG,
    ),
    Dialog(
        Text=f"Se estiver chovendo, você responde 'Sim', e fica em casa.",
        Character_Dir=CHARACTER_DIALOG,
    ),
    Dialog(
        Text=f"Se não estiver chovendo, você diz 'Não' e sai para brincar.",
        Character_Dir=CHARACTER_DIALOG,
    ),
    Dialog(
        Text=f"Isso é uma condição! É como uma pergunta que ajuda a escolher o que fazer.",
        Character_Dir=CHARACTER_DIALOG,
    ),
    Dialog(
        Text=f"Agora, imagine que o computador também precisa tomar decisões.",
        Character_Dir=CHARACTER_DIALOG,
    ),
    Dialog(
        Text=f"Ele faz perguntas como: 'O botão foi pressionado?' ou 'O número é maior que 10?'.",
        Character_Dir=CHARACTER_DIALOG,
    ),
    Dialog(
        Text=f"Dependendo da resposta, ele faz uma coisa ou outra.",
        Character_Dir=CHARACTER_DIALOG,
    ),
    Dialog(
        Text="Pronto pra praticar?",
        Character_Dir=CHARACTER_DIALOG,
    ),
    Dialog(
        Text="Nesse jogo os movimentos são representados por cores.",
        Character_Dir=CHARACTER_DIALOG,
    ),
    Dialog(
        Text="Primeiro, será mostrado qual movimento cada cor representa.",
        Character_Dir=CHARACTER_DIALOG,
    ),
    Dialog(
        Text="Depois será mostrado em tela a sequencia de cores.",
        Character_Dir=CHARACTER_DIALOG,
    ),
    Dialog(
        Text="Memorize as cores e depois realize os movimentos que elas representam na ordem correta.",
        Character_Dir=CHARACTER_DIALOG,
    ),
    Dialog(
        Text="Vamos lá!",
        Character_Dir=CHARACTER_DIALOG,
    ),
]

DIALOG_ITERATION = [
    Dialog(
        Text="AQUI VAI O TEXTO DA ITERAÇÃO",
        Character_Dir=CHARACTER_DIALOG,
    ),
]

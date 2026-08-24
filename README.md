# LIPE-ALMA — Atividade Lúdica para Memória Ativa

LIPE-ALMA é um jogo digital para estimular coordenação motora e memória em idosos, usando reconhecimento de pose via webcam. O jogador segue sequências de movimentos exibidas na tela, executando-as com o próprio corpo. O jogo detecta os movimentos automaticamente e fornece feedback visual imediato, encorajando o participante a cada etapa.

---

## Pré-requisitos

- Python 3.11
- pip (gerenciador de pacotes do Python)
- Uma webcam funcional
- Desktop Development with C++ (disponível ao instalar o Visual Studio)

---

## Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/MateusSilver/LIPE-ALMA
cd LIPE-ALMA
```

### 2. Crie e ative um ambiente virtual (recomendado)

```bash
# Criação
python -m venv venv

# Ativação no Windows
venv\Scripts\activate

# Ativação no Linux/macOS
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute o jogo

```bash
python main.py
```

---

## Movimentos

| Movimento | Descrição |
|---|---|
| Braço Esquerdo | Levante o braço esquerdo acima da cabeça |
| Braço Direito | Levante o braço direito acima da cabeça |
| Abra os Braços | Abra os dois braços para os lados (posição em T) |
| Dobre os Joelhos | Dobre levemente os joelhos (agache suave) |

---

## Como jogar

1. Posicione-se na frente da webcam de forma que seu corpo inteiro apareça na tela.
2. O jogo exibe uma fase de aquecimento: siga cada movimento no seu ritmo.
3. Após o aquecimento, o jogo mostra sequências de movimentos para memorizar e executar.
4. A cada acerto você avança; não se preocupe com erros — basta tentar novamente!

---

## Observações

- Para remover os jogadores registrados, delete o arquivo `database/database.db`.
- Os logs de execução ficam em `execucoes.log` e as imagens de log em `LogsImages/`.

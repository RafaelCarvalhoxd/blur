# BLUR

Um utilitário Python para aplicar um filtro de **Blur Médio** em imagens, de forma paralela, usando **NumPy** e **Pillow**, com duas interfaces:

1. **CLI** – linha de comando em `scripts/run_blur.py` (py scripts/run_blur.py imagem-teste.jpg imagem-borrada.jpg --kernel 5 --threads 8 --passes 2 )
2. **GUI** – interface gráfica Tkinter em `ui.py`

---

## Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes)

---

## Instalação

`
**Instale as dependências**

```bash
pip install -r requirements.txt
```

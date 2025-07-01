
import argparse
import numpy as np
from PIL import Image
from core import parallel_blur_array

def main():
    parser = argparse.ArgumentParser(description="Aplicar blur via CLI")
    parser.add_argument("input",  help="Caminho da imagem de entrada")
    parser.add_argument("output", help="Caminho da imagem de saída")
    parser.add_argument("--kernel",  type=int, default=3,   help="Tamanho do kernel (ímpar)")
    parser.add_argument("--threads", type=int, default=4,   help="Número de threads")
    parser.add_argument("--passes",  type=int, default=1,   help="Número de passadas de blur")
    args = parser.parse_args()

    img = Image.open(args.input).convert('RGB')
    arr = np.array(img, dtype=np.float32)
    res = parallel_blur_array(arr, args.kernel, args.threads, args.passes)
    Image.fromarray(np.clip(res, 0, 255).astype(np.uint8)).save(args.output)
    print(f"Salvo em {args.output}")

if __name__ == "__main__":
    main()

"""
python scripts/run_blur.py entrada.jpg saida.jpg --kernel 5 --threads 8 --passes 3
"""
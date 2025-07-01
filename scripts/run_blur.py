
import argparse
import os
import sys
import numpy as np
from PIL import Image

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))         
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)                      
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from core.core import parallel_blur_array  

def main():
    BASE_DIR   = PROJECT_ROOT
    INPUT_DIR  = os.path.join(BASE_DIR, 'public', 'input')
    OUTPUT_DIR = os.path.join(BASE_DIR, 'public', 'output')

    parser = argparse.ArgumentParser(description="Aplicar blur via CLI")
    parser.add_argument("input",
                        help="Nome de arquivo ou caminho da imagem de entrada")
    parser.add_argument("output",
                        help="Nome de arquivo ou caminho da imagem de saída")
    parser.add_argument("--kernel",  type=int, default=3,
                        help="Tamanho do kernel (ímpar)")
    parser.add_argument("--threads", type=int, default=4,
                        help="Número de threads")
    parser.add_argument("--passes",  type=int, default=1,
                        help="Número de passadas de blur")
    args = parser.parse_args()

    def resolve(path_arg: str, default_dir: str) -> str:
        if os.path.isabs(path_arg) or os.sep in path_arg:
            return path_arg
        return os.path.join(default_dir, path_arg)

    input_path  = resolve(args.input, INPUT_DIR)
    output_path = resolve(args.output, OUTPUT_DIR)

    out_dir = os.path.dirname(output_path)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    img = Image.open(input_path).convert('RGB')
    arr = np.array(img, dtype=np.float32)
    res = parallel_blur_array(arr, args.kernel, args.threads, args.passes)
    result_img = Image.fromarray(np.clip(res, 0, 255).astype(np.uint8))
    result_img.save(output_path)

    print(f"Salvo em {output_path}")

if __name__ == "__main__":
    main()

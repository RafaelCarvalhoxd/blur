
import threading
import numpy as np
from PIL import Image

def apply_blur_region(input_arr, output_arr, kernel_size, y_start, y_end):

    pad = kernel_size // 2
    H, W, C = input_arr.shape
    padded = np.pad(input_arr, ((pad,pad),(pad,pad),(0,0)), mode='edge')

    for y in range(y_start, y_end):
        for x in range(W):
            neighborhood = padded[y:y+kernel_size, x:x+kernel_size]
            output_arr[y, x] = neighborhood.reshape(-1, C).mean(axis=0)

def parallel_blur_array(arr, kernel_size, num_threads, passes=1):

    for _ in range(passes):
        H, W, C = arr.shape
        output = np.zeros_like(arr)
        stripe = H // num_threads
        threads = []
        for i in range(num_threads):
            y0 = i * stripe
            y1 = (i+1) * stripe if i < num_threads - 1 else H
            t = threading.Thread(
                target=apply_blur_region,
                args=(arr, output, kernel_size, y0, y1)
            )
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        arr = output
    return arr

def parallel_blur(input_path, output_path, kernel_size, num_threads, passes, on_done):

    try:
        img = Image.open(input_path).convert('RGB')
        arr = np.array(img, dtype=np.float32)
        result_arr = parallel_blur_array(arr, kernel_size, num_threads, passes)
        result = Image.fromarray(np.clip(result_arr, 0, 255).astype(np.uint8))
        result.save(output_path)
        on_done(True, output_path)
    except Exception as e:
        on_done(False, str(e))

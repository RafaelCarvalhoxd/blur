
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from core import parallel_blur

class BlurApp:
    def __init__(self, root):
        self.root = root
        root.title("Blur Médio Paralelo")

        tk.Label(root, text="Imagem de Entrada:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.in_path = tk.Entry(root, width=40)
        self.in_path.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(root, text="...", command=self.browse_input).grid(row=0, column=2, padx=5, pady=5)

        tk.Label(root, text="Salvar em:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.out_path = tk.Entry(root, width=40)
        self.out_path.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(root, text="...", command=self.browse_output).grid(row=1, column=2, padx=5, pady=5)

        tk.Label(root, text="Tamanho do Kernel (ímpar):").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.kernel_spin = tk.Spinbox(root, from_=3, to=31, increment=2, width=5)
        self.kernel_spin.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        tk.Label(root, text="Número de Threads:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.thread_spin = tk.Spinbox(root, from_=1, to=32, width=5)
        self.thread_spin.grid(row=3, column=1, sticky="w", padx=5, pady=5)

        tk.Label(root, text="Passadas de Blur:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.passes_spin = tk.Spinbox(root, from_=1, to=10, width=5)
        self.passes_spin.grid(row=4, column=1, sticky="w", padx=5, pady=5)

        self.btn = tk.Button(root, text="Aplicar Blur", command=self.start_blur)
        self.btn.grid(row=5, column=0, columnspan=3, pady=10)

        self.status = tk.Label(root, text="", fg="blue")
        self.status.grid(row=6, column=0, columnspan=3, pady=(0,10))

    def browse_input(self):
        path = filedialog.askopenfilename(
            filetypes=[("Imagens", "*.png;*.jpg;*.jpeg;*.bmp"), ("Todos", "*.*")]
        )
        if path:
            self.in_path.delete(0, tk.END)
            self.in_path.insert(0, path)

    def browse_output(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png"), ("BMP", "*.bmp")]
        )
        if path:
            self.out_path.delete(0, tk.END)
            self.out_path.insert(0, path)

    def start_blur(self):
        inp = self.in_path.get().strip()
        out = self.out_path.get().strip()
        try:
            k = int(self.kernel_spin.get())
            t = int(self.thread_spin.get())
            p = int(self.passes_spin.get())
        except ValueError:
            messagebox.showerror("Erro", "Kernel, Threads e Passadas devem ser inteiros.")
            return
        if not inp or not out:
            messagebox.showerror("Erro", "Selecione caminhos de entrada e saída.")
            return
        if k < 1 or k % 2 == 0:
            messagebox.showerror("Erro", "Kernel deve ser ímpar e ≥ 1.")
            return

        self.btn.config(state="disabled")
        self.status.config(text="Processando... isso pode levar alguns segundos.")

        threading.Thread(
            target=parallel_blur,
            args=(inp, out, k, t, p, self.on_done),
            daemon=True
        ).start()

    def on_done(self, success, msg):
        self.root.after(0, lambda: self.finish(success, msg))

    def finish(self, success, msg):
        self.btn.config(state="normal")
        self.status.config(text="")
        if success:
            messagebox.showinfo("Concluído", f"Imagem salva em:\n{msg}")
        else:
            messagebox.showerror("Erro ao processar", msg)

if __name__ == "__main__":
    root = tk.Tk()
    app = BlurApp(root)
    root.mainloop()

import tkinter as tk
from tkinter import messagebox
import math


class Calculadora:

    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora Científica")
        self.root.geometry("450x650")
        self.root.resizable(False, False)
        self.root.configure(bg="#f4f6fa")

        self.expresion = ""
        self.decimales = 4

        self.entrada = tk.Entry(
            root,
            font=("Segoe UI", 20, "bold"),
            borderwidth=0,
            relief="flat",
            justify="right",
            bg="#222831",
            fg="#EEEEEE",
            insertbackground="white"
        )
        self.entrada.pack(fill=tk.BOTH, ipadx=8, ipady=15, padx=15, pady=15)

        self.crear_botones()
        self.configurar_teclado()  # 🔥 Activar teclado


    # ----------------------------
    # FUNCIONES BÁSICAS
    # ----------------------------

    def agregar(self, valor):
        self.expresion += str(valor)
        self.entrada.delete(0, tk.END)
        self.entrada.insert(tk.END, self.expresion)

    def limpiar(self, event=None):
        self.expresion = ""
        self.entrada.delete(0, tk.END)

    def retroceder(self, event=None):
        self.expresion = self.expresion[:-1]
        self.entrada.delete(0, tk.END)
        self.entrada.insert(tk.END, self.expresion)

    def cambiar_decimales(self, n):
        self.decimales = n
        messagebox.showinfo("Decimales", f"Ahora se muestran {n} decimales")


    # ----------------------------
    # CONFIGURACIÓN TECLADO
    # ----------------------------

    def configurar_teclado(self):

        # Enter = calcular
        self.root.bind("<Return>", lambda event: self.calcular())
        self.root.bind("<KP_Enter>", lambda event: self.calcular())

        # Backspace
        self.root.bind("<BackSpace>", self.retroceder)

        # ESC limpiar
        self.root.bind("<Escape>", self.limpiar)

        # Números y operadores básicos
        teclas_permitidas = "0123456789+-*/()."

        for tecla in teclas_permitidas:
            self.root.bind(tecla, lambda event, t=tecla: self.agregar(t))


    # ----------------------------
    # CALCULAR
    # ----------------------------

    def calcular(self):

        try:
            expr = self.expresion

            expr = expr.replace("×", "*")
            expr = expr.replace("÷", "/")
            expr = expr.replace("−", "-")
            expr = expr.replace("^", "**")

            expr = expr.replace("π", str(math.pi))

            expr = expr.replace("sin", "math.sin")
            expr = expr.replace("cos", "math.cos")
            expr = expr.replace("tan", "math.tan")
            expr = expr.replace("√", "math.sqrt")
            expr = expr.replace("ln", "math.log")
            expr = expr.replace("log₁₀", "math.log10")

            # Validar raíz indefinida
            if "math.sqrt" in expr and "-" in expr:
                raise ValueError("Raíz indefinida")

            resultado = eval(expr, {"__builtins__": None}, {"math": math})

            if isinstance(resultado, float):
                resultado = round(resultado, self.decimales)

            self.entrada.delete(0, tk.END)
            self.entrada.insert(tk.END, str(resultado))
            self.expresion = str(resultado)

        except Exception:
            messagebox.showerror("Error", "Expresión inválida")
            self.limpiar()


    # ----------------------------
    # BOTONES
    # ----------------------------

    def crear_botones(self):

        botones = [
            ["7", "8", "9", "÷", "C"],
            ["4", "5", "6", "×", "⌫"],
            ["1", "2", "3", "−", "("],
            ["0", ".", "=", "+", ")"],
            ["π", "√", "x²", "x³", "xʸ"],
            ["sin", "cos", "tan", "ln", "log₁₀"],
            ["1/x", "n!", "³√", "log(a,b)", "DEC"]
        ]

        colores = {
            "normal": "#e0e0e0",
            "operador": "#90caf9",
            "igual": "#43a047",
            "especial": "#ffb74d"
        }

        marco = tk.Frame(self.root, bg="#f4f6fa")
        marco.pack()

        for fila in botones:
            fila_frame = tk.Frame(marco, bg="#f4f6fa")
            fila_frame.pack()

            for boton in fila:

                if boton == "=":
                    comando = self.calcular
                    color = colores["igual"]

                elif boton == "C":
                    comando = self.limpiar
                    color = colores["especial"]

                elif boton == "⌫":
                    comando = self.retroceder
                    color = colores["especial"]

                elif boton == "x²":
                    comando = lambda: self.agregar("**2")
                    color = colores["operador"]

                elif boton == "x³":
                    comando = lambda: self.agregar("**3")
                    color = colores["operador"]

                elif boton == "xʸ":
                    comando = lambda: self.agregar("**")
                    color = colores["operador"]

                elif boton == "³√":
                    comando = lambda: self.agregar("**(1/3)")
                    color = colores["operador"]

                elif boton == "1/x":
                    comando = lambda: self.agregar("1/")
                    color = colores["operador"]

                elif boton == "n!":
                    comando = lambda: self.agregar("math.factorial(")
                    color = colores["operador"]

                elif boton == "log(a,b)":
                    comando = lambda: self.agregar("math.log(")
                    color = colores["operador"]

                elif boton == "DEC":
                    comando = lambda: self.cambiar_decimales(6)
                    color = colores["especial"]

                elif boton in ["+", "−", "×", "÷", "√", "sin", "cos", "tan", "ln", "log₁₀", "π"]:
                    comando = lambda val=boton: self.agregar(val)
                    color = colores["operador"]

                else:
                    comando = lambda val=boton: self.agregar(val)
                    color = colores["normal"]

                b = tk.Button(
                    fila_frame,
                    text=boton,
                    width=6,
                    height=2,
                    font=("Segoe UI", 12, "bold"),
                    bg=color,
                    bd=0,
                    command=comando
                )

                b.pack(side=tk.LEFT, padx=5, pady=5)


# ----------------------------
# MAIN
# ----------------------------

def main():
    root = tk.Tk()
    app = Calculadora(root)
    root.mainloop()


if __name__ == "__main__":
    main()
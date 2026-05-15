import tkinter as tk

root = tk.Tk()
root.title("Calculadora")
root.resizable(False, False)
root.configure(bg="#0d0d0d")

expression = ""
result_shown = False

# ── Display ──────────────────────────────────────────
display_frame = tk.Frame(root, bg="#111111", padx=20, pady=16)
display_frame.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=2, pady=(2, 0))

expr_var = tk.StringVar(value="")
expr_label = tk.Label(
    display_frame, textvariable=expr_var,
    font=("Consolas", 13), bg="#111111", fg="#555555",
    anchor="e"
)
expr_label.pack(fill="x")

result_var = tk.StringVar(value="0")
result_label = tk.Label(
    display_frame, textvariable=result_var,
    font=("Consolas", 32, "bold"), bg="#111111", fg="#ffffff",
    anchor="e"
)
result_label.pack(fill="x")

# ── Lógica ────────────────────────────────────────────
def format_number(value):
    try:
        f = float(value)
        return str(int(f)) if f == int(f) else str(f)
    except:
        return value

def on_click(label):
    global expression, result_shown

    if label == "C":
        expression = ""
        result_var.set("0")
        expr_var.set("")
        result_shown = False

    elif label == "⌫":
        if result_shown:
            expression = ""
            result_var.set("0")
            result_shown = False
        else:
            expression = expression[:-1]
            result_var.set(expression or "0")

    elif label == "=":
        try:
            expr_var.set(expression + " =")
            result = eval(expression)
            expression = format_number(str(result))
            result_var.set(expression)
            result_shown = True
        except ZeroDivisionError:
            result_var.set("erro: div/0")
            expression = ""
        except:
            result_var.set("erro")
            expression = ""

    elif label == "%":
        try:
            val = float(expression)
            expression = str(val / 100)
            result_var.set(format_number(expression))
        except:
            pass

    elif label == "+/−":
        try:
            val = float(expression)
            expression = str(-val)
            result_var.set(format_number(expression))
        except:
            pass

    else:
        symbol_map = {"×": "*", "÷": "/", "−": "-"}
        char = symbol_map.get(label, label)

        if result_shown:
            if char in "+-*/":
                result_shown = False
            else:
                expression = ""
                result_shown = False

        expression += char
        result_var.set(expression)

# ── Botões ────────────────────────────────────────────
buttons = [
    ("C",   "#1f1f1f", "#ff5555"),
    ("⌫",   "#2a2a2a", "#aaaaaa"),
    ("%",   "#2a2a2a", "#aaaaaa"),
    ("÷",   "#2a2a2a", "#aaaaaa"),

    ("7",   "#1a1a1a", "#ffffff"),
    ("8",   "#1a1a1a", "#ffffff"),
    ("9",   "#1a1a1a", "#ffffff"),
    ("×",   "#2a2a2a", "#aaaaaa"),

    ("4",   "#1a1a1a", "#ffffff"),
    ("5",   "#1a1a1a", "#ffffff"),
    ("6",   "#1a1a1a", "#ffffff"),
    ("−",   "#2a2a2a", "#aaaaaa"),

    ("1",   "#1a1a1a", "#ffffff"),
    ("2",   "#1a1a1a", "#ffffff"),
    ("3",   "#1a1a1a", "#ffffff"),
    ("+",   "#2a2a2a", "#aaaaaa"),

    ("+/−", "#1a1a1a", "#ffffff"),
    ("0",   "#1a1a1a", "#ffffff"),
    (".",   "#1a1a1a", "#ffffff"),
    ("=",   "#333333", "#ffffff"),
]

for i, (label, bg, fg) in enumerate(buttons):
    row = (i // 4) + 1
    col = i % 4
    btn = tk.Button(
        root, text=label,
        font=("Consolas", 18), bg=bg, fg=fg,
        activebackground="#444444", activeforeground=fg,
        relief="flat", bd=0, cursor="hand2",
        width=4, height=2,
        command=lambda l=label: on_click(l)
    )
    btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")

root.mainloop()


# --- teclado ---------
def on_key(event):
    key_map = {
        "Return": "=",
        "BackSpace": "⌫",
        "Escape": "C",
        "*": "×",
        "/": "÷",
        "-": "−"
    }
    char = key_map.get(event.keysym, event.char)
    if char in "0123456789.+-=C⌫×÷−%":
        on_click(char)

root.bind("<Key>", on_key)

root.mainloop()
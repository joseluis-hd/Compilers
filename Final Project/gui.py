'''
José Luis Haro Díaz
GUI V1.0
'''

from __future__ import annotations
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from pathlib import Path

# ---- Paleta de colores ----
DARK_BG = "#0f1720"          
DARK_FG = "#e6edf3"          
DARK_CONSOLE_BG = "#0a1016"   
DARK_CONSOLE_FG = "#b4f1b4"   
ACCENT = "#3fb950"            

APP_TITLE = "Compilador – GUI (MiniJS → Node)"
DEFAULT_EXT = ".mini"

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title(APP_TITLE)
        self.geometry("1000x680")
        self.minsize(780, 520)
        self._current_file: Path | None = None
        self._modified = False

        self._build_layout()
        self._build_menus()
        self._bind_shortcuts()
        self._update_status()

        #Mensaje de bienvenida
        self.editor.insert(
            "1.0", "GUI Compilador NodeJS - V1.0 - José Luis Haro Díaz\n"
        )

    def _build_layout(self):
        toolbar = ttk.Frame(self, padding=(6,6,6,0))
        toolbar.pack(side="top", fill="x")
        for text, cmd in (("Abrir", self.open_file), ("Guardar", self.save_file), ("Limpiar", self.clear_all)):
            ttk.Button(toolbar, text=text, command=cmd).pack(side="left", padx=4)

        paned = ttk.PanedWindow(self, orient="vertical")
        paned.pack(fill="both", expand=True, padx=6, pady=6)

        f_editor = ttk.Frame(paned)
        self.editor = tk.Text(
            f_editor,
            wrap="none",
            undo=True,
            bg=DARK_BG,
            fg=DARK_FG,
            insertbackground=DARK_FG,
            padx=10,
            pady=8,
        )
        self.editor.pack(side="left", fill="both", expand=True)
        y1 = ttk.Scrollbar(f_editor, orient="vertical", command=self.editor.yview)
        x1 = ttk.Scrollbar(f_editor, orient="horizontal", command=self.editor.xview)
        self.editor.configure(yscrollcommand=y1.set, xscrollcommand=x1.set)
        y1.pack(side="right", fill="y")
        x1.pack(side="bottom", fill="x")
        paned.add(f_editor, weight=3)

        #Consola
        f_console = ttk.Frame(paned)
        self.console = tk.Text(
            f_console,
            height=8,
            wrap="word",
            bg=DARK_CONSOLE_BG,
            fg=DARK_CONSOLE_FG,
            insertbackground=DARK_CONSOLE_FG,
            padx=10,
            pady=8,
            state="normal",
        )
        self.console.pack(side="left", fill="both", expand=True)
        y2 = ttk.Scrollbar(f_console, orient="vertical", command=self.console.yview)
        self.console.configure(yscrollcommand=y2.set)
        y2.pack(side="right", fill="y")
        paned.add(f_console, weight=1)

        self.status = ttk.Label(self, anchor="w")
        self.status.pack(fill="x", padx=6, pady=(0,6))

        self.editor.bind("<<Modified>>", self._on_modified)
        self.editor.bind("<KeyRelease>", self._on_caret_move)
        self.editor.bind("<ButtonRelease-1>", self._on_caret_move)

    #---------------- Menús ----------------
    def _build_menus(self):
        menubar = tk.Menu(self)

        #Archivo
        m_file = tk.Menu(menubar, tearoff=0)
        m_file.add_command(label="Abrir", accelerator="Ctrl+A", command=self.open_file)
        m_file.add_command(label="Guardar", accelerator="Ctrl+G", command=self.save_file)
        m_file.add_command(label="Limpiar pantalla", accelerator="Ctrl+P", command=self.clear_all)
        m_file.add_separator()
        m_file.add_command(label="Cerrar", accelerator="Ctrl+Q", command=self.on_quit)
        menubar.add_cascade(label="Archivo", menu=m_file)

        #Compiladores
        m_comp = tk.Menu(menubar, tearoff=0)
        m_comp.add_command(label="Análisis Léxico", command=self.action_lexico)
        m_comp.add_command(label="Análisis Sintáctico", command=self.action_sintactico)
        m_comp.add_command(label="Análisis Semántico", command=self.action_semantico)
        m_comp.add_command(label="Generación Código Intermedio", command=self.action_intermedio)
        m_comp.add_command(label="Código Objeto", command=self.action_objeto)
        menubar.add_cascade(label="Compiladores", menu=m_comp)

        # Ayuda → “Librerías” (adaptado a Node: require())
        m_help = tk.Menu(menubar, tearoff=0)
        m_libs = tk.Menu(m_help, tearoff=0)
        for mod in ["fs", "path", "os", "http", "crypto", "url"]:
            m_libs.add_command(label=mod, command=lambda m=mod: self.insert_require(m))
        m_help.add_cascade(label="Librerías (Node)", menu=m_libs)
        m_help.add_command(label="Variables (guía)", command=lambda: self._insert("// JS: usa let/const; evita var\n"))
        m_help.add_command(label="main() (plantilla)", command=self.insert_main_js)
        menubar.add_cascade(label="Ayuda", menu=m_help)

        #Variables → Tipos
        m_vars = tk.Menu(menubar, tearoff=0)
        m_types = tk.Menu(m_vars, tearoff=0)
        for t in ["number", "string", "boolean", "array", "object"]:
            m_types.add_command(label=t, command=lambda tt=t: self.insert_js_var(tt))
        m_vars.add_cascade(label="Tipos", menu=m_types)
        menubar.add_cascade(label="Variables", menu=m_vars)

        self.config(menu=menubar)

    #---------------- Atajos ----------------
    def _bind_shortcuts(self):
        self.bind("<Control-a>", lambda e: self.open_file())
        self.bind("<Control-g>", lambda e: self.save_file())
        self.bind("<Control-p>", lambda e: self.clear_all())
        self.bind("<Control-q>", lambda e: self.on_quit())

    #---------------- Archivo ----------------
    def open_file(self):
        if not self._confirm_discard():
            return
        path = filedialog.askopenfilename(
            filetypes=[("MiniJS/JS", "*.mini *.js *.txt"), ("Todos", "*.*")]
        )
        if not path:
            return
        p = Path(path)
        text = p.read_text(encoding="utf-8", errors="ignore")
        self.editor.delete("1.0", "end")
        self.editor.insert("1.0", text)
        self._current_file = p
        self._modified = False
        self._log_console(f"✔ Archivo abierto: {p.name}\n")
        self._update_status()

    def save_file(self):
        if self._current_file is None:
            return self.save_file_as()
        self._write_to(self._current_file)
        self._log_console("✔ Archivo guardado\n")
        self._update_status()

    def save_file_as(self):
        path = filedialog.asksaveasfilename(
            defaultextension=DEFAULT_EXT,
            filetypes=[("MiniJS/JS", "*.mini *.js *.txt"), ("Todos", "*.*")]
        )
        if not path:
            return
        p = Path(path)
        self._write_to(p)
        self._current_file = p
        self._log_console(f"✔ Guardado como: {p.name}\n")
        self._update_status()

    def _write_to(self, p: Path):
        p.write_text(self.editor.get("1.0", "end-1c"), encoding="utf-8")
        self._modified = False

    def clear_all(self):
        self.editor.delete("1.0", "end")
        self.console.configure(state="normal")
        self.console.delete("1.0", "end")
        self.console.configure(state="normal")
        self._modified = True
        self._update_status()

    def on_quit(self):
        if self._confirm_discard():
            self.destroy()

    def _confirm_discard(self) -> bool:
        if not self._modified:
            return True
        return messagebox.askyesno("Descartar cambios", "Hay cambios sin guardar. ¿Deseas descartarlos?")

    #---------------- Ayuda / Librerías (Node) ----------------
    def insert_require(self, module_name: str):
        line = f"const {module_name} = require('{module_name}')\n"
        text = self.editor.get("1.0", "end-1c")
        if line not in text:
            self.editor.insert("1.0", line)
            self._log_console(f"＋ Módulo agregado: {module_name}\n")
        else:
            self._log_console(f"• Módulo ya presente: {module_name}\n")
        self._modified = True
        self._update_status()

    def insert_main_js(self):
        tpl = (
            "'use strict';\n\n"
            "function main() {\n"
            "\t// TODO: escribe tu lógica aquí\n"
            "\tconsole.log('Hello from main()');\n"
            "}\n\n"
            "if (require.main === module) {\n"
            "\tmain();\n"
            "}\n"
        )
        self.editor.insert("insert", tpl)
        self._modified = True
        self._update_status()

    #---------------- Variables (JS) ----------------
    def insert_js_var(self, vtype: str):
        name = simpledialog.askstring("Nueva variable", f"Nombre para variable {vtype}:")
        if not name:
            return
        if vtype == "number":
            decl = f"let {name} = 0;\n"
        elif vtype == "string":
            decl = f"let {name} = \"\";\n"
        elif vtype == "boolean":
            decl = f"let {name} = true;\n"
        elif vtype == "array":
            decl = f"let {name} = [];\n"
        elif vtype == "object":
            decl = f"let {name} = {{}};\n"
        else:
            decl = f"let {name};\n"
        self.editor.insert("insert", decl)
        self._log_console(f"＋ Variable insertada: {decl.strip()}\n")
        self._modified = True
        self._update_status()

    #---------------- Compiladores (marcadores) ----------------
    def action_lexico(self):
        self._insert_marker("// [LEXICO] tokens => [...]")

    def action_sintactico(self):
        self._insert_marker("// [SINTACTICO] AST => {...}")

    def action_semantico(self):
        self._insert_marker("// [SEMANTICO] chequeos de símbolos/tipos")

    def action_intermedio(self):
        self._insert_marker("// [INTERMEDIO] IR / 3-direcciones")

    def action_objeto(self):
        self._insert_marker("// [OBJETO] JS generado (Node)")

    def _insert_marker(self, text: str):
        self.editor.insert("insert", text + "\n")
        self._log_console(text + "\n")
        self._modified = True
        self._update_status()

    #---------------- Utilidades ----------------
    def _caret_pos(self):
        line, col = self.editor.index("insert").split(".")
        return int(line), int(col) + 1

    def _update_status(self):
        line, col = self._caret_pos()
        name = self._current_file.name if self._current_file else f"sin_nombre{DEFAULT_EXT}"
        dirty = "*" if self._modified else ""
        self.status.configure(text=f"{name}{dirty} — línea {line}, col {col}")
        self.title(f"{APP_TITLE} — {name}{' *' if self._modified else ''}")

    def _on_modified(self, event=None):
        if self.editor.edit_modified():
            self._modified = True
            self.editor.edit_modified(False)
            self._update_status()

    def _on_caret_move(self, event=None):
        self._update_status()

    def _log_console(self, text: str):
        self.console.configure(state="normal")
        self.console.insert("end", text)
        self.console.see("end")
        self.console.configure(state="normal")

def main():
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_quit)
    app.mainloop()

if __name__ == "__main__":
    main()

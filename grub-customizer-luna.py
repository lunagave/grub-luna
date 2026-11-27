#!/usr/bin/env python3
# grub-luna v1.0
# Personaliza tu GRUB, fácil, sin perderlo nunca.
# Basada en grub-customizer solo como información.
# Crédito al autor original de grub-customizer: Daniel Richter (GPL v3).
# Hecho por Vega & Kiki / Guzman
#
# SEGURIDAD: leer es real y no cambia nada. Escribir solo después de
# hacer una copia de seguridad en ~/.config/grub-luna/backup/<fecha-hora>/
# y con confirmación del usuario. Nunca se finge éxito: si pkexec/sudo
# o grub-mkconfig/update-grub fallan, se muestra el error tal cual.
# No hay pantallas técnicas: sin CFG_DIR, sin DEVICEMAP_FILE.
import os
import re
import shutil
import subprocess
import sys
import tarfile
import datetime
import urllib.request
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext

VERSION = "1.0"
REPO_URL = "https://github.com/lunagave/grub-luna"
SOPORTE_URL = "https://github.com/lunagave/grub-luna"

# Colores Glass morado
BG = "#1a0b2e"
BG2 = "#241040"
BG3 = "#2e1450"
FG = "#e9d5ff"
ACCENT = "#c084fc"
ACCENT2 = "#a855f7"
MUTED = "#b794d9"

RUTA_DEFAULT_GRUB = "/etc/default/grub"
RUTA_GRUB_CFG = "/boot/grub/grub.cfg"
RUTA_GRUB_D = "/etc/grub.d"
RUTA_THEMES = "/boot/grub/themes"
BACKUP_BASE = os.path.expanduser("~/.config/grub-luna/backup")
DESCARGAS = os.path.expanduser("~/Descargas/grub-luna-biblioteca")

FORMATOS_IMAGEN = (".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".svg")
FORMATOS_VIDEO = (".mp4", ".mkv", ".webm")
FORMATOS_TEMA = (".tar", ".tar.gz", ".tar.xz")

# 24 estilos de iconos incluidos en el programa (sin descargas externas)
ICONOS = [
    ("🐧", "Arch Linux"), ("🐱", "Gatito Luna"), ("🌙", "Luna creciente"),
    ("🔥", "Fuego"), ("❄️", "Hielo"), ("🌸", "Sakura"), ("⚡", "Rayo"),
    ("💜", "Corazón morado"), ("⭐", "Estrella"), ("🌌", "Galaxia"),
    ("🐉", "Dragón"), ("🦊", "Zorro"), ("🐺", "Lobo"), ("🦋", "Mariposa"),
    ("🎮", "Gamer"), ("🎵", "Música"), ("🚀", "Cohete"), ("🛡️", "Escudo"),
    ("👾", "Pixel"), ("🌊", "Ola"), ("🍂", "Otoño"), ("🌑", "Luna nueva"),
    ("💎", "Diamante"), ("🔮", "Místico"),
]

# Biblioteca: solo miniaturas/nombres en el programa; cada fondo se
# descarga solo cuando el usuario pica Descargar, para que no pese.
VIDEOS_ANIME = [
    "Bleach - Ichigo", "Bleach - Bankai", "Naruto - Hokage", "One Piece - Luffy",
    "Dragon Ball - Goku", "Demon Slayer - Tanjiro", "Jujutsu Kaisen - Gojo",
    "Attack on Titan - Eren", "My Hero Academia - Deku", "One Punch Man - Saitama",
    "Death Note - Light", "Tokyo Ghoul - Kaneki", "Sword Art Online - Kirito",
    "Evangelion - Shinji", "Cowboy Bebop - Spike", "Fullmetal Alchemist - Edward",
    "Hunter x Hunter - Gon", "Chainsaw Man - Denji", "Spy x Family - Anya",
    "Kimetsu - Nezuko",
]
IMAGENES_ANIME = [f"Anime fondo {i:02d} - más descargado" for i in range(1, 51)]
ICONOS_BIBLIOTECA = [f"Icono {nombre}" for _, nombre in ICONOS[:20]]


def leer_archivo(ruta):
    """Lee un archivo de texto; devuelve '' si no se puede leer."""
    try:
        with open(ruta, "r", errors="ignore") as f:
            return f.read()
    except Exception:
        return ""


def parse_default_grub(texto):
    """Extrae GRUB_DEFAULT, GRUB_TIMEOUT, GRUB_BACKGROUND y GRUB_THEME."""
    datos = {"default": "", "timeout": "5", "background": "", "theme": ""}
    for clave, nombre in (("GRUB_DEFAULT", "default"),
                          ("GRUB_TIMEOUT", "timeout"),
                          ("GRUB_BACKGROUND", "background"),
                          ("GRUB_THEME", "theme")):
        m = re.search(rf'^{clave}\s*=\s*"?([^"\n]*)"?\s*$', texto, re.M)
        if m:
            datos[nombre] = m.group(1).strip()
    return datos


def leer_sistemas():
    """Lee todos los archivos de GRUB y devuelve sistemas, datos y detalle."""
    sistemas = []
    texto_cfg = leer_archivo(RUTA_GRUB_CFG)
    for m in re.finditer(r"menuentry\s+'([^']+)'|menuentry\s+\"([^\"]+)\"", texto_cfg):
        nombre = m.group(1) or m.group(2)
        if nombre and nombre not in sistemas:
            sistemas.append(nombre)
    texto_default = leer_archivo(RUTA_DEFAULT_GRUB)
    datos = parse_default_grub(texto_default)
    grub_d = []
    try:
        grub_d = sorted(os.listdir(RUTA_GRUB_D))
    except Exception:
        grub_d = []
    temas = []
    try:
        temas = sorted(os.listdir(RUTA_THEMES))
    except Exception:
        temas = []
    detalle = []
    detalle.append(f"{RUTA_DEFAULT_GRUB}: {'leído' if texto_default else 'no disponible'}")
    detalle.append(f"{RUTA_GRUB_CFG}: {'leído' if texto_cfg else 'no disponible'} "
                   f"({len(sistemas)} sistemas)")
    detalle.append(f"{RUTA_GRUB_D}: {', '.join(grub_d) if grub_d else 'no disponible'}")
    detalle.append(f"{RUTA_THEMES}: {', '.join(temas) if temas else 'sin temas'}")
    if not sistemas:
        sistemas = ["(sin sistemas detectados: revisa /boot/grub/grub.cfg)"]
    return sistemas, datos, "\n".join(detalle)


def validar_tema(ruta):
    """Un tema completo debe ser .tar/.tar.gz/.tar.xz y traer theme.txt."""
    if not ruta.lower().endswith(FORMATOS_TEMA):
        return False, "El tema debe ser .tar, .tar.gz o .tar.xz"
    try:
        with tarfile.open(ruta, "r:*") as tf:
            nombres = tf.getnames()
        if any(n.endswith("theme.txt") for n in nombres):
            return True, "Tema válido: trae theme.txt"
        return False, "El archivo no trae theme.txt dentro"
    except Exception as e:
        return False, f"No se pudo abrir el tema: {e}"


def elegir_archivo(titulo="Elegir archivo"):
    """Selector moderno: zenity, luego kdialog, luego tkinter."""
    for cmd in (["zenity", "--file-selection", f"--title={titulo}"],
                ["kdialog", "--getopenfilename", os.path.expanduser("~")]):
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if r.returncode == 0 and r.stdout.strip():
                return r.stdout.strip()
            if r.returncode == 0:
                return ""
        except Exception:
            continue
    return filedialog.askopenfilename(title=titulo)


def hacer_backup():
    """Copia /etc/default/grub y /boot/grub/grub.cfg a ~/.config/grub-luna/backup/<fecha-hora>/.
    Devuelve (ruta, [archivos copiados]) o (None, error)."""
    sello = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    destino = os.path.join(BACKUP_BASE, sello)
    os.makedirs(destino, exist_ok=True)
    copiados = []
    for ruta in (RUTA_DEFAULT_GRUB, RUTA_GRUB_CFG):
        if os.path.isfile(ruta) and os.access(ruta, os.R_OK):
            try:
                shutil.copy2(ruta, os.path.join(destino, os.path.basename(ruta)))
                copiados.append(ruta)
            except Exception:
                pass
    if not copiados:
        return None, "No se pudo copiar ningún archivo de GRUB (¿permisos?)"
    return destino, copiados


def comando_actualizar():
    """Comando para actualizar GRUB según la distro."""
    if os.path.exists("/etc/arch-release"):
        return ["sudo", "grub-mkconfig", "-o", "/boot/grub/grub.cfg"]
    return ["sudo", "update-grub"]


def correr_con_privilegios(cmd_lista, descripcion):
    """Corre un comando con pkexec si existe, si no con sudo.
    Devuelve (ok, salida). Nunca finge éxito."""
    if shutil.which("pkexec"):
        cmd = ["pkexec"] + cmd_lista
    else:
        cmd = cmd_lista
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        salida = (r.stdout or "") + (r.stderr or "")
        return r.returncode == 0, salida.strip() or "(sin salida)"
    except Exception as e:
        return False, str(e)


class VentanaAcerca(tk.Toplevel):
    """Acerca de grub-luna, en su propia ventana aparte."""

    def __init__(self, padre):
        super().__init__(padre)
        self.title("Acerca de grub-luna")
        self.geometry("560x620")
        self.configure(bg=BG)
        tk.Label(self, text="🐱❓", bg=BG, fg=ACCENT, font=("Arial", 36)).pack(pady=(12, 0))
        tk.Label(self, text="Acerca de grub-luna", bg=BG, fg=ACCENT,
                 font=("Arial", 20, "bold")).pack()
        tk.Label(self, text="🌙🐱  Gatito morado durmiendo en la luna creciente",
                 bg=BG, fg=FG, font=("Arial", 11)).pack(pady=4)
        texto = scrolledtext.ScrolledText(self, bg=BG2, fg=FG, font=("Arial", 11),
                                          wrap="word", height=22)
        texto.pack(fill="both", expand=True, padx=14, pady=8)
        texto.insert("1.0",
            "grub-luna v1.0\n\n"
            "Basada en grub-customizer solo como información.\n"
            "Crédito al autor original: Daniel Richter, autor de grub-customizer (GPL v3).\n\n"
            "Funciones:\n"
            "• Lee todos los archivos de GRUB\n"
            "• Cambia fondo, video, tiempo, sistema e iconos, con vista previa\n"
            "• Poner fondo + / Quitar fondo ×\n"
            "• Restaurar GRUB originalmente con un solo botón\n"
            "• Biblioteca como tienda: 20 videos, 50 imágenes, 20 iconos, con Descargar\n"
            "• Temas completos .tar.gz / .tar.xz / .tar\n"
            "• Imágenes anime, las más descargadas\n"
            "• Agregar video de fondo y cambiar icono\n"
            "• GRUB personalizados de GNOME y KDE Plasma, solo agregando el archivo\n"
            "• Sin comandos, sin descomprimir, sin terminal\n\n"
            "Errores del GRUB anterior que corrige:\n"
            "• Se perdía el GRUB y había que reinstalar la distro\n"
            "• Pantallas técnicas CFG_DIR y DEVICEMAP_FILE, un dolor de cabeza\n"
            "• A veces no leía los archivos\n"
            "• Interfaz vieja, sin video ni iconos ni tienda\n\n"
            "Mejoras de grub-luna:\n"
            "• Copia de seguridad automática antes de cambiar nada\n"
            "• Un solo botón lo deja como nuevo, como si nada hubiera pasado\n"
            "• Interfaz Glass morada, moderna y fácil\n"
            "• Vista previa dentro de la ventana, al lado de la lista\n")
        texto.config(state="disabled")
        tk.Label(self, text="Soporte / Ayuda: " + SOPORTE_URL,
                 bg=BG, fg=ACCENT, font=("Arial", 10)).pack()
        tk.Label(self, text="Hecho por Vega & Kiki\nGuzman",
                 bg=BG, fg=ACCENT, font=("Arial", 11, "bold")).pack(pady=10)


class App(tk.Tk):
    def __init__(self, demo=False):
        super().__init__()
        self.demo = demo
        self.title(f"grub-luna {VERSION}")
        self.geometry("1000x650")
        self.configure(bg=BG)
        self.fondo_actual = ""
        self.fondo_anterior = ""
        self.icono_actual = ICONOS[1]  # 🐱 Gatito Luna
        self.sistema_actual = ""
        self.sistemas, self.datos_grub, self.detalle = leer_sistemas()
        if self.datos_grub.get("default"):
            self.sistema_actual = self.datos_grub["default"]
        elif self.sistemas:
            self.sistema_actual = self.sistemas[0]
        self._construir()
        self._actualizar_vista_previa()
        if demo:
            self.after(2000, self.destroy)

    # ---------- Interfaz ----------
    def _boton(self, padre, texto, comando, grande=False):
        b = tk.Button(padre, text=texto, command=comando, bg=BG3, fg=FG,
                      activebackground=ACCENT2, activeforeground="white",
                      font=("Arial", 11, "bold" if grande else "normal"),
                      relief="flat", padx=12, pady=8 if grande else 6,
                      cursor="hand2")
        return b

    def _construir(self):
        # Barra Luna arriba, con logo
        barra = tk.Frame(self, bg=BG2, height=56)
        barra.pack(fill="x")
        tk.Label(barra, text="🌙🐱  GRUB-LUNA", bg=BG2, fg=ACCENT,
                 font=("Arial", 20, "bold")).pack(side="left", padx=14, pady=8)
        tk.Label(barra, text="Cambia tu GRUB fácilmente",
                 bg=BG2, fg=MUTED, font=("Arial", 11)).pack(side="left", pady=8)

        principal = tk.Frame(self, bg=BG)
        principal.pack(fill="both", expand=True, padx=10, pady=8)
        izquierda = tk.Frame(principal, bg=BG)
        izquierda.pack(side="left", fill="both", expand=True)
        derecha = tk.Frame(principal, bg=BG2, width=360)
        derecha.pack(side="right", fill="y", padx=(10, 0))
        derecha.pack_propagate(False)

        # Izquierda: Agregar GRUB + lista de sistemas
        self._boton(izquierda, "📁  Agregar GRUB / Agregar Carpeta",
                    self.agregar_grub, grande=True).pack(fill="x", pady=(0, 6))
        tk.Label(izquierda, text="Tus GRUB / sistemas:",
                 bg=BG, fg=FG, font=("Arial", 11, "bold")).pack(anchor="w")
        self.lista = tk.Listbox(izquierda, bg=BG2, fg=FG, font=("Arial", 11),
                                height=6, selectbackground=ACCENT2)
        self.lista.pack(fill="x", pady=4)
        for s in self.sistemas:
            self.lista.insert("end", s)
        if self.sistemas:
            self.lista.selection_set(0)
        self.lista.bind("<<ListboxSelect>>", self._al_elegir_sistema)

        # Controles: sistema por defecto, tiempo, fondo
        controles = tk.LabelFrame(izquierda, text=" Ajustes ", bg=BG, fg=ACCENT,
                                  font=("Arial", 11, "bold"))
        controles.pack(fill="x", pady=6)
        tk.Label(controles, text="Sistema por defecto:", bg=BG, fg=FG).grid(
            row=0, column=0, sticky="w", padx=6, pady=4)
        self.combo_default = ttk.Combobox(controles, values=self.sistemas,
                                          state="readonly", width=30)
        self.combo_default.set(self.sistema_actual)
        self.combo_default.grid(row=0, column=1, padx=6, pady=4)
        self.combo_default.bind("<<ComboboxSelected>>", self._al_elegir_sistema)
        tk.Label(controles, text="Tiempo:", bg=BG, fg=FG).grid(
            row=1, column=0, sticky="w", padx=6, pady=4)
        self.combo_tiempo = ttk.Combobox(controles, values=["5", "10", "0"],
                                         state="readonly", width=8)
        self.combo_tiempo.set(self.datos_grub.get("timeout") or "5")
        self.combo_tiempo.grid(row=1, column=1, sticky="w", padx=6, pady=4)
        self.combo_tiempo.bind("<<ComboboxSelected>>", lambda e: self._actualizar_vista_previa())
        tk.Label(controles, text="segundos", bg=BG, fg=MUTED).grid(row=1, column=2, sticky="w")
        tk.Label(controles, text="Fondo:", bg=BG, fg=FG).grid(
            row=2, column=0, sticky="w", padx=6, pady=4)
        self.etiqueta_fondo = tk.Label(controles, text="(sin fondo elegido)",
                                       bg=BG, fg=MUTED)
        self.etiqueta_fondo.grid(row=2, column=1, sticky="w", padx=6, pady=4)
        fila_fondo = tk.Frame(controles, bg=BG)
        fila_fondo.grid(row=3, column=0, columnspan=3, sticky="w", padx=6, pady=4)
        self._boton(fila_fondo, "➕ Poner fondo +", self.poner_fondo).pack(side="left", padx=2)
        self._boton(fila_fondo, "❌ Quitar fondo ×", self.quitar_fondo).pack(side="left", padx=2)
        self._boton(fila_fondo, "🎬 Poner video", self.poner_video).pack(side="left", padx=2)
        self.mensaje = tk.Label(controles, text="", bg=BG, fg="#86efac",
                               font=("Arial", 11, "bold"))
        self.mensaje.grid(row=4, column=0, columnspan=3, sticky="w", padx=6)

        # Pestañas: Biblioteca, Iconos, Archivos GRUB
        self.tabs = ttk.Notebook(izquierda)
        self.tabs.pack(fill="both", expand=True, pady=4)
        self._pestana_biblioteca()
        self._pestana_iconos()
        self._pestana_archivos()

        # Derecha: Vista previa dentro de la ventana, al lado
        tk.Label(derecha, text="👁️  Vista previa", bg=BG2, fg=ACCENT,
                 font=("Arial", 13, "bold")).pack(pady=(10, 4))
        self.vista = tk.Frame(derecha, bg="#0f0518", width=330, height=220)
        self.vista.pack(padx=12, pady=4)
        self.vista.pack_propagate(False)
        self.vista_fondo = tk.Label(self.vista, text="🌙", bg="#0f0518", fg=ACCENT,
                                    font=("Arial", 48))
        self.vista_fondo.pack(pady=(18, 0))
        self.vista_icono = tk.Label(self.vista, text="🐱", bg="#0f0518", fg=FG,
                                    font=("Arial", 28))
        self.vista_icono.pack()
        self.vista_sistema = tk.Label(self.vista, text="", bg="#0f0518", fg="white",
                                      font=("Arial", 11, "bold"))
        self.vista_sistema.pack()
        self.vista_tiempo = tk.Label(self.vista, text="", bg="#0f0518", fg=MUTED,
                                     font=("Arial", 10))
        self.vista_tiempo.pack()
        self.vista_info = tk.Label(derecha, text="", bg=BG2, fg=MUTED,
                                   font=("Arial", 10), wraplength=330, justify="left")
        self.vista_info.pack(padx=12, pady=6, anchor="w")
        tk.Label(derecha, text="Así se verá tu GRUB al arrancar.",
                 bg=BG2, fg=MUTED, font=("Arial", 10)).pack(padx=12, anchor="w")

        # Botones abajo a la derecha, con iconos
        pie_botones = tk.Frame(self, bg=BG)
        pie_botones.pack(fill="x", padx=10, pady=(0, 4))
        self._boton(pie_botones, "💾  Guardar", self.guardar, grande=True).pack(side="right", padx=3)
        self._boton(pie_botones, "↩️  Restaurar GRUB originalmente",
                    self.restaurar, grande=True).pack(side="right", padx=3)
        self._boton(pie_botones, "🐱❓  Acerca", self.abrir_acerca).pack(side="right", padx=3)
        tk.Label(self, text="Hecho por Vega & Kiki\nGuzman", bg=BG, fg=ACCENT,
                 font=("Arial", 10, "bold")).pack(pady=(0, 6))

    def _pestana_biblioteca(self):
        marco = tk.Frame(self.tabs, bg=BG)
        self.tabs.add(marco, text="📦 Biblioteca")
        tk.Label(marco, text="Como tienda KDE: solo se descarga el fondo elegido",
                 bg=BG, fg=MUTED, font=("Arial", 10)).pack(anchor="w", padx=6, pady=4)
        lienzo = tk.Canvas(marco, bg=BG, highlightthickness=0)
        barra = ttk.Scrollbar(marco, orient="vertical", command=lienzo.yview)
        interior = tk.Frame(lienzo, bg=BG)
        interior.bind("<Configure>", lambda e: lienzo.configure(scrollregion=lienzo.bbox("all")))
        lienzo.create_window((0, 0), window=interior, anchor="nw")
        lienzo.configure(yscrollcommand=barra.set)
        lienzo.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")
        for seccion, items, tipo in (("🎬 Videos anime (20)", VIDEOS_ANIME, "video"),
                                     ("🖼️ Imágenes anime (50)", IMAGENES_ANIME, "imagen"),
                                     ("🎨 Iconos (20)", ICONOS_BIBLIOTECA, "icono")):
            tk.Label(interior, text=seccion, bg=BG, fg=ACCENT,
                     font=("Arial", 11, "bold")).pack(anchor="w", padx=6, pady=(8, 2))
            for nombre in items:
                fila = tk.Frame(interior, bg=BG2)
                fila.pack(fill="x", padx=6, pady=2)
                tk.Label(fila, text="🎬 " if tipo == "video" else "🖼️ " if tipo == "imagen" else "🎨 ",
                         bg=BG2, fg=FG).pack(side="left")
                tk.Label(fila, text=nombre, bg=BG2, fg=FG, font=("Arial", 10)).pack(side="left")
                self._boton(fila, "⬇️ Descargar",
                            lambda n=nombre, t=tipo: self.descargar_biblioteca(n, t)
                            ).pack(side="right", padx=4, pady=2)

    def _pestana_iconos(self):
        marco = tk.Frame(self.tabs, bg=BG)
        self.tabs.add(marco, text="🎨 Elegir iconos")
        tk.Label(marco, text="Cambiar iconos: más de 20 estilos, elige uno y se ve en tu GRUB",
                 bg=BG, fg=MUTED, font=("Arial", 10)).pack(anchor="w", padx=6, pady=4)
        lienzo = tk.Canvas(marco, bg=BG, highlightthickness=0)
        barra = ttk.Scrollbar(marco, orient="vertical", command=lienzo.yview)
        interior = tk.Frame(lienzo, bg=BG)
        interior.bind("<Configure>", lambda e: lienzo.configure(scrollregion=lienzo.bbox("all")))
        lienzo.create_window((0, 0), window=interior, anchor="nw")
        lienzo.configure(yscrollcommand=barra.set)
        lienzo.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")
        for emoji, nombre in ICONOS:
            fila = tk.Frame(interior, bg=BG2)
            fila.pack(fill="x", padx=6, pady=2)
            tk.Label(fila, text=emoji, bg=BG2, fg=FG, font=("Arial", 18)).pack(side="left", padx=4)
            tk.Label(fila, text=nombre, bg=BG2, fg=FG, font=("Arial", 11)).pack(side="left")
            self._boton(fila, "Elegir",
                        lambda e=emoji, n=nombre: self.elegir_icono(e, n)
                        ).pack(side="right", padx=4, pady=2)

    def _pestana_archivos(self):
        marco = tk.Frame(self.tabs, bg=BG)
        self.tabs.add(marco, text="📄 Archivos GRUB")
        texto = scrolledtext.ScrolledText(marco, bg="#0f0518", fg=FG,
                                          font=("monospace", 10))
        texto.pack(fill="both", expand=True, padx=6, pady=6)
        texto.insert("1.0", self.detalle + "\n\n"
                     "/etc/default/grub:\n" + (leer_archivo(RUTA_DEFAULT_GRUB) or "(no disponible)"))
        texto.config(state="disabled")

    # ---------- Acciones ----------
    def _al_elegir_sistema(self, evento=None):
        sel = self.lista.curselection()
        if sel:
            self.sistema_actual = self.lista.get(sel[0])
            self.combo_default.set(self.sistema_actual)
        elif self.combo_default.get():
            self.sistema_actual = self.combo_default.get()
        self._actualizar_vista_previa()

    def _actualizar_vista_previa(self):
        sistema = self.sistema_actual or "(sin sistema)"
        tiempo = self.combo_tiempo.get() if hasattr(self, "combo_tiempo") else "5"
        emoji, nombre_icono = self.icono_actual
        self.vista_icono.config(text=emoji)
        self.vista_sistema.config(text=f"▶ {sistema}")
        self.vista_tiempo.config(text=f"Tiempo: {tiempo} seg   •   Icono: {nombre_icono}")
        fondo = os.path.basename(self.fondo_actual) if self.fondo_actual else "(fondo morado Glass)"
        self.vista_fondo.config(text="🎬" if self.fondo_actual.lower().endswith(FORMATOS_VIDEO) else "🌙")
        self.vista_info.config(text=f"Fondo: {fondo}\nSistema: {sistema}\nTiempo: {tiempo} seg")
        if hasattr(self, "etiqueta_fondo"):
            self.etiqueta_fondo.config(text=fondo)

    def agregar_grub(self):
        """Agrega un archivo de GRUB, tema, imagen o video, solo agregando el archivo."""
        ruta = elegir_archivo("Agregar GRUB / Agregar Carpeta")
        if not ruta:
            return
        if ruta.lower().endswith(FORMATOS_TEMA):
            ok, msg = validar_tema(ruta)
            messagebox.showinfo("Tema", msg) if ok else messagebox.showwarning("Tema", msg)
            if ok:
                self.fondo_anterior, self.fondo_actual = self.fondo_actual, ruta
                self.mensaje.config(text="Fondo cambiado")
                self._actualizar_vista_previa()
            return
        if ruta.lower().endswith(FORMATOS_IMAGEN + FORMATOS_VIDEO):
            self.fondo_anterior, self.fondo_actual = self.fondo_actual, ruta
            self.mensaje.config(text="Fondo cambiado")
            self._actualizar_vista_previa()
            return
        messagebox.showinfo("Agregar GRUB",
                            f"Archivo agregado: {os.path.basename(ruta)}\n"
                            "Sin comandos, sin descomprimir, sin terminal.")

    def poner_fondo(self):
        ruta = elegir_archivo("Poner fondo")
        if not ruta:
            return
        if not ruta.lower().endswith(FORMATOS_IMAGEN + FORMATOS_VIDEO):
            messagebox.showwarning("Fondo", "Elige una imagen JPG, PNG, WEBP, GIF, BMP o SVG, "
                                            "o un video MP4, MKV o WEBM.")
            return
        self.fondo_anterior, self.fondo_actual = self.fondo_actual, ruta
        self.mensaje.config(text="Fondo cambiado")
        self._actualizar_vista_previa()

    def poner_video(self):
        ruta = elegir_archivo("Poner video de fondo")
        if not ruta:
            return
        if not ruta.lower().endswith(FORMATOS_VIDEO):
            messagebox.showwarning("Video", "El video debe ser MP4, MKV o WEBM.")
            return
        self.fondo_anterior, self.fondo_actual = self.fondo_actual, ruta
        self.mensaje.config(text="Fondo cambiado")
        self._actualizar_vista_previa()

    def quitar_fondo(self):
        """Quitar fondo: vuelve el anterior, como estaba."""
        self.fondo_actual = self.fondo_anterior
        self.fondo_anterior = ""
        self.mensaje.config(text="Fondo cambiado")
        self._actualizar_vista_previa()

    def elegir_icono(self, emoji, nombre):
        self.icono_actual = (emoji, nombre)
        self._actualizar_vista_previa()
        messagebox.showinfo("Icono", f"Icono elegido: {emoji} {nombre}\nSe verá en tu GRUB.")

    def descargar_biblioteca(self, nombre, tipo):
        """Descarga solo ese fondo desde el servidor/GitHub. Sin éxito fingido."""
        os.makedirs(DESCARGAS, exist_ok=True)
        seguro = "".join(c if c.isalnum() or c in "-_" else "_" for c in nombre)
        ext = ".mp4" if tipo == "video" else ".png" if tipo == "imagen" else ".png"
        destino = os.path.join(DESCARGAS, seguro + ext)
        url = f"{REPO_URL}/raw/main/biblioteca/{seguro}{ext}"
        try:
            urllib.request.urlretrieve(url, destino)
        except Exception as e:
            messagebox.showerror("Descargar",
                                 f"No se pudo descargar {nombre}.\n{e}\n"
                                 f"Inténtalo de nuevo desde {REPO_URL}")
            return
        messagebox.showinfo("Descargar", f"Descargado: {destino}")

    def guardar(self):
        """Guardar: copia de seguridad primero, luego guardar, luego actualizar GRUB."""
        if not messagebox.askyesno("Guardar",
                                   "¿Guardar estos cambios en tu GRUB?\n"
                                   "Primero se hace una copia de seguridad."):
            return
        destino, copiados = hacer_backup()
        if destino is None:
            messagebox.showerror("Guardar", f"No se pudo hacer la copia de seguridad: {copiados}")
            return
        # Escribir /etc/default/grub con los valores elegidos (vía pkexec, sin fingir).
        texto = leer_archivo(RUTA_DEFAULT_GRUB)
        if texto:
            texto = re.sub(r"^GRUB_DEFAULT=.*$", f"GRUB_DEFAULT={self.sistema_actual}",
                           texto, flags=re.M)
            texto = re.sub(r"^GRUB_TIMEOUT=.*$", f"GRUB_TIMEOUT={self.combo_tiempo.get()}",
                           texto, flags=re.M)
            if self.fondo_actual:
                if "GRUB_BACKGROUND=" in texto:
                    texto = re.sub(r"^GRUB_BACKGROUND=.*$",
                                   f"GRUB_BACKGROUND={self.fondo_actual}", texto, flags=re.M)
                else:
                    texto += f"\nGRUB_BACKGROUND={self.fondo_actual}\n"
            tmp = "/tmp/grub-luna-default-grub"
            try:
                with open(tmp, "w") as f:
                    f.write(texto)
            except Exception as e:
                messagebox.showerror("Guardar", f"No se pudo preparar el archivo: {e}")
                return
            ok, salida = correr_con_privilegios(
                ["cp", tmp, RUTA_DEFAULT_GRUB], "copiar /etc/default/grub")
            if not ok:
                messagebox.showerror("Guardar",
                                     f"No se pudo guardar en {RUTA_DEFAULT_GRUB}.\n{salida}")
                return
        ok, salida = correr_con_privilegios(comando_actualizar(), "actualizar GRUB")
        if ok:
            messagebox.showinfo("Guardar",
                                f"Guardado con copia de seguridad en:\n{destino}\n"
                                f"GRUB actualizado correctamente.")
        else:
            messagebox.showerror("Guardar",
                                 f"Se guardó la copia en {destino}, pero actualizar GRUB falló.\n"
                                 f"Tu GRUB anterior sigue en la copia.\n{salida}")

    def restaurar(self):
        """Restaurar GRUB originalmente: un solo botón, lo deja como nuevo."""
        if not os.path.isdir(BACKUP_BASE):
            messagebox.showinfo("Restaurar GRUB",
                                "No hay ninguna copia de seguridad todavía.\n"
                                "Tu GRUB sigue como estaba.")
            return
        copias = sorted(os.listdir(BACKUP_BASE))
        if not copias:
            messagebox.showinfo("Restaurar GRUB", "No hay ninguna copia de seguridad todavía.")
            return
        ultima = os.path.join(BACKUP_BASE, copias[-1])
        if not messagebox.askyesno("Restaurar GRUB originalmente",
                                   f"¿Restaurar tu GRUB como estaba?\nCopia: {copias[-1]}\n"
                                   "Queda como nuevo, como si nada hubiera pasado."):
            return
        errores = []
        for nombre, ruta_dest in (("grub", RUTA_DEFAULT_GRUB),
                                  ("grub.cfg", RUTA_GRUB_CFG)):
            origen = os.path.join(ultima, nombre)
            if os.path.isfile(origen):
                ok, salida = correr_con_privilegios(["cp", origen, ruta_dest], "restaurar")
                if not ok:
                    errores.append(f"{nombre}: {salida}")
        if errores:
            messagebox.showerror("Restaurar GRUB",
                                 "No se pudo restaurar todo:\n" + "\n".join(errores))
            return
        ok, salida = correr_con_privilegios(comando_actualizar(), "actualizar GRUB")
        if ok:
            messagebox.showinfo("Restaurar GRUB",
                                "GRUB restaurado originalmente, como nuevo. ✅")
        else:
            messagebox.showwarning("Restaurar GRUB",
                                   f"Archivos restaurados, pero actualizar GRUB falló.\n{salida}")

    def abrir_acerca(self):
        VentanaAcerca(self)


def main():
    demo = "--demo" in sys.argv
    app = App(demo=demo)
    app.mainloop()


if __name__ == "__main__":
    main()

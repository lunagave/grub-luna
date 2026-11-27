# 🌙 grub-luna v1.0
Personaliza tu GRUB, fácil, sin perderlo nunca.
Basada en grub-customizer solo como información, crédito a Daniel Richter, su autor original.
Hecho por Vega & Kiki / Guzman

## 🔄 Diferencias: GRUB viejo y nuevo
- ❌ Viejo: se perdía el GRUB, había que reinstalar la distro | ✅ Nuevo: un solo botón Restaurar GRUB, queda como nuevo
- ❌ Viejo: pantallas técnicas CFG_DIR, DEVICEMAP_FILE, dolor de cabeza | ✅ Nuevo: sin pantallas técnicas, fácil, sin terminal
- ❌ Viejo: a veces no leía los archivos | ✅ Nuevo: lee todos los archivos de GRUB, verifica y hace copia de seguridad
- ❌ Viejo: interfaz vieja, GTK3 | ✅ Nuevo: interfaz Glass morada, moderna, con barrita Luna
- ❌ Viejo: sin video, sin iconos, sin tienda | ✅ Nuevo: video de fondo, Cambiar iconos con más de 20 estilos, Biblioteca como tienda con Descargar

## ✨ Funciones
- 📖 Lee todos los archivos de GRUB
- 📁 Agregar GRUB / Agregar Carpeta
- ➕ Poner fondo + / ❌ Quitar fondo ×
- ↩️ Restaurar GRUB originalmente, con un solo botón
- 🎨 Cambiar iconos, más de 20 estilos, con vista previa
- 🎬 Video como fondo del GRUB
- 📦 Biblioteca: 20 videos, 50 imágenes, 20 iconos, los de anime más descargados, con botón Descargar como tienda KDE
- 🗂️ Tipos: .tar.gz, .tar.xz, .tar, JPG, PNG, WEBP, MP4, MKV
- 🎨 GRUB personalizados de GNOME y KDE Plasma, solo agregar archivo
- 🚫 Sin comandos, sin descomprimir, sin terminal
- 💾 Guardar con copia de seguridad
- ❓ Acerca, con gatito negro y ?, basada, funciones, errores del anterior GRUB y mejoras
- 🆘 Soporte / Ayuda: https://github.com/lunagave/grub-luna

## 🗂️ Todo tipo de archivos
- Temas completos: .tar, .tar.gz, .tar.xz, con theme.txt, iconos y fuentes
- Imágenes de fondo: .png, .jpg / .jpeg, .tga
- Tipografías: fuentes del sistema o .pf2
- Archivos del sistema: /etc/default/grub, /etc/grub.d/, /boot/grub/grub.cfg, /boot/grub/themes/

## 🚀 Mejoras
- No se pierde el GRUB, con un solo botón se restaura como nuevo
- Copia de seguridad automática antes de cambiar nada
- Sin pantallas técnicas, sin CFG_DIR, sin DEVICEMAP_FILE
- Interfaz Glass morada, moderna, fácil, sin terminal
- Video como fondo, iconos, temas, Biblioteca como tienda con Descargar

## 💻 Comandos
### 🐧 Arch Pacman
```bash
sudo pacman -S --needed --noconfirm zenity && curl -L https://github.com/lunagave/grub-luna/raw/main/grub-luna-launcher1.zip -o ~/Descargas/grub-luna-launcher1.zip && cd ~/Descargas && unzip -o grub-luna-launcher1.zip && makepkg -si && bash ~/Descargas/grub-luna-installer.sh
```
### 🟠 Debian / Ubuntu .deb
```bash
curl -L https://github.com/lunagave/grub-luna/raw/main/grub-luna_1.0_all.deb -o ~/Descargas/grub-luna_1.0_all.deb && cd ~/Descargas && sudo dpkg -i grub-luna_1.0_all.deb && sudo apt install -f
```
### 💻 Actualiza tu GRUB
Arch:
```bash
sudo grub-mkconfig -o /boot/grub/grub.cfg
```
Debian/Ubuntu:
```bash
sudo update-grub
```

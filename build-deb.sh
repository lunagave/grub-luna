#!/bin/bash
set -e
rm -rf grub-luna-deb
mkdir -p grub-luna-deb/usr/bin grub-luna-deb/usr/share/applications grub-luna-deb/usr/lib/grub-luna grub-luna-deb/usr/share/grub-luna grub-luna-deb/DEBIAN
cp grub-customizer-luna.py grub-luna-deb/usr/bin/grub-luna
chmod +x grub-luna-deb/usr/bin/grub-luna
cp grub-luna-installer-gui.py grub-luna-deb/usr/lib/grub-luna/
cp grub-luna-installer.sh grub-luna-deb/usr/lib/grub-luna/ 2>/dev/null || true
cp grub-luna.desktop grub-luna-deb/usr/share/applications/
cp media-generation-grub-luna-instalador-paso1-gat-0-495f56c1-d29f-4f76-b53d-2d01f8e39382.webp grub-luna-deb/usr/share/grub-luna/paso1.webp
cp media-generation-grub-luna-instalador-paso2-0-3d175b6d-011a-4cb3-b1cd-a42609e09cbe.webp grub-luna-deb/usr/share/grub-luna/paso2.webp
cp media-generation-grub-luna-instalador-paso3-0-18937017-82fd-44d6-a909-795352141355.webp grub-luna-deb/usr/share/grub-luna/paso3.webp
cat > grub-luna-deb/DEBIAN/control <<'EOF'
Package: grub-luna
Version: 1.0
Section: utils
Priority: optional
Architecture: all
Depends: python3, python3-tk, python3-pil, zenity, grub-common
Maintainer: Fernando <lunagave>
Description: Personaliza tu GRUB, fácil, sin perderlo nunca
EOF
chmod 755 grub-luna-deb/DEBIAN
dpkg-deb --build grub-luna-deb grub-luna_1.0_all.deb
echo "Listo: grub-luna_1.0_all.deb"

# Maintainer: Fernando <lunagave>
pkgname=grub-luna
pkgver=1.0
pkgrel=1
pkgdesc="Personaliza tu GRUB, fácil, sin perderlo nunca"
arch=('any')
url="https://github.com/lunagave/grub-luna"
license=('GPL3')
depends=('python' 'python-pillow' 'tk' 'zenity' 'grub')
source=('grub-customizer-luna.py' 'grub-luna-installer-gui.py' 'grub-luna.desktop'
        'media-generation-grub-luna-instalador-paso1-gat-0-495f56c1-d29f-4f76-b53d-2d01f8e39382.webp'
        'media-generation-grub-luna-instalador-paso2-0-3d175b6d-011a-4cb3-b1cd-a42609e09cbe.webp'
        'media-generation-grub-luna-instalador-paso3-0-18937017-82fd-44d6-a909-795352141355.webp')
sha256sums=('6949dd855740a4d1b3cd8139119851b8762d9eb162ec2d1e45c4bf7314826867'
            'e4e22f30a9c76f8a8f16c0b30bfef63656c420396d72a0cb0b19df60a513597f'
            'd9c9c3cadacc96ffe65b6042e0297d2209dfe8b45e9796062f885edbe6ba41fd'
            '200d4b003916e200a90d3becb5600ae61e7e665573ebe49260ee94a069b4f177'
            'e7f2671eab274c1ee2b4c2fca700afc15ba7ce3d3fd0c6c21445aeeb62876b61'
            '27ab9214bbb2e7999b3ea735450732b19f3ebb086e64687fd6ce87382f3e7525')
package() {
  install -Dm755 grub-customizer-luna.py "$pkgdir/usr/bin/grub-luna"
  install -Dm755 grub-luna-installer-gui.py "$pkgdir/usr/lib/grub-luna/grub-luna-installer-gui.py"
  install -Dm644 grub-luna.desktop "$pkgdir/usr/share/applications/grub-luna.desktop"
  install -Dm644 media-generation-grub-luna-instalador-paso1-gat-0-495f56c1-d29f-4f76-b53d-2d01f8e39382.webp "$pkgdir/usr/share/grub-luna/paso1.webp"
  install -Dm644 media-generation-grub-luna-instalador-paso2-0-3d175b6d-011a-4cb3-b1cd-a42609e09cbe.webp "$pkgdir/usr/share/grub-luna/paso2.webp"
  install -Dm644 media-generation-grub-luna-instalador-paso3-0-18937017-82fd-44d6-a909-795352141355.webp "$pkgdir/usr/share/grub-luna/paso3.webp"
  install -Dm644 biblioteca/Anime_fondo_*.png -t "$pkgdir/usr/share/grub-luna/biblioteca/"
  install -Dm644 biblioteca/Icono_*.png -t "$pkgdir/usr/share/grub-luna/biblioteca/"
}

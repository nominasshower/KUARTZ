#!/bin/bash
# Corre este script dentro de la carpeta img/
# En Windows usa Git Bash o WSL

echo "Descargando imágenes de Küartz..."

curl -L "https://kuartzsurfaces.com/wp-content/uploads/2021/08/calacatta_bengala_img-destacada.jpg" -o "calacatta-bengala.jpg"
curl -L "https://kuartzsurfaces.com/wp-content/uploads/2020/12/about-us.png" -o "about-us.png"
curl -L "https://kuartzsurfaces.com/wp-content/uploads/2020/12/Recurso-4.png" -o "kitchen-countertops.png"
curl -L "https://kuartzsurfaces.com/wp-content/uploads/2020/12/vanity-tops.png" -o "vanity-tops.png"
curl -L "https://kuartzsurfaces.com/wp-content/uploads/2020/12/Recurso-5.png" -o "surroundings.png"
curl -L "https://kuartzsurfaces.com/wp-content/uploads/2020/11/marquina-color-chip.png" -o "marquina.png"
curl -L "https://kuartzsurfaces.com/wp-content/uploads/2021/08/single_product-5.jpg" -o "calacatta-lincoln.jpg"
curl -L "https://kuartzsurfaces.com/wp-content/uploads/2020/12/galaxy-white-color-chip.png" -o "galaxy-white.png"
curl -L "https://kuartzsurfaces.com/wp-content/uploads/2020/12/pure-white-color-chip-1.png" -o "pure-white.png"
curl -L "https://kuartzsurfaces.com/wp-content/uploads/2020/12/calacatta-statuario-color-chip.png" -o "calacatta-statuario.png"
curl -L "https://kuartzsurfaces.com/wp-content/uploads/2021/01/catalogo-mobile.png" -o "catalogo.png"

echo ""
echo "=== LISTO ==="
echo "11 imágenes descargadas."

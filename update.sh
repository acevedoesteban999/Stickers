#! /bin/bash
#echo ""
#echo "========== Iniciando Proceso de Actualización =========="
#echo ""
#cd ../opt/python/django/Stickers
#./update.sh
set -e
echo ""
echo "========== Accediendo a la Carpeta de Stickers =========="
echo ""
cd ../opt/python/django/Stickers
echo ""
echo "========== Accediendo al Entorno Virtual =========="
echo ""
source .venv/bin/activate
echo ""
echo "========== Actualizando remotamente de Github.com/Esteban1914/Stickers/ =========="
echo ""
git pull origin master
echo ""
echo "========== Dando Permisos =========="
chmod 777 update.sh
echo "========== Permisos Asignados =========="
echo ""
echo "========== Haciendo Migraciones en la Base de Datos =========="
echo ""
python manage.py makemigrations
python manage.py migrate
echo ""
echo "========== Reiniciando Apache =========="
echo ""
systemctl restart apache2
echo ""
echo "========== Completado! Se ha actualizado correctamente =========="
echo ""

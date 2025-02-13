# Activar conda:

conda activate mi_entorno_django

# Crear nuevo proyecto:

django-admin startproject nombre_del_proyecto

# Crear aplicación:

py manage.py startapp members

# Creación de 1era migración:

python manage.py makemigrations nombre_de_la_aplicacion

# Crear archivos migración:

py manage.py makemigrations

# Verificar 1era migración:

python manage.py showmigrations

# Ejecutar migraciones:

python manage.py migrate

# Ver SQL:

py manage.py sqlmigrate members 0001

# Abrir Shell de Python:

py manage.py shell

# Ejecutar servidor:

py manage.py runserver

# Dependencias:

pip install Jinja2 django-jinja


Vino Tinto (Fuego): Representa vinos fuertes y potentes, como el fuego.

Vino Blanco (Nieve): Representa vinos frescos y ligeros, como la nieve.

Vino Rosado (Agua): Representa vinos suaves y fluidos, como el agua.


# Crear admin:

python manage.py createsuperuser

# Añadir vino automatica:

python manage.py add_wine

Le projet Bubble-Time est un site ecommerce destiner à proposer un menu de boisson bubble tea, il  contient les pages:
    -menu
    -inscription
    -connexion
    -profil
    -admin

Ce projet a été réaliser en groupe de 3 avec comme intervenant: JMOUR Dhia, LADJOUI Mariam et BESROUR Mohamed

Voici le guide d'installation:

1--> python -m venv venv

2--> source venv/Scripts/activate
	deactivate

3--> pip install django

4--> django-admin startproject bubble_time

5--> cd bubble_time/

6--> python manage.py startapp my_app

7--> pip install mysqlclient

8--> python manage.py migrate

9--> python manage.py runserver


vérifier les installations
python --version
django-admin --version
pip show django
pip show mysqlclient


Commande pour lancer l'environnement virtuel
\GitHub\BUBBLE-TIME> .\venv\Scripts\Activate.ps1
(venv) \GitHub\BUBBLE-TIME> cd src
(venv) \GitHub\BUBBLE-TIME\src> python manage.py runserver
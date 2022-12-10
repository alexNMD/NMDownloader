# fichier permettant le l'ensemble des différents scripts périodiques de l'application
import sys
import os

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.append(f'{path}/scripts/')

from scrapper import parse_data
from link_uptader import update_link

# lancement de la récupération des nouvelles données
parse_data()

# recherche des liens morts afin de les remplacer
update_link()

# amélioration de la qualité des liens
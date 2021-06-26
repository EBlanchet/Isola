# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 00:37:55 2020

@author: Jeanne et Elise
"""
#############################################################################
# MODULES A CHARGER                                                         #
#############################################################################
from doctest import testmod

from random import randint

from fltk import cree_fenetre,\
                    ferme_fenetre,\
                    mise_a_jour,\
                    abscisse_souris,\
                    ordonnee_souris,\
                    donne_ev, \
                    type_ev, \
                    rectangle,\
                    cercle,\
                    texte,\
                    efface,\
                    touche


#############################################################################
# CONSTANTES                                                                #
#############################################################################
NB_PIX_CASE = 100       # Nombre de pixel par case.
NB_COLONNES = 6         # Nombre de colonnes que contient la grille.
NB_LIGNES = 6           # Nombre de lignes que contient la grille.
MARGE = 120             # Nombre de pixels de marge graphique.


#############################################################################
# ELEMENTS VARIABLES                                                        #
#############################################################################
PION_ACTUEL = {'Couleur': 'Bleu', 'Joueur': 2}


#############################################################################
# FONCTIONS LITTERALES                                                      #
#############################################################################
def pixel_vers_case(position_pixel):
    '''
    Fonction permettant de connaître les coordonnées d'une case à partir
    des coordonnées fournies en pixels.

    :param position_pixel: tuple Coordonnées (X, Y) fournies en pixels.
    :return pos_case: list Position [X, Y] de la case pointée.

    >>> NB_PIX_CASE = 100
    >>> NB_COLONNES = 6
    >>> NB_LIGNES = 6
    >>> pixel_vers_case((159, 159))
    [1, 1]
    >>> pixel_vers_case((-2, 70))
    [1, 1]
    >>> pixel_vers_case((180, 450))
    [2, 4]
    '''
    pixel_x, pixel_y = position_pixel
    pos_case = [1, 1]

    # Vérification des sorties de zone du curseur de la souris
    if pixel_x < MARGE // 2:
        pixel_x = MARGE // 2
    elif pixel_x >= NB_PIX_CASE * NB_COLONNES + MARGE // 2:
        pixel_x = NB_PIX_CASE * NB_COLONNES - 1 + MARGE // 2

    if pixel_y < MARGE // 2:
        pixel_y = MARGE // 2
    elif pixel_y >= NB_PIX_CASE * NB_LIGNES + MARGE // 2:
        pixel_y = NB_PIX_CASE * NB_LIGNES - 1 + MARGE // 2

    # Position des coordonnées de grille (et non en pixels)
    pos_case[0] = ((pixel_x - MARGE // 2) // NB_PIX_CASE) + 1
    pos_case[1] = ((pixel_y - MARGE // 2) // NB_PIX_CASE) + 1

    return pos_case


# ---------------------------------------------------------------------------


def case_vers_pixel(case):
    '''
    Fonction recevant les coordonnées d'une case du plateau et renvoyant les
    coordonnées du pixel se trouvant au centre de cette case, en prenant en
    compte la taille de chaque case.

    :param case: int tuple Position (X, Y) de la case sur le plateau.
    :return coords: int list Coordonnées [X, Y] du milieu de la case pointée.

    >>> NB_PIX_CASE = 100
    >>> case_vers_pixel((1, 1))
    [110, 110]
    >>> case_vers_pixel((2, 3))
    [210, 310]
    >>> case_vers_pixel((6, 6))
    [610, 610]
    '''
    case_x, case_y = case
    coords = [0, 0]

    # Position des coordonnées des milieux de case en pixels
    coords[0] = case_x * NB_PIX_CASE - NB_PIX_CASE // 2 + MARGE // 2
    coords[1] = case_y * NB_PIX_CASE - NB_PIX_CASE // 2 + MARGE // 2

    return coords


# ---------------------------------------------------------------------------


def case_possible(num_joueur, terrain):
    '''
    Fonction prenant la case sur laquelle le pion se trouve et retournant les
    coordonnées des cases peuvant être utilisées pour se déplacer.

    :param num_joueur: int Numéro du joueur.
    :param terrain: list Eléments de terrain [[X, Y, Occupation, Joueur]]
    :return possible: list Liste des positions jouables.

    >>> plateau = [[1, 1, 'Prise', 1], [1, 2, 'Vide', 0], [1, 3, 'Vide', 0],\
    [1, 4, 'Vide', 0], [1, 5, 'Vide', 0], [1, 6, 'Vide', 0],\
    [2, 1, 'Noire', -1], [2, 2, 'Noire', -1], [2, 3, 'Vide', 0],\
    [2, 4, 'Vide', 0], [2, 5, 'Vide', 0], [2, 6, 'Vide', 0],\
    [3, 1, 'Prise', 2], [3, 2, 'Noire', -1], [3, 3, 'Noire', -1],\
    [3, 4, 'Vide', 0], [3, 5, 'Vide', 0], [3, 6, 'Vide', 0],\
    [4, 1, 'Vide', 0], [4, 2, 'Vide', 0], [4, 3, 'Vide', 0],\
    [4, 4, 'Vide', 0], [4, 5, 'Vide', 0], [4, 6, 'Vide', 0],\
    [5, 1, 'Vide', 0], [5, 2, 'Vide', 0], [5, 3, 'Vide', 0],\
    [5, 4, 'Vide', 0], [5, 5, 'Vide', 0], [5, 6, 'Vide', 0],\
    [6, 1, 'Vide', 0], [6, 2, 'Vide', 0], [6, 3, 'Vide', 0],\
    [6, 4, 'Vide', 0], [6, 5, 'Vide', 0], [6, 6, 'Vide', 0]]
    >>> joueur = 1
    >>> case_possible(joueur, plateau)
    [[1, 2]]
    >>> joueur = 2
    >>> case_possible(joueur, plateau)
    [[4, 1], [4, 2]]
    '''
    possible = []
    pos_joueur = []
    pos_libre = []

    # Enregistrements des positions des cases vides et du joueur
    for liste in terrain:
        if liste[2] == 'Vide':
            pos_libre.append([liste[0], liste[1]])
        if liste[3] == num_joueur:
            pos_joueur = [liste[0], liste[1]]

    # Détermination des cases libres autour du joueur
    for liste in pos_libre:
        if liste[0] <= pos_joueur[0]+1 and liste[0] >= pos_joueur[0]-1:
            if liste[1] <= pos_joueur[1]+1 and liste[1] >= pos_joueur[1]-1:
                possible.append(liste)

    return possible


# ---------------------------------------------------------------------------


def case_possible_hasard(num_joueur, terrain):
    '''
    Fonction permettant de fournir les coordonnées d'une case aléatoirement
    parmi les cases possibles autour du joueur en cours.

    :param num_joueur: int Numéro du joueur en cours.
    :param terrain: list Liste des cases du plateau.
    :return case: list Liste des deux coordonnées données au hasard.
    '''
    # Les coordonnées des cases possibles sont enregistrées
    case = case_possible(num_joueur, terrain)

    # Choix aléatoire parmi la liste de ces cases
    if case != []:
        case = case[randint(0, len(case) - 1)]

    return case


# ---------------------------------------------------------------------------


def position_joueur(num_joueur, terrain):
    '''
    Fonction permettant la détermination des coordonnées d'un joueur.

    :param num_joueur: int Numéro du joueur.
    :param terrain: list Liste des cases du plateau.
    :return case: list Coordonnées de la position du joueur.
    '''
    for liste in terrain:
        if liste[3] == num_joueur:
            case = [liste[0], liste[1]]

    return case


# ---------------------------------------------------------------------------


def multi_list(nombre, liste):
    '''
    Fonction permettant de multiplier tous les éléments d'une liste
    par un nombre.

    :param nombre: int Scalaire multiplicateur.
    :param liste: list Liste dont les termes sont à multiplier.
    :return liste: list Liste mise à jour.
    '''
    iteration = 0
    liste_sortie = []
    for _ in liste:
        liste_sortie.append(nombre * liste[iteration])
        iteration += 1
    return liste_sortie


# ---------------------------------------------------------------------------


def add_list(liste1, liste2):
    '''
    Fonction permettant le calcul de l'addition terme à terme de deux
    listes de même longueur.

    :param liste1: list Première liste d'entrée.
    :param liste2: list Deuxième liste d'entrée.
    :return somme: list Liste de la somme des deux listes,
    si possible.
    '''
    somme = []
    iteration = 0

    # Si la longueur de chaque liste est la même
    if len(liste1) == len(liste2):

        # Différence "terme à terme"
        for _ in liste1:
            somme.append(liste1[iteration] + liste2[iteration])
            iteration += 1

    return somme


# ---------------------------------------------------------------------------


def pos_max_list(liste):
    '''
    Fonction permettant la détection de la position du maximum d'une
    liste à une dimension.

    :param liste: list Liste d'entrée à traiter.
    :return curseur: int Position du maximum dans la liste.
    '''
    curseur = 0                 # Curseur du maximum détecté dans la liste
    maxi = 0                    # Maximum détecté
    compteur = 0                # Numéro du cas en cours de traitement
    for elem in liste:
        if elem > maxi:
            maxi = elem
            curseur = compteur
        compteur += 1
    return curseur


# ---------------------------------------------------------------------------


def choix_vide(num_joueur, terrain):
    '''
    Fonction permettant de connaître la case de déplacement la plus
    judicieuse pour l'ordinateur.
    Il s'agit de la case libre pour laquelle il y a le plus de cases
    libres consécutives dans la même direction.

    :param num_joueur: int Numéro du joueur.
    :param terrain: list Liste des cases du plateau.
    :return: list List des deux coordonnées de la case judicieuse.
    '''
    # Test des différentes cases encore possibles
    reste_cases = case_possible(num_joueur, terrain)

    # Détermination de la position actuelle du pion
    ma_pos = position_joueur(num_joueur, terrain)

    # Préparation vectorielle des huit positions possibles
    # vect[0]    vect[1]    vect[2]
    # vect[3]     pion      vect[4]
    # vect[5]    vect[6]    vect[7]
    vect = [[-1, -1],
            [0, -1],
            [1, -1],
            [-1, 0],
            [1, 0],
            [-1, 1],
            [0, 1],
            [1, 1]]

    # Répertoire des divers cas de figure (8 directions au maximum)
    num_cas = [1] * 8

    for i in range(8):

        # Les cas impossibles sont repertoriés dans num_cas[].
        if add_list(vect[i], ma_pos) not in reste_cases:
            num_cas[i] = 0

        # Parmi les cas restants, il reste à déterminer jusque quelle
        # profondeur vont les cases vides.
        compteur = True
        nbr = 2

        while compteur:
            liste_temp = []

            # Pas de traitement inutile
            if num_cas[i] == 0:
                compteur = False
            else:
                # Fabrication temporaire de l'élément suivant à comparer
                # avec le plateau s'il s'agit bien d'une case blanche.
                # L'élément est du style :
                # [Xmoi + nbr * Xdirection, Ymoi + nbr * Ydirection, 'Vide', 0]
                liste_temp = add_list(ma_pos, multi_list(nbr, vect[i]))
                liste_temp += ['Vide', 0]

                # Si cette case blanche existe et elle est répertoriée
                # dans num_cas[].
                if liste_temp in terrain:
                    num_cas[i] += 1
                else:
                    compteur = False
            nbr += 1

    # Détermination du cas le plus favorable (Maximum dans num_cas[]).
    index_max = pos_max_list(num_cas)

    # Direction à prendre et coordonnées finales à choisir
    return add_list(ma_pos, vect[index_max])


# ---------------------------------------------------------------------------


def init_plateau():
    '''
    Fonction permettant la création du plateau vide.

    :return grille: list Liste des cases vides du plateau.
    '''
    grille = []
    for col in range(NB_COLONNES):
        for lig in range(NB_LIGNES):
            grille.append([col+1, lig+1, 'Vide', 0])

    return grille


# ---------------------------------------------------------------------------


def change_joueur():
    '''
    Fonction permettant de changer joueur et de retenir temporairement
    la position du joueur après changement.
    '''
    if PION_ACTUEL['Couleur'] == 'Bleu' and PION_ACTUEL['Joueur'] == 1:
        PION_ACTUEL['Couleur'] = 'Rouge'
        PION_ACTUEL['Joueur'] = 2

    else:
        PION_ACTUEL['Couleur'] = 'Bleu'
        PION_ACTUEL['Joueur'] = 1


#############################################################################
# FONCTIONS GRAPHIQUES ET EVENEMENTIELLES                                   #
#############################################################################
def affiche_plateau(terrain):
    '''
    Fonction affichant le plateau ainsi que l'état de chaque case.

    :param terrain: list Liste des cases du plateau.
    '''
    lettres = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
               'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'W',
               'X', 'Y', 'Z']

    # Gestion d'affichage des cases
    for coords in terrain:

        # case_vers_pixel() tient déjà compte des marges
        centre = case_vers_pixel((coords[0], coords[1]))
        p1_x = centre[0] - NB_PIX_CASE / 2
        p1_y = centre[1] - NB_PIX_CASE / 2
        p2_x = centre[0] + NB_PIX_CASE / 2
        p2_y = centre[1] + NB_PIX_CASE / 2
        if coords[2] != 'Noire':
            remplissage = 'white'
        else:
            remplissage = 'black'
        rectangle(p1_x, p1_y, p2_x, p2_y, 'black', remplissage, 2)

        # Gestion d'affichage des coordonnées verticales
        texte(MARGE // 3,
              centre[1],
              lettres[coords[1]-1],
              'black',
              'e',
              'Arial',
              20,
              'lettres')

        # Gestion d'affichage des coordonnées horizontales
        texte(centre[0],
              MARGE // 3,
              coords[0],
              'black',
              'center',
              'Arial',
              20,
              'nombres')

        # Gestion d'affichage des pions
        if coords[3] == 1:
            trait = 'black'
            coul_pion = 'red'
            etiquette = 'Rouge'
        elif coords[3] == 2:
            trait = 'black'
            coul_pion = 'blue'
            etiquette = 'Bleu'
        else:
            trait = ''
            coul_pion = ''
            etiquette = ''
        cercle(centre[0], centre[1], 30, trait, coul_pion, 2, etiquette)

    mise_a_jour()


# ---------------------------------------------------------------------------


def affiche_texte(message):
    '''
    Fonction permettant d'afficher un message dans le canvas de l'interface
    graphique, par-dessus le cadrillage.

    :param message: str Message à afficher.
    '''
    efface('texte')
    texte(NB_PIX_CASE * NB_COLONNES // 2,
          NB_PIX_CASE * NB_LIGNES + MARGE - 2,
          message,
          'orange',
          's',
          'Arial',
          14,
          'texte')
    mise_a_jour()


# ---------------------------------------------------------------------------


def cree_pion(terrain):
    '''
    Fonction recevant les coordonnées du pion par la position du curseur de la
    souris et un clic gauche pour confirmer cette position sur le plateau.

    :param terrain: list Liste des cases du plateau.
    :return terrain: list Liste modifiée des cases du plateau (joueur placé).
    '''
    coordonnees = (0, 0)
    attente = True

    # Au clic gauche, blocage des coordonnées retenues
    while attente:
        coordonnees = (abscisse_souris(), ordonnee_souris())
        evenement = donne_ev()
        if type_ev(evenement) == 'ClicGauche':

            # Conversion des pixels en position de case
            pos = pixel_vers_case(coordonnees)

            # pos[0] contient le numéro de colonne et
            # pos[1] contient le numéro de ligne.
            for liste in terrain:   # Recherche de la case à modifier
                if liste[0] == pos[0] and liste[1] == pos[1]:

                    # Recherche d'index de la case à modifier
                    num_index = terrain.index(liste)

                    # Test de non superposition avec le pion précédent
                    if terrain[num_index][2] != 'Prise':
                        terrain[num_index][2] = 'Prise'
                        terrain[num_index][3] = PION_ACTUEL['Joueur']

                        # Si tout s'est bien passé, il y a changement de joueur
                        change_joueur()
                        attente = False

        mise_a_jour()

    return terrain


# ---------------------------------------------------------------------------


def case_en_moins(terrain):
    '''
    Fonction rendant une certaine case inutilisable (par un clic souris).

    :param terrain: list Liste des cases du plateau ainsi que leur état.
    :return terrain: list Liste des nouveaux états des cases du plateau.
    '''
    coordonnees = (0, 0)
    attente = True

    # Au clic gauche, blocage des coordonnées retenues
    while attente:
        coordonnees = (abscisse_souris(), ordonnee_souris())
        evenement = donne_ev()
        if type_ev(evenement) == 'ClicGauche':

            # Conversion des pixels en position de case
            pos = pixel_vers_case(coordonnees)

            # pos[0] contient le numéro de colonne et
            # pos[1] contient le numéro de ligne de la case cliquée.
            for liste in terrain:   # Recherche de la case à modifier
                if liste[0] == pos[0] and liste[1] == pos[1]:

                    # Recherche d'index de la case à modifier
                    num_index = terrain.index(liste)

                    # Test de liberté de la case pointée
                    if terrain[num_index][2] == 'Vide':
                        terrain[num_index][2] = 'Noire'
                        # terrain[num_index][3] = pion_actuel['Joueur']

                        attente = False

        mise_a_jour()

    return terrain


# ---------------------------------------------------------------------------


def case_en_moins_ordi(terrain):
    '''
    Fonction rendant une certaine case inutilisable (Automatiquement).

    :param terrain: list Liste des cases du plateau ainsi que leur état.
    :return terrain: list Liste des nouveaux états des cases du plateau.
    '''
    # Détermination d'une case à noircir autour du joueur
    pos = case_possible_hasard(1, terrain)

    # Recherche de l'index pour les coordonnées "pos"
    pos.append('Vide')
    pos.append(0)
    num_index = terrain.index(pos)

    # Incorporation du pion de l'ordinateur
    terrain[num_index][2] = 'Noire'
    terrain[num_index][3] = -1

    mise_a_jour()

    return terrain


# ---------------------------------------------------------------------------


def deplacement(terrain):
    '''
    Fonction permettant le déplacement d'un pion losque c'est possible.

    :param terrain: list Liste des cases du plateau ainsi que leur état.
    :return terrain: list Liste des cases du plateau mises à jour.
    '''
    attente = True

    # Au clic gauche, blocage des coordonnées retenues
    while attente:
        pos = pixel_vers_case((abscisse_souris(), ordonnee_souris()))
        evenement = donne_ev()

        # Vérification des cases restantes autour du joueur
        restant = case_possible(PION_ACTUEL['Joueur'], terrain)

        # La vérification du clic du joueur dans la bonne zone est
        # effectuée en même temps.
        if type_ev(evenement) == 'ClicGauche' and\
                pos in restant and restant != []:

            # Ajout des états par défaut dans la liste "restant"
            for prepa in restant:
                prepa += ['Vide', 0]

            # Effacement de la position initiale du joueur en cours.
            efface_position(PION_ACTUEL['Joueur'], terrain)

            for liste in restant:

                # Gestion de la prochaine position
                if liste[0] == pos[0] and liste[1] == pos[1]:

                    # Recherche d'index de la case à modifier
                    num_index = terrain.index(liste)

                    # Test de liberté de la case pointée
                    if terrain[num_index][2] == 'Vide':
                        terrain[num_index][2] = 'Prise'
                        terrain[num_index][3] = PION_ACTUEL['Joueur']

                        attente = False
        mise_a_jour()
    return terrain


# ---------------------------------------------------------------------------


def deplacement_ordi(terrain):
    '''
    Fonction permettant le déplacement de l'ordinateur,
    nécessairement "Joueur 2".

    :param terrain: list Liste des cases du plateau ainsi que leur état.
    :return terrain: list Liste des cases du plateau mises à jour.
    '''
    # Choix automatique du déplacement du pion ordinateur
    pos = choix_vide(2, terrain)

    # Effacement de la position initiale du joueur en cours.
    efface_position(2, terrain)

    # Recherche de l'index pour les coordonnées "pos"
    pos.append('Vide')
    pos.append(0)
    num_index = terrain.index(pos)

    # Incorporation du pion de l'ordinateur
    terrain[num_index][2] = 'Prise'
    terrain[num_index][3] = 2

    mise_a_jour()
    return terrain


# ---------------------------------------------------------------------------


def efface_position(num_joueur, terrain):
    '''
    Fonction permettant de réinitialiser la position d'un joueur.

    :param num_joueur: int Numéro de joueur en cours.
    :param terrain: list Liste des cases du plateau.
    :return terrain: list Plateau dont l'état des cases a été mis à jour.
    '''
    # Recherche de la case contenant le joueur en cours.
    for pos in terrain:
        if pos[2] == 'Prise' and pos[3] == num_joueur:

            # Réinitialisation de la case
            pos[2] = 'Vide'
            pos[3] = 0

    return terrain


# ---------------------------------------------------------------------------


def mort():
    '''
    Fonction recevant les coordonnées du pion et celles des cases utilisables,
    et retournant 0 si il n'y en a aucune autour de celui-ci.
    '''
    efface('messagefin')
    efface('messagefin2')
    efface('texte')

    # Rectangle principal de message de fin
    rectangle((NB_COLONNES * NB_PIX_CASE + MARGE) // 8 - 4,
              (NB_LIGNES * NB_PIX_CASE + MARGE) // 3 - 4,
              (NB_COLONNES * NB_PIX_CASE + MARGE) * 7 // 8 + 4,
              (NB_LIGNES * NB_PIX_CASE + MARGE) * 2 // 3 + 4,
              'black',
              'white',
              2,
              'messagefin2')

    rectangle((NB_COLONNES * NB_PIX_CASE + MARGE) // 8,
              (NB_LIGNES * NB_PIX_CASE + MARGE) // 3,
              (NB_COLONNES * NB_PIX_CASE + MARGE) * 7 // 8,
              (NB_LIGNES * NB_PIX_CASE + MARGE) * 2 // 3,
              'black',
              'white',
              2,
              'messagefin')

    # Message de fin de partie
    message = "Joueur " + str(PION_ACTUEL['Joueur'])\
        + " : Vous avez perdu !\n"\
        + "Voulez-vous rejouer ?\n"\
        + "[ESC] : Quitter\n"\
        + "[ESPACE] : Rejouer"

    texte((NB_PIX_CASE * NB_COLONNES + MARGE) // 2,
          (NB_PIX_CASE * NB_LIGNES + MARGE) // 2,
          message,
          'red',
          'center',
          'Arial',
          20,
          'texte')

    return False


# ---------------------------------------------------------------------------


def menu_depart():
    '''
    Fonction permettant l'affichage des choix des modes de jeu désiré.
    '''
    efface('messagedebut')
    efface('messagedebut2')
    efface('texte')

    # Rectangle principal de message de fin
    rectangle((NB_COLONNES * NB_PIX_CASE + MARGE) // 8 - 4,
              (NB_LIGNES * NB_PIX_CASE + MARGE) // 3 - 4,
              (NB_COLONNES * NB_PIX_CASE + MARGE) * 7 // 8 + 4,
              (NB_LIGNES * NB_PIX_CASE + MARGE) * 2 // 3 + 4,
              'black',
              'white',
              2,
              'messagedebut2')

    rectangle((NB_COLONNES * NB_PIX_CASE + MARGE) // 8,
              (NB_LIGNES * NB_PIX_CASE + MARGE) // 3,
              (NB_COLONNES * NB_PIX_CASE + MARGE) * 7 // 8,
              (NB_LIGNES * NB_PIX_CASE + MARGE) * 2 // 3,
              'black',
              'white',
              2,
              'messagedebut')

    # Message de fin de partie
    message = "~ ~ ~ ~ ~ ISOLA ~ ~ ~ ~ ~"\
        + "\n \n"\
        + "Combien de joueur(s) ?\n"\
        + "[1] : Un joueur\n"\
        + "[2] : Deux joueurs"

    texte((NB_PIX_CASE * NB_COLONNES + MARGE) // 2,
          (NB_PIX_CASE * NB_LIGNES + MARGE) // 2,
          message,
          'springgreen3',
          'center',
          'Arial',
          22,
          'texte')


# ---------------------------------------------------------------------------


def nb_joueurs():
    '''
    Fonction qui attend la réponse du nombre de joueur(s) à participer.

    :return nombre: int Nombre de joueur(s).
    '''
    choix_effectue = False
    while not choix_effectue:
        choix = donne_ev()
        type_eve = type_ev(choix)

        # Détection de la touche de sélection du nombre de joueur(s)
        if type_eve is not None:
            if touche(choix) == 'KP_1' or touche(choix) == '1':
                nombre = 1
                choix_effectue = True
            if touche(choix) == 'KP_2' or touche(choix) == '2':
                nombre = 2
                choix_effectue = True
        mise_a_jour()

    return nombre


# ---------------------------------------------------------------------------


def jeu(fonctionnement):
    '''
    Fonction isolant la partie en cours.
    '''
    plateau = init_plateau()
    menu_depart()
    rep = nb_joueurs()

    # Création des joueurs
    for _ in range(2):
        affiche_plateau(plateau)
        affiche_texte("Joueur "
                      + str(PION_ACTUEL['Joueur'])
                      + " : Placez votre pion.")
        plateau = cree_pion(plateau)
        affiche_plateau(plateau)

    # Cas du jeu à deux joueurs
    if rep == 2:
        fonctionnement = jeu2(fonctionnement, plateau)

    # Cas du jeu à un joueur
    if rep == 1:
        fonctionnement = jeu1(fonctionnement, plateau)

    return fonctionnement


# ---------------------------------------------------------------------------


def jeu2(fonctionnement, terrain):
    '''
    Coeur du jeu à deux joueurs.

    :param fonctionnement: bool Etat de la partie en cours.
    :param terrain: list Liste des cases du plateau.
    :return fonctionnement: bool Etat de la partie.
    '''
    # C'est parti pour le jeu à deux !
    while fonctionnement:
        change_joueur()
        if case_possible(PION_ACTUEL['Joueur'], terrain) == []:
            fonctionnement = mort()
        else:
            affiche_texte("Joueur "
                          + str(PION_ACTUEL['Joueur'])
                          + " : Déplacez votre pion.")
            terrain = deplacement(terrain)
            affiche_plateau(terrain)
            if case_possible(PION_ACTUEL['Joueur'], terrain) != []:
                affiche_texte("Joueur "
                              + str(PION_ACTUEL['Joueur'])
                              + " : Interdisez une case.")
                terrain = case_en_moins(terrain)
                affiche_plateau(terrain)
            else:
                fonctionnement = mort()

    return fonctionnement


# ---------------------------------------------------------------------------


def jeu1(fonctionnement, terrain):
    '''
    Coeur du jeu à un joueur contre l'ordinateur.

    :param fonctionnement: bool Etat de la partie en cours.
    :param terrain: list Liste des cases du plateau.
    :return fonctionnement: bool Etat de la partie.
    '''
    # C'est parti pour le jeu en mode Ordinateur !
    while fonctionnement:
        change_joueur()

        if case_possible(PION_ACTUEL['Joueur'], terrain) == []:
            fonctionnement = mort()
        else:

            # L'ordinateur sera toujours le joueur 2
            if PION_ACTUEL['Joueur'] == 1:
                affiche_texte("Joueur 1 : Déplacez votre pion.")
                terrain = deplacement(terrain)
            else:
                affiche_texte("Ordinateur : Déplacement du pion.")
                terrain = deplacement_ordi(terrain)
            affiche_plateau(terrain)

            if case_possible(PION_ACTUEL['Joueur'], terrain) != []:

                # L'ordinateur est toujours le joueur 2
                if PION_ACTUEL['Joueur'] == 1:
                    affiche_texte("Joueur "
                                  + str(PION_ACTUEL['Joueur'])
                                  + " : Interdisez une case.")
                    terrain = case_en_moins(terrain)
                else:
                    affiche_texte("Ordinateur : Interdiction d'une case.")
                    terrain = case_en_moins_ordi(terrain)

                affiche_plateau(terrain)

            else:
                fonctionnement = mort()

    return fonctionnement


#############################################################################
# PROGRAMME PRINCIPAL                                                       #
#############################################################################
testmod()

# Amélioration de jeu : entrée du nombre de lignes et colonnes
# dans un terminal à cause de l'ouverture de fenêtre.
TEST = False
while not TEST:
    print("~~~~ ISOLA ~~~~")
    nbre_lignes = int(input("Nombre de lignes souhaitées (5 à 9) ? "))
    if 5 <= nbre_lignes <= 9:
        nbre_colonnes = int(input("Nombre de colonnes souhaitées (5 à 12) ? "))
        if 5 <= nbre_colonnes <= 12:
            TEST = True
            NB_LIGNES = nbre_lignes
            NB_COLONNES = nbre_colonnes
# Fin d'amélioration de jeu

cree_fenetre(NB_COLONNES * NB_PIX_CASE + MARGE,
             NB_LIGNES * NB_PIX_CASE + MARGE)

BOUCLE = True
REPONSE = False
while BOUCLE:
    EVE = donne_ev()
    TYPE_EVE = type_ev(EVE)

    # Détection des touches appuyées en fin de partie
    if TYPE_EVE == 'Touche':
        if touche(EVE) == 'Escape':
            BOUCLE = False
        if touche(EVE) == 'space':
            REPONSE = False
            BOUCLE = True
    elif not REPONSE:
        REPONSE = True
        jeu(REPONSE)

    mise_a_jour()

ferme_fenetre()

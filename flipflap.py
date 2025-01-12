from tkiteasy import *
from random import *
'''
add_tuple(tuple, tuple) -> tuple
entrée: position de la bille et le vecteur a lui appliquer
sortie: nouvelle position de la bille '''
def add_tuple(tuple1,tuple2):
    return tuple(a + b for a, b in zip(tuple1, tuple2))

class FlipFlap:
    '''creation de la classe
    __init__(int, int, int, int)
    entrée: le nombre de pixels du jeu , le nombre de lignes(et donc de colonnes), le nombre d'obstacles crées, le nombre de billes mises en jeu sur le plateau 
    sortie: pas de sortie mais creation de variables utiles plus tard'''
    def __init__(self,taille_ecran, nombre_lignes, nombre_obstacles,nombrebilles):
        self.nbrebilles=nombrebilles
        self.nombre_lignes = nombre_lignes
        self.taille_ecran = taille_ecran
        self.taillecase = taille_ecran//nombre_lignes
        self.nombre_obstacles = nombre_obstacles
        self.plateau = {(ligne, colonne): "0" for ligne in range(self.nombre_lignes) for colonne in range(self.nombre_lignes)}
        self.list_bille= []
        self.list_objbille=[]
        self.list_vect_bille=[]
        self.list_obstacles = []
    '''positions initiales des billes  
    random_billes(self) -> list
    entrée: objet de classe
    sortie: liste des positions des billes (tuples(x, y))'''
    def random_billes(self):
        for _ in range(self.nbrebilles):
    
            pos_bille  = (choice([(randint(0, self.nombre_lignes-1), 0),
                            (randint(0, self.nombre_lignes-1), self.nombre_lignes-1),
                            (0, randint(0, self.nombre_lignes-1)),
                            (self.nombre_lignes-1, randint(0, self.nombre_lignes-1))]))
            if pos_bille[0] == 0:
                vect_bille = (1, 0)
            if pos_bille[0] == 49:
                vect_bille = (-1, 0)
            if pos_bille[1] == 49:
                vect_bille = (0, -1)
            if pos_bille[1] == 0:
                vect_bille = (0, 1)
            self.list_vect_bille.append(vect_bille)
            
            self.list_bille.append(pos_bille)
        return self.list_bille
    '''positions des obstacles
    random_obstacle(self) -> dict    
    entrée: objet de classe
    sortie: dictionnaire ayant comme clés les positions des obstacles (tuples(x, y)) et comme valeur la couleur de l'obstacle (string)'''
    def random_obstacle(self):
        pos_obstacle = sample(list(self.plateau), self.nombre_obstacles)
        self.position_obstacles = {(position): choice(["red", "green", "blue"]) for position in pos_obstacle}
        return self.position_obstacles
    '''creation de l'ecran du jeu 
    init_gfx(self) -> list
    entrée: objet de classe
    sortie: liste des objets obstacles'''
    def init_gfx(self): 
        self.gfx = ouvrirFenetre(self.taille_ecran, self.taille_ecran)
        for i in range(0, self.taille_ecran, self.taillecase):
            self.gfx.dessinerLigne(i, 0, i, self.taille_ecran, "grey")
            self.gfx.dessinerLigne(0, i, self.taille_ecran, i, "grey")
        for bille in self.list_bille:
            self.list_objbille.append(self.gfx.dessinerDisque(bille[0]*self.taillecase+self.taillecase//2,
                                                                 bille[1]*self.taillecase+self.taillecase//2,
                                                                 self.taillecase//2-1.5,
                                                                 'white'))
        for pos, color in self.position_obstacles.items():
            obstacle_obj = self.gfx.dessinerRectangle(pos[1]*self.taillecase+1,
                                       pos[0]*self.taillecase+1,
                                       self.taillecase-1,
                                       self.taillecase-1,
                                       color)
            self.list_obstacles.append((pos, obstacle_obj))
        for objBille in self.list_objbille:
            self.gfx.placerAuDessus(objBille)
            
    '''fonction qui modifie le vecteur a appliquer a la  bille en fonction de l'obstacle qu'elle rencontre
    vect_obstacle(self, tuple, int) -> list
    entrée: objet de classe, position de la bille dont on veut changer le vecteur, position de la bille dans la liste des billes (voir verif_case)
    sortie: liste des vecteurs a appliquer aux billes modifiée'''
    def vect_obstacle(self,bille,i):
            if self.position_obstacles[bille[1],bille[0]] == 'green':
                self.list_vect_bille[i] = (-self.list_vect_bille[i][0],-self.list_vect_bille[i][1])
            if self.position_obstacles[bille[1],bille[0]] == 'blue':
                self.list_vect_bille[i] = (self.list_vect_bille[i][1],-self.list_vect_bille[i][0])
            if self.position_obstacles[bille[1],bille[0]] == 'red':
                self.list_vect_bille[i] = (-self.list_vect_bille[i][1],self.list_vect_bille[i][0])
            return self.list_vect_bille
    '''fonction qui verifie si la bille croise un obstacle
    verif_case(self) -> None
    entrée: objet de classe
    sortie: (voir vect_obstacle)'''
    def verif_case(self):
        for i in range(len(self.list_bille)):
            if (self.list_bille[i][1],self.list_bille[i][0]) in self.position_obstacles:
                    self.vect_obstacle(self.list_bille[i],i)
    '''fonction qui deplace sur le plateau les billes 
    move(self) -> list
    entrée: objet de classe
    sortie: liste des position des billes mise a jour'''
    def move(self):
        for i in range(len(self.list_bille)):
                self.list_bille[i]= add_tuple(self.list_bille[i], self.list_vect_bille[i])
        return self.list_bille
    '''fonction qui determine quand le jeu est terminé
    is_ended(self) -> bool
    entrée: objet de classe
    sortie: booleen qui determine si le jeu est terminé'''
    def is_ended(self):
        compteur = 0 
        for bille in self.list_bille:
            if (bille not in self.plateau):
                compteur +=1
            if compteur == self.nbrebilles:
                return True
        return False
    '''fonction qui deplace les billes graphiquement cette fois ci
    move_gfx(self) -> None
    entrée: objet de classe
    sortie: rien mais l'ecran actualisé'''
    def move_gfx(self):
        for i in range (len(self.list_bille)):
            self.gfx.deplacer(self.list_objbille[i],self.list_vect_bille[i][0]*self.taille_ecran//self.nombre_lignes, self.list_vect_bille[i][1]*self.taille_ecran//self.nombre_lignes)
            self.gfx.actualiser()
    '''fonction qui permet au clic de changer la couleur de l'obstacle
    changement_couleur(self) -> None
    entrée: objet de classe
    sortie: rien mais la liste des obstacles actualisée et l'obstacle changé'''
    def changement_couleur(self):
        couleurs = ['red', 'green', 'blue']
        clic = self.gfx.recupererClic()
        if clic:
            for position, obstacle_obj in self.list_obstacles:
                if position[1] == clic.x // self.taillecase and position[0] == clic.y // self.taillecase:
                    couleur_actuelle = self.position_obstacles[position]
                    prochaine_couleur = (couleurs.index(couleur_actuelle) + 1) % len(couleurs)
                    nouvelle_couleur = couleurs[prochaine_couleur]
                    self.position_obstacles[position] = nouvelle_couleur
                    self.gfx.changerCouleur(obstacle_obj, nouvelle_couleur)
                    self.gfx.actualiser()
                    break
        

    
    

    '''boucle du jeu qui lance les fonctions utiles au deroulement du jeu
    game(self) -> None
    entrée: objet de classe
    sortie: rien '''
    def game(self):
        self.random_obstacle()
        self.random_billes()
        self.init_gfx()
        while not self.is_ended():
            self.changement_couleur()
            self.verif_case()
            self.move()
            self.move_gfx()
            self.gfx.pause(0.2)
        self.gfx.fermerFenetre()

    
    

'''menu qui permet de modifier les parametres du jeu et de le lancer
menu() -> None
entrée None
sortie None'''
def menu():
    parametres = {
        'taille_ecran': 500,
        'nombre_obstacles': 100,
        'nombrebilles': 20,
        'nombre_cases': 50
    }
    while True:
        menu = ouvrirFenetre(500, 555)
        menu.dessinerRectangle(0, 0, 555, 555, "white")
        menu.afficherTexte("FLIP FLAP GAME", 250, 100, "black", 24)
        menu.dessinerRectangle(50, 200, 400, 50, "grey")
        menu.afficherTexte("PLAY", 250, 225, "black", 18)
        menu.dessinerRectangle(50, 300, 400, 50, "grey")
        menu.afficherTexte("PARAMETRES", 250, 325, "black", 18)
        menu.dessinerRectangle(50, 400, 400, 50, "grey")
        menu.afficherTexte("QUITTER", 250, 425, "black", 18)
        clic = menu.attendreClic()
        if 50 < clic.x < 450 and 200 < clic.y < 250:
            menu.fermerFenetre()
            a = FlipFlap(parametres['taille_ecran'], 
                         parametres['nombre_cases'], 
                         parametres['nombre_obstacles'], 
                         parametres['nombrebilles'])
            a.game()
        elif 50 < clic.x < 450 and 300 < clic.y < 350:
            menu.fermerFenetre()
            ouvert = True
            while ouvert:
                parametre = ouvrirFenetre(500, 555)
                parametre.dessinerRectangle(0, 0, 555, 555, "white")
                parametre.afficherTexte("PARAMETRES", 250, 100, "black", 24)
                parametre.dessinerRectangle(50, 200, 400, 50, "grey")
                parametre.afficherTexte(f"Taille de l'ecran: {parametres['taille_ecran']}", 250, 225, "black", 18)
                parametre.dessinerRectangle(50, 300, 400, 50, "grey")
                parametre.afficherTexte(f"Obstacles: {parametres['nombre_obstacles']}", 250, 325, "black", 18)
                parametre.dessinerRectangle(50, 400, 400, 50, "grey")
                parametre.afficherTexte(f"Billes: {parametres['nombrebilles']}", 250, 425, "black", 18)
                parametre.dessinerRectangle(50, 500, 400, 50, "grey")
                parametre.afficherTexte("retour au menu ", 250, 525, "black", 18)
                clic = parametre.attendreClic()
                if 50 < clic.x < 450 and 200 < clic.y < 250:
                    parametres['taille_ecran'] = 1000 if parametres['taille_ecran'] == 500 else 500 if parametres['taille_ecran'] == 1000 else None
                    parametre.fermerFenetre()
                elif 50 < clic.x < 450 and 300 < clic.y < 350:
                    parametres['nombre_obstacles'] = 100 if parametres['nombre_obstacles'] == 200 else 200 if parametres['nombre_obstacles'] == 100 else None
                    parametre.fermerFenetre()
                elif 50 < clic.x < 450 and 400 < clic.y < 450:
                    parametres['nombrebilles'] = 20 if parametres['nombrebilles'] == 50 else 50 if parametres['nombrebilles'] == 20 else None
                    parametre.fermerFenetre()
                elif 50 < clic.x < 450 and 500 < clic.y < 550:
                    parametre.fermerFenetre()
                    ouvert = False
        elif 50 < clic.x < 450 and 400 < clic.y < 450:
            menu.fermerFenetre()
            break
'''seule fonction a lancer pour le fonctionnement du jeu'''
menu()
import os,random,time
import multiprocessing as mp
import threading

#Couleurs
couleurs = [
    "\033[22;31m",
    "\033[22;32m",
    "\033[22;33m",
    "\033[22;34m",
    "\033[22;35m",
    "\033[22;36m",
    "\033[22;37m",
]

def start_travailleurs(nb_travailleur:int,nb_prise:int,cond,billes_disponnible)->None:
    """
    fonction qui lance les différents process travailleur.
    """
    listTravailleur = list()
    for i in range(nb_travailleur):
        listTravailleur.append(mp.Process(target=travailleur, args= (i,nb_prise,cond,billes_disponnible)))
    for fils in listTravailleur:
        fils.start()

def travailleur(id_travailleur:int,nb_de_prise_de_bille:int,cond,billes_disponnible)->None:
    """
    process travailleur.
        Génère un nombre entre 1 et 9,
        Dit au controlleur qu'il souhaite x bille(s), attends un retour du controlleur.
        Lorsque il peut il commence a travailler avec le(s) bille(s) ensuite repose les billes dans le pot commun.
    """

    while working.value:
        billes_a_prendre = random.randint(1,billes)# if billes_disponnible.value else 1
        demander(billes_a_prendre,cond,billes_disponnible)
        print(f"{couleurs[id_travailleur]}id : {id_travailleur} je prends {billes_a_prendre}")
        time.sleep(random.random()*5)#temps d'attente (Temps de simulation de travail)
        rendre(billes_a_prendre,billes_disponnible)
        print(f"{couleurs[id_travailleur]}id : {id_travailleur} je vais rendre {billes_a_prendre}")

def demander(nombre_de_bille_demande,cond,billes_disponnible):

    cond.acquire()
    while nombre_de_bille_demande > billes_disponnible.value:
        cond.wait()
    billes_disponnible.value -= nombre_de_bille_demande
    cond.notify_all()
    cond.release()


def rendre(billes_a_rendre,billes_disponnible):
    billes_disponnible.value += billes_a_rendre
    

def controlleur(verrou,billes_disponnible)->None:
    """
    Controlleur:
        regarde si les billes peuvent être distribué.
            Si oui elle les distribue au travailleur, et les informe qu'ils peuvent travailler.
            sinon elle les met en attente.
    """


    while working.value:
        if billes_disponnible.value >= 0 and billes_disponnible.value <= billes:

            #print("ok")
            time.sleep(1)
            
        else:
            print("KO")
            exit("erreur")

    """
    assert(billes_disponnible.value >= 0 and billes_disponnible.value <= billes)
    print("ok")
    """

if __name__ == '__main__':
    #valeurs
    billes = 9
    nb_travailleurs = 4
    nb_prise = 4
    #nombre de bille actuel.
    billes_disponnible = mp.Value('i', billes)
    #nombre de travailleur qui fonctionne pr le moment.
    working = mp.Value('b', True)
    #condition :
    condition = mp.Condition()
    #queue des demandes de bille.
    queue_billes = mp.Queue()

    #process controlleur.
    controlleur = mp.Process(target=controlleur, args= (condition,billes_disponnible))
    controlleur.start()
    #starts process
    start_travailleurs(nb_travailleurs,nb_prise,condition,billes_disponnible)
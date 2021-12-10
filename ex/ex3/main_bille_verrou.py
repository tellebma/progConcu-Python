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

def start_travailleurs(nb_travailleur:int,nb_prise:int,verrou,billes_disponnible)->None:
    """
    fonction qui lance les différents process travailleur.
    """
    listTravailleur = list()
    for i in range(nb_travailleur):
        listTravailleur.append(mp.Process(target=travailleur, args= (i,nb_prise,verrou,billes_disponnible)))
    for fils in listTravailleur:
        fils.start()

def travailleur(id_travailleur:int,nb_de_prise_de_bille:int,verrou,billes_disponnible)->None:
    """
    process travailleur.
        Génère un nombre entre 1 et 9,
        Dit au controlleur qu'il souhaite x bille(s), attends un retour du controlleur.
        Lorsque il peut il commence a travailler avec le(s) bille(s) ensuite repose les billes dans le pot commun.
    """
    while working.value:
        billes_a_prendre = random.randint(1,billes)# if billes_disponnible.value else 1
        
        demander(billes_a_prendre,verrou,billes_disponnible)
        print(f"{couleurs[id_travailleur]}id : {id_travailleur} je prends {billes_a_prendre}")
        time.sleep(random.random()*10)#temps d'attente (Temps de simulation de travail)
        rendre(billes_a_prendre,verrou,billes_disponnible)
        print(f"{couleurs[id_travailleur]}id : {id_travailleur} je vais rendre {billes_a_prendre}")

def demander(nombre_de_bille_demande,verrou,billes_disponnible):
    verrou.acquire()
    while nombre_de_bille_demande > billes_disponnible.value:
        verrou.release()
        time.sleep(0.5)
        verrou.acquire()
    billes_disponnible.value -= nombre_de_bille_demande
    verrou.release()

def rendre(billes_a_rendre,verrou,billes_disponnible):
    with verrou:
        billes_disponnible.value += billes_a_rendre
 
def controlleur(verrou,billes_disponnible)->None:
    """
    Controlleur:
        regarde si les billes peuvent être distribué.
            Si oui elle les distribue au travailleur, et les informe qu'ils peuvent travailler.
            sinon elle les met en attente.
    """
    while working.value:
        verrou.acquire()
        if billes_disponnible.value >= 0 and billes_disponnible.value <= billes:
            verrou.release()
            #print("ok")
            time.sleep(1)
        else:
            print("KO")
            exit("erruer")
    """
    assert(billes_disponnible.value >= 0 and billes_disponnible.value <= billes)
    print("ok")
    """

if __name__ == '__main__':
    #mutex du sémaphore
    mutex = mp.Semaphore() 
    #valeurs 
    billes = 9
    nb_travailleurs = 4
    nb_prise = 4
    #nombre de bille actuel.
    billes_disponnible = mp.Value('i', billes)
    #nombre de travailleur qui fonctionne pr le moment.
    working = mp.Value('b', True)
    #verrou :
    verrou = mp.Lock()
    #queue des demandes de bille.
    queue_billes = mp.Queue()
    #process controlleur.
    controlleur = mp.Process(target=controlleur, args= (verrou,billes_disponnible))
    controlleur.start()
    #starts process
    start_travailleurs(nb_travailleurs,nb_prise,verrou,billes_disponnible)
    

import os,random,time
import multiprocessing as mp


#Couleurs
CL_GREEN="\033[22;32m" 
CL_RED="\033[22;31m"
NORMAL = "\x1B[0m"  
CL_YELLOW="\033[01;33m" 

def start_travailleurs(nb_travailleur:int,nb_prise:int)->None:
    """
    fonction qui lance les différents process travailleur.
    """
    listTravailleur = list()
    for i in range(nb_travailleur):
        listTravailleur.append(mp.Process(target=travailleur, args= (i,nb_prise)))
    for fils in listTravailleur:
        fils.start()



def attente_retour(id_travailleur:int)->None:
    """
    Attends jusqu'a ce que le controlleur l'autorise a travailler.
    """
    while not retour[id_travailleur]:pass
    

def travailleur(id_travailleur:int,nb_de_prise_de_bille:int)->None:
    """
    process travailleur.
        Génère un nombre entre 1 et 9,
        Dit au controlleur qu'il souhaite x bille(s), attends un retour du controlleur.
        Lorsque il peut il commence a travailler avec le(s) bille(s) ensuite repose les billes dans le pot commun.
    
    """
    billes_a_prendre = int(random.random()*8)+1
    while nb_de_prise_de_bille>0:
        
        if billes_total[0]-billes_a_prendre >= 0:
            retour[id_travailleur]=False
            queue_billes.put([id_travailleur,-billes_a_prendre])
            #ATTENTE
            attente_retour(id_travailleur)

            print(f"{NORMAL}Je viens ({os.getpid()}) de prendre {CL_RED}{billes_a_prendre} bille(s){NORMAL}, il reste mnt {CL_YELLOW}{billes_total[0]} bille(s){NORMAL} dans le pot.")
            time.sleep(random.random()*2)#temps d'attente (Temps de simulation de travail)
            nb_de_prise_de_bille-=1#nb de tours a faire.
            
            with mutex:
                billes_total[0] += billes_a_prendre
            
            print(f"{NORMAL}Je viens ({os.getpid()}) de reposer les {CL_GREEN}{billes_a_prendre} bille(s){NORMAL} que j'ai emprunté, il me reste {nb_de_prise_de_bille} tour(s) a faire. Il reste mnt {CL_YELLOW}{billes_total[0]} bille(s){NORMAL} dans le pot.")
            billes_a_prendre = int(random.random()*8)+1
    
    with mutex:
        working[0]-=1
        
    
def controlleur()->None:
    """
    Controlleur:
        regarde si les billes peuvent être distribué.
            Si oui elle les distribue au travailleur, et les informe qu'ils peuvent travailler.
            sinon elle les met en attente.
    """
    logs = list()
    while working[0] > 0:
        if not queue_billes.empty():
            tab = queue_billes.get()
            identifiant_process = tab[0]
            nombre_de_billes_demande = tab[1]
            if billes_total[0] + nombre_de_billes_demande > 0:
                
                with mutex:
                    billes_total[0] += nombre_de_billes_demande
                logs.append(billes_total[0])
                retour[identifiant_process] = True
                
                #print(f"Je veux bien preter {nombre_de_billes_demande} à {identifiant_process}")
            else:
                queue_billes.put(tab)
                


    logs.append(billes_total[0])
    print(f"Ils ont tous finis de travailler. {logs}")
    return logs


if __name__ == '__main__':
    #mutex du sémaphore
    mutex = mp.Semaphore() 

    #valeurs 
    billes = 9
    nb_travailleurs = 4
    nb_prise = 4



    #tab partagé
    #retour = autorise le travailleur a reprendre.
    retour = mp.Array('i', nb_travailleurs)
    

    #nombre de bille actuel.
    billes_total = mp.Array('i', 1)
    billes_total[0]=billes
    

    #nombre de travailleur qui fonctionne pr le moment.
    working = mp.Array('i', 1)
    working[0]=nb_travailleurs


    #queue des demandes de bille.
    queue_billes = mp.Queue()

    #process controlleur.
    controlleur = mp.Process(target=controlleur, args= ())
    controlleur.start()


    #starts process
    start_travailleurs(nb_travailleurs,nb_prise)
    

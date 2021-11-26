import os,random,time
import multiprocessing as mp
from new_demandeur import fils_calculette




def start_calculettes(nb_calculette:int,queue_demande,queue_resultat)->None:
    print(f"Nous lancons {nb_calculette} calculette(s)")
    calcs = list()
    for i in range (nb_calculette):
        calcs.append(mp.Process(target=fils_calculette, args= (queue_demande,queue_resultat)))
    for calculette in calcs:
        calculette.start()

def server(nb_calculette:int)->None:
    queue_demande = mp.Queue()
    queue_resultat = mp.Queue()  
    start_calculettes(nb_calculette,queue_demande,queue_resultat) 
    while True :
        #time.sleep(0.5)
        print('−'* 60)
        # Le pere envoie au fils un calcul aléatoire à faire et récupère le résultat
        #opération:
        opd1 = random.randint(1,10)
        opd2 = random.randint(1,10)
        operateur=random.choice(['+','-', '*', '/'])
        str_commande = str(opd1) + operateur + str(opd2)
        print("Le père va demander à faire : ", str_commande)
        
        #demande opération
        queue_demande.put(str_commande)
        
        #recperation resultat
        res = queue_resultat.get()


        print("Le Pere a recu ", res)
        
            



if __name__ == "__main__" :
    server(4)
    
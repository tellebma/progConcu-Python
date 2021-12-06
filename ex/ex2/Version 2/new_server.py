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

def start_server(nb_server:int,queue_demande,queue_resultat)->None:
    print(f"Nous lancons {nb_server} server(s)")
    servers = list()
    for i in range (nb_server):
        servers.append(mp.Process(target=server, args= (queue_demande,queue_resultat)))
    for serv in servers:
        serv.start()

def server(queue_demande,queue_resultat)->None:
    operation_en_attente = False
    try :     
        while True :
            while not operation_en_attente:
                    
                time.sleep(0.8)
                #print('−'* 60)
                # Le pere envoie au fils un calcul aléatoire à faire et récupère le résultat
                #opération:
                opd1 = random.randint(1,10)
                opd2 = random.randint(1,10)
                operateur=random.choice(['+','-', '*', '/'])
                str_commande = [str(opd1) , operateur , str(opd2)]
                print(f"{JAUNE}{str(os.getpid())[4]}{BLEU}| Le père va demander à faire : {JAUNE}{str_commande}")
                
                #calc id:
                ident = int(str(random.random())[2:])


                #demande opération
                queue_demande.put([ident,str_commande])



                operation_en_attente = True

             
                while operation_en_attente:

                    #recperation resultat
                    tab = queue_resultat.get()
                    identifiant_get = tab[0]

                    if identifiant_get != ident:
                        queue_resultat.put(tab)
                    else:
                        res = tab[1]
                        fils_executant = tab[2]
                        print(f"{JAUNE}{str(os.getpid())[4]}{ROUGE}| résultat de {JAUNE}{str_commande} = {res} {ROUGE}par fils {fils_executant}")
                        operation_en_attente = False
            
    except KeyboardInterrupt:
        exit(0)
            
NORMAL = "\x1B[0m"        
BLEU = "\033[22;34m"
JAUNE = "\033[01;33m"
ROUGE = "\033[22;31m"

if __name__ == "__main__" :
    print(NORMAL)
    
    #Global var:
    nb_calculette = 15
    nb_server = 8


    #init queue:
    
            
    queue_demande = mp.Queue()
    queue_resultat = mp.Queue()

        
    #starts process
    start_calculettes(nb_calculette,queue_demande,queue_resultat)

    start_server(nb_server,queue_demande,queue_resultat)
    
    
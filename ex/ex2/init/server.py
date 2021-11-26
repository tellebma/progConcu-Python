import os,random,time
import multiprocessing as mp
from demandeur import fils_calculette
if __name__ == "__main__" :
    rpipe_reponse, wpipe_reponse = os.pipe()
    rpipe_commande, wpipe_commande = os.pipe()
    pid = os.fork()
    if pid == 0:
        fils_calculette(rpipe_commande, wpipe_reponse)
        assert False, 'fork du fils n a pas marché !' # Si échec, on affiche un message
    else :
        
        
        # On ferme les "portes" non utilisées
        os.close(wpipe_reponse)
        os.close(rpipe_commande)
        while True :


            # Le pere envoie au fils un calcul aléatoire à faire et récupère le résultat
            opd1 = random.randint(1,10)
            opd2 = random.randint(1,10)
            operateur=random.choice(['+', '*', '/'])
            str_commande = str(opd1) + operateur + str(opd2)
            print("Le père va demander à faire : ", str_commande)
            os.write(wpipe_commande, str_commande.encode())
            
            res = os.read(rpipe_reponse, 32)
            print("Le Pere a recu ", res)
            print('−'* 60)
            time.sleep(1)
import time,os,random
import multiprocessing as mp

def fils_calculette(queue_demande, queue_resultat):
    while True:    
        print('Bonjour du Fils', )
        cmd = queue_demande.get()
        print(f"Le fils {os.getpid()} a recu {cmd}")
        res=eval(cmd)
        #print("Dans fils, le résultat =", res)
        queue_resultat.put(res)
        print("Le fils a envoyé", res)


if __name__ == "__main__":
    fils_calculette()
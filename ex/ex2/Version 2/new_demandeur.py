import os
import multiprocessing as mp

def fils_calculette(queue_demande, queue_resultat):
    try:
            
        while True:    
            #print('Bonjour du Fils', )
            
            tab = queue_demande.get()
            ident = tab[0]
            cmd = tab[1]
            #print(f"\033[22;35mLe fils {os.getpid()} a recu {cmd}")
            if cmd[1] == "+":
                res = lambda a,b: a + b
            elif cmd[1] == "-":
                res = lambda a,b: a - b
            elif cmd[1] == "*":
                res = lambda a,b: a * b
            elif cmd[1] == "/":
                res = lambda a,b: a / b
            else:
                resultat=eval(cmd[0]+cmd[1]+cmd[2])
            
            if cmd[1] in ['+','-','*','/']:
                resultat = res(int(cmd[0]),int(cmd[2]))
            #res=eval(cmd)
            #print("Dans fils, le résultat =", res)
            queue_resultat.put([ident,resultat,os.getpid()])
            
            #print("Le fils a envoyé", res)
        
    except KeyboardInterrupt:
        exit(0)


if __name__ == "__main__":
    print("NE PAS LANCER CE FICHIER")
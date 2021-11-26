import time,os,random

def fils_calculette(rpipe_commande, wpipe_reponse):
    print('Bonjour du Fils', os.getpid())
    while True:
        cmd = os.read(rpipe_commande, 32)
        print("Le fils a recu ", cmd)
        res=eval(cmd)
        print("Dans fils, le résultat =", res)
        os.write(wpipe_reponse, str(res).encode())
        print("Le fils a envoyé", res)
        time.sleep(1)
    os._exit(0)


if __name__ == "__main__":
    fils_calculette()
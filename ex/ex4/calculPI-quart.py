#//////////////////////////////
import multiprocessing as mp
import random, time


# calculer le nbr de hits dans un cercle unitaire (utilisé par les différentes méthodes)
def frequence_de_hits_pour_n_essais(id_calculateur,nb_iteration:int)->None:
    #print(id_calculateur)
    count = 0
    for i in range(nb_iteration):
        x = random.random()
        y = random.random()
    # si le point est dans l’unit circle
        if x * x + y * y <= 1: count += 1
    with mutex:
        frequence_de_hits[id_calculateur]= count
# Nombre d’essai pour l’estimation


def calculateur()->float:
    #calc :
    for i in range(nombre_de_calculeurs):
        mes_process.append(mp.Process(target=frequence_de_hits_pour_n_essais, args= (i,int(nb_total_iteration/nombre_de_calculeurs))))
        mes_process[i].start()
        
        
    for i in range(nombre_de_calculeurs): 
        mes_process[i].join()
    
    total = 0
    for nombre_de_hit in frequence_de_hits: total += nombre_de_hit/nombre_de_calculeurs
    
    return total*nombre_de_calculeurs

if __name__ == '__main__':
    print("\x1B[0m",end="")
    nb_total_iteration = 10000000
    nombre_de_calculeurs = 4
    mutex = mp.Semaphore()
    frequence_de_hits = mp.Array('i', nombre_de_calculeurs)
    mes_process = list()
    start_time = time.time()

    total = calculateur()
    
    diff = time.time()-start_time
    
    #print(frequence_de_hits)
    #total = sum(frequence_de_hits)    
    temps = str(diff)[0:5]    
    print(f"{temps}s")
    
    
    print("Valeur estimée Pi par la méthode Mono−Processus : ", 4 * total / nb_total_iteration)


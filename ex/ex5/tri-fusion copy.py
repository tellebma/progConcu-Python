import math, random, time
from array import array
import multiprocessing as mp

def merge(left, right):
    tableau = array('i', []) # tableau vide qui reçoit les résultats
    while len(left) > 0 and len(right) > 0:
        if left[0] < right[0]: tableau.append(left.pop(0))
        else: tableau.append(right.pop(0))
    tableau += left + right
    return tableau

def merge_sort(ident):
    
    
    length_Tableau = len(Tableau)

    if length_Tableau <= 1: return Tableau
    mid = length_Tableau // 2
    tab_left = Tableau[0:mid]
    tab_right = Tableau[mid:]
    tab_left = merge_sort(tab_left)
    tab_right = merge_sort(tab_right)
    merged = merge(tab_left, tab_right)
    print(merged)
    #ident = [1,2,3] on veut [0,1,2]
    tab_return[ident-1] = merged


def version_de_base(N):
    """
    deprecated
    """
    print("Avant : ", Tab)
    start=time.time()
    Tab = merge_sort(Tab)
    end=time.time()
    print("Après : ", Tab)
    print("Le temps avec 1 seul Process = %f pour un tableau de %d eles " % ((end - start)*1000, N))
    print("Vérifions que le tri est correct −−> ", end='')
    try :
        assert(all([(Tab[i] <= Tab[i+1]) for i in range(N-1)]))
        print("Le tri est OK !")
    except : print(" Le tri n’a pas marché !")


def startProcess(nombre_process,N):
    tab_process = []
    
    
    tab = mp.Array('i', N)
    tab = [random.randint(0, 2 * N) for _ in range(N)]
    

    tab_return = mp.Array('i', nombre_process)


    first_value = 0
    nombre_el = int(N/nombre_process)

    start=time.time()
    for i in range(1,nombre_process+1):
        #print(i*nombre_el)
        print(tab[first_value:i*nombre_el])


        

        first_value = i*nombre_el+1


    for i in range(nombre_process):
        
    tab_process.append(mp.Process(target=merge_sort,args=(i,)))


    print("Start")
    start=time.time()
    for process in tab_process:
        process.start()
        process.join()
    end=time.time()
    print("c'est terminé !")
    print((end - start)*1000)

    for tab in tab_return:
        pass#print(tab)

if __name__ == '__main__':
    N = 100
    startProcess(5,N)
    
    #version_de_base(N)

"""
      ***********                  ***********
   *****************            *****************
 *********************        *********************
***********************      ***********************
************************    ************************
*************************  *************************
 **************************************************
  ************************************************
    ********************************************
      ****************************************
         **********************************
           ******************************
              ************************
                ********************
                   **************
                     **********
                       ******
                         **
"""

from multiprocessing import process
import random,time
import multiprocessing as mp
from array import array

def store_first_merge_sort(identifiant, tableau):
    resultats[identifiant]=merge_sort(tableau)

def merge(left, right):
    tableau = array('i', []) # tableau vide qui reçoit les résultats

    while len(left) > 0 and len(right) > 0:
        if left[0] < right[0]: tableau.append(left.pop(0))
        else: tableau.append(right.pop(0))

    tableau += left + right
    return tableau

def merge_sort(tableau):

    length_tableau = len(tableau)
    if length_tableau <= 1: return tableau
    mid = length_tableau // 2

    tableau[0:mid] = merge_sort(tableau[0:mid])
    tableau[mid:] = merge_sort(tableau[mid:])
    return merge(tableau[0:mid], tableau[mid:])

    
def parallel_merge_sort(array, nb_process):
    process = []
    # Divide the list in chunks
    step = int(length / nb_process)

    # Instantiate a multiprocessing.Manager object to
    # store the output of each process.
    # See example here
    # http://docs.python.org/library/multiprocessing.html#sharing-state-between-processes

    for n in range(nb_process):
        if n < nb_process - 1:#dernier element
            parti_tab_a_trier = array[n * step: (n + 1) * step]
        else:
            # tous les eleents restant
            parti_tab_a_trier = array[n * step:]
        
        print(type(parti_tab_a_trier))
        process.append(mp.Process(target=merge_sort, args= (parti_tab_a_trier)))
        
    
    for i in range(nb_process):
        print(f"je start un process")
        process[i].start()
        process[i].join()
        

    # finals merges

    #dernier merge des lists merges
    """merged = False
    newlist = list()
    while merged:
        for i in range(nb_process):
            newlist.append(merge(resultats[i],resultats[i+1]))
            resultats[i] = []
            resultats[i+1] = []
    """
        
    

    

    final_sorted_list = resultats
    print(final_sorted_list)
    return final_sorted_list


def verificationTableau(tableau):
    try :
        assert(all([(tableau[i] <= tableau[i+1]) for i in range(len(tableau)-1)]))
        print("Le tri est OK !")
    except : print(" Le tri n’a pas marché !")

def version_de_base(N):
    tab = array('i', [random.randint(0, 2 * N) for _ in range(N)])
    print("Avant : ", tab)
    start=time.time()
    #merge_sort(tab)
    process = list()
    step = int(length / N)

    for n in range(N):
        if n < N - 1:#dernier element
            parti_tab_a_trier = tab[n * step: (n + 1) * step]
        else:
            # tous les eleents restant
            parti_tab_a_trier = tab[n * step:]
        
        print(type(parti_tab_a_trier))
        process.append(mp.Process(target=merge_sort, args= (parti_tab_a_trier)))
    
    for i in range(N):
        process[i].start()
    
    
    #tab=merge(tab[0:N//2], tab[N//2:])
    end=time.time()
    print("Après : ", tab)
    print("Le temps avec 1 seul Process = %f pour un tableau de %d eles " % ((end - start)*1000, N))
    print("Vérifions que le tri est correct −−> ", end='')
    try :
        assert(all([(tab[i] <= tab[i+1]) for i in range(N-1)]))
        print("Le tri est OK !")
    except : 
        print(" Le tri n’a pas marché !") 

if __name__ == '__main__':
    N = 4 # nb_process
    # Randomize the length of our list
    length = 4

    resultats = mp.Array('i', N)

    # Create an unsorted list with random numbers
    tableau = array('i', [random.randint(0, 2 * N) for _ in range(length)])

    print('Starts parallel merge.')
    version_de_base(length)
    #parallel_sorted_list = parallel_merge_sort(tableau, N)
    print("Verification du tableau :")
    #verificationTableau(parallel_sorted_list)

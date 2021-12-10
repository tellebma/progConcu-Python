"""
FONCTIONNEL UNIQUEMENT 1 SEUL PROCESS
"""
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

def merge_sort(tableau):

    length_tableau = len(tableau)
    if length_tableau <= 1: return tableau
    mid = length_tableau // 2

    tableau[0:mid] = merge_sort(tableau[0:mid])
    tableau[mid:] = merge_sort(tableau[mid:])
    return merge(tableau[0:mid], tableau[mid:])


def version_de_base(N):
    tab = array('i', [random.randint(0, 2 * N) for _ in range(N)])
    print("Avant : ", tab)
    start=time.time()
    merge_sort(tab)
    tab=merge(tab[0:N//2], tab[N//2:])
    end=time.time()
    print("Après : ", tab)
    print("Le temps avec 1 seul Process = %f pour un tableau de %d eles " % ((end - start)*1000, N))
    print("Vérifions que le tri est correct −−> ", end='')
    try :
        assert(all([(tab[i] <= tab[i+1]) for i in range(N-1)]))
        print("Le tri est OK !")
    except : print(" Le tri n’a pas marché !")




if __name__ == '__main__':
 N = 100
 version_de_base(N)
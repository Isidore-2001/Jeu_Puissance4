
from render_connect4 import *
import random
import math
import copy
def init(nc,nr):
    return [[0 for i in range(nc)] for i in range(nr)]

def nr(g):
    """
    """
    return len(g)

def nc(g):
    return len(g[0])

def affichage(g):
    d= {2:"X", 1:"O", 0:"-"}
    res = "";
    for c in g:
        res2 = ""
        for c1 in c:
            res2+= d[c1]
        res2+="\n"
        res+=res2
    for k in g[0]:
        res+="="
    res+="\n"
    i = 0
    for k in g[0]:
        res+=str(i)
        i+=1
    print(res)
    
def colonne_valide(c,g):
    l = []
    
    if 0 <= c  and c < len(g[0]):
        for c1 in g:
            l.append(c1[c])
    return 0 in l

   
def grille_non_fini(g):
    return any([0 in c for c in g])
    
def demande(p,g):
    c = input("saisissez une colonne valide ")
    if colonne_valide(int(c),g):
        return int(c)
    else:
        return demande(p,g)
    
def laligne(c,g):
    i=0
    if colonne_valide(c,g):
        for c1 in g:
            if c1[c] ==0:
                i+=1
        
        return i
def laligne2(c,g):
    i=0
    if colonne_valide(c,g):
        for c1 in g:
            if c1[c] ==0:
                i+=1
        
    return i
                

def modif_grille(g,p,c):
    
   
    g[laligne(c,g)-1][c] = p
    
def is_align4(g,lc,p):
    i = 0
    
    while (i<= len(lc)-4):
           l = lc[i:i+4]
           l1 = []
           
           for c in l:
              
               
               if 0<=c[0] < nr(g) and 0<=c[1] < nc(g):
                   l1.append(g[c[0]][c[1]]==p )
           
           if all(l1) and len(l1)==4:
                return True
           
           i+=1
    return False
def lc_r(r,c):
    return [(r,c-3),(r,c-2),(r,c-1),(r,c),(r,c+1),(r,c+2),(r,c+3)]

def lc_c(r,c):
    return [(r-3,c),(r-2,c),(r-1,c),(r,c),(r+1,c),(r+2,c),(r+3,c)]

def lc_diagonale(r,c):
    l = []
    for i in range(7):
        l.append((r-3+i,c-3+i))
    return l
def lc_diagonale_2(r,c):
    l = []
    for i in range(7):
        l.append((r+3-i,c-3+i))
    return l
 
# (r−3,c+3)
def is_win(g,c,p):
    r = laligne2(c,g)
    
    if r != None:
        
        return any([is_align4(g,lc_r(r,c),p),is_align4(g,lc_c(r,c),p),
                    is_align4(g,lc_diagonale(r,c),p),is_align4(g,lc_diagonale_2(r,c),p)])
    return False

def get_colonne_valide(g):
    l = g[0]
    l1 = []
    i = 0
    for c in l:
        
        if c == 0:
            l1.append(i)
        i+=1
    return l1
def ia_aleat(g):
    print(get_colonne_valide(g))
    return random.choice(get_colonne_valide(g))

def evaluation(quadruplet):
    score = 0
    if 1 in quadruplet and not 2 in quadruplet:
        if quadruplet.count(1) == 1:
            score=1
        elif quadruplet.count(1) == 2:
            score = 10
        elif quadruplet.count(1) == 3:
            score = 1000
        elif quadruplet.count(1) == 4:
            score = 100000
    if 2 in quadruplet and not 1 in quadruplet:
        if quadruplet.count(2) == 1:
            score=-1
        elif quadruplet.count(2) == 2:
            score = -10
        elif quadruplet.count(2) == 3:
            score = -500
        elif quadruplet.count(2) == 4:
            score = -50000
    return score
    
        
def formation_de_quadruplet(g,c,r):
    l = []
    
    l1 = lc_r(r,c)[lc_r(r,c).index((r,c)):lc_r(r,c).index((r,c))+4]
    
    l2 = lc_c(r,c)[lc_c(r,c).index((r,c)):lc_c(r,c).index((r,c))+4]
    l3 = lc_diagonale(r,c)[lc_c(r,c).index((r,c)):lc_c(r,c).index((r,c))+4]
    l4 = lc_diagonale_2(r,c)[0:lc_c(r,c).index((r,c))+1]
    l.append(l1)
    l.append(l2)
    l.append(l3)
    l.append(l4)
    l_f = []
    for c in l:
        tmp = []
        for k in c:
            if 0 <= k[1] < nc(g) and  0 <= k[0] < nr(g):
                tmp.append(True)
            else:
                tmp.append(False)
        if all(tmp):
            l_f.append(c)
        
    return l_f
            
    
                    
def formation_quadruplet(g):
    i = 0
    j = 0
    l = []
    while i < len(g):
        j=0
        while j < len(g[i]):
            l+=formation_de_quadruplet(g,i,j)
            j+=1
        i+=1
    
    return l
        
def evaluation_g (g):
    score = 0
    k = formation_quadruplet(g)
    for c in k:
        tmp = [g[k[0]][k[1]] for k in c]
        score+=evaluation(tmp)
    return score
def terminal_node(g):
    return evaluation_g(g) < -50000 or evaluation_g(g) > 100000 or len(get_colonne_valide(g)) ==0
def unmove(g,c):
    g[laligne(c,g)][c] = 0



def minmax(g, profondeur,alpha, beta, maxPlayer):
    #draw_connect4(g)
    colonne = get_colonne_valide(g)
    tableau = copy.deepcopy(g)
    
    if terminal_node(g) or profondeur ==0 :
        
        if evaluation_g(g) < -50000:
            return (None, -50000)
        elif evaluation_g(g) > 100000:
            return (None, 100000)
        else:
            return (None, evaluation_g(g))
    if maxPlayer:
        value = -math.inf
        col = random.choice(colonne)
        if colonne != []:
            for c in colonne:
                tab = tableau.copy()
                
                if colonne_valide(c,g):
                    modif_grille(tab,1,c)
                    score = minmax(tab, profondeur-1,alpha,beta, False)[1]
                    
                   
                    if score > value:
                        value = score
                        col = c
                    alpha = max(alpha,value)
                    if alpha >= beta:
                        break
        return (col, value)
    else:
        value = +math.inf
        col = random.choice(colonne)
        if colonne != []:
            for c in colonne:
                tab = tableau.copy()
                
                if colonne_valide(c,g):
                    modif_grille(tab,2,c)
                    score = minmax(tab, profondeur-1,alpha,beta, True)[1]
                   
                    
                    if score < value:
                        value = score
                        col = c
                    beta = min(beta,value)
                    if alpha >= beta:
                        break
                    
        return (col, value)
        
            
    
def play(g,ia):
    p = random.randint(1,2)
    
    if p == 2:
        c= demande(2, g)
        
        p = 1
        
    else:
        if ia:
            c1 = minmax(g, 12,-math.inf,math.inf ,True)
            c = c1[0]
            if c ==None :
                c = ia_aleat(g)
        else:
            c = demande(p,g)
        p = 2
    
    modif_grille(g,p,c)
    affichage(g)
    draw_connect4(g)
    while grille_non_fini(g) and not is_win(g,c,p):
        
        if p == 2:
            c = demande(2, g)
        
            p = 1
        else:
            if ia:
                c1 = minmax(g, 12,-math.inf,math.inf ,True)
                c = c1[0]
                if c ==None :
                    c = ia_aleat(g)
            else:
                c = demande(p,g)
            p = 2
        f = lc_r(laligne(c,g) ,c)
        
        modif_grille(g,p,c)
        
        affichage(g)
        draw_connect4(g)
    
    
    if is_win(g,c,p):
        print("le joueur " + str(p) + " a gagné "+ "sur la colonne " + str(c) )
    
        
wait_quit()
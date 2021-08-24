from tkinter import *
from tkinter import font
from random import randint, random
import math

TEXT=30

render_data={"canvas":None,"root":None,"stop":False,"start":False,"dim":(6,7),"view":(500,500),"grid":[]}
	
def rgb(r,g,b):
  """
  renvoie une couleur au format hexadécimal (tkinter) à partir de r,g,b normalisés
  """
  assert (0<=r<=1 and 0<=g<=1 and 0<=b<=1),"r,g,b non normalisés :"+(r,g,b)
  return "#%02x%02x%02x"%(int(r*255),int(g*255),int(b*255))




def fill_circle(center,radius,color):
    """
    trace cercle de centre center=(x,y) de rayon radius de couleur color
    """
    render_data["canvas"].create_oval(center[0]-radius,center[1]-radius,center[0]+radius,center[1]+radius,fill=color,width=2)
        
def fill_rectangle(tl,diag,color):
    """
    trace rectangle de top-left tl, de diagonale diag, et de couleur color
    """
    render_data["canvas"].create_rectangle(tl[0],tl[1],tl[0]+diag[0],tl[1]+diag[1],fill=color,width=2)


	
def on_quit():
  """
  callback lors du click sur fermeture de fenêtre
  """
  render_data["stop"]=True

  
def which_color(player):
  """
  renvoie la couleur du disque player (0 => pas de disque, 1 => joueur 1, 2 => joueur 2)
  """
  disk_color=(rgb(1,1,1),rgb(1,0,0),rgb(1,1,0))
  return disk_color[player]

def draw_grid4():
  """
  trace le plateau de jeu (grille des disques donnée par render_data["grid"])
  """
  if render_data["stop"]: return None

  canvas=render_data["canvas"]
  canvas.delete("all")

  nbr=render_data["dim"][0]
  nbc=render_data["dim"][1]
  w=render_data["view"][0]
  h=render_data["view"][1]

  g=render_data["grid"]
    
  # draw grid
  fill_rectangle((0,0),(w,h-30),rgb(0,0,1))

  stepx=w/nbc
  stepy=(h-30)/nbr

  y=stepy/2
  for r in range(nbr):
    x=stepx/2
    for c in range(nbc):
      fill_circle((x,y),stepx/2-stepx*0.08,which_color(g[r][c]))
      x+=stepx
    y+=stepy
    
  # draw text (column names)
  stepx=w/nbc
  x=stepx/2
  y-=stepy*0.45
  for c in range(nbc):
    canvas.create_text(x,y,text=str(c),width=stepx,anchor=N)
    x+=stepx
  
  #
  canvas.update()

def draw_align(lc):
  """
  trace des points dans les cases de la liste lc (liste de coordonnées de la grille)
  """
  if render_data["stop"]: return None

  canvas=render_data["canvas"]

  nbr=render_data["dim"][0]
  nbc=render_data["dim"][1]
  w=render_data["view"][0]
  h=render_data["view"][1]

  stepx=w/nbc
  stepy=(h-30)/nbr
  for c in lc:
    fill_circle((c[1]*stepx+stepx/2,c[0]*stepy+stepy/2),stepx*0.1,rgb(0,1,0))
  canvas.update()


def configure_draw(nr,nc):
  """
  modifie les dimensions de l'affichage du plateau de jeu selon les nombres de ligne nr et colonne nc (tient compte du ratio largeur/hauteur de la fenêtre graphique)
  """
  dim=(nr,nc)
  render_data["dim"]=dim

  render_data["grid"]=[[0 for i in range(nc)] for j in range(nr)]

  canvas=render_data["canvas"]
  view=(canvas.winfo_width(),canvas.winfo_height()-TEXT)
  dim=render_data["dim"]
  rx=view[0]/dim[1]
  ry=(view[1]-30)/dim[0]
  if (rx<ry):
    v=(view[0],dim[0]*rx+30)
  else:
    v=(dim[1]*ry,view[1])
  render_data["view"]=v

def set_draw_disk(r,c,player):
  """
  modifie la grille avec un disque player à la ligne r, colonne c
  """
  render_data["grid"][r][c]=player
  
def wait_quit():
  """
  attend explicitement la fermeture de la fenêtre graphique
  """
  if (render_data["start"]):
    canvas=render_data["canvas"]
    while not(render_data["stop"]):
      canvas.update()
    root=render_data["root"]
    root.destroy()
    

def init_draw(w=450,h=480):
  """
  initialise la fenêtre graphique (canvas de largeur w et hauteur h)
  """
  render_data["view"]=(w,h-TEXT)

  root=Tk()
  root.protocol("WM_DELETE_WINDOW", on_quit)
  canvas=Canvas(root,width=w,height=h)
  canvas["background"]=rgb(1,1,1)
  #canvas.bind("<Configure>",configure)
  canvas.pack(fill=BOTH,expand=1)
  render_data["canvas"]=canvas
  render_data["root"]=root
  canvas.winfo_toplevel().title("Connect 4")
  canvas.update()
  render_data["start"]=True

def draw_connect4(g):
  """
  trace le plateau de jeu correspondant à la grille g
  CU : g = liste de lignes; chaque ligne = liste de valeurs 0,1,2; len(ligne) identiques
  """
  nr=len(g)
  if nr!=0:
    nc=len(g[0])
  else:
    nc=0
  if not(render_data["start"]):
    init_draw()
    
  configure_draw(nr,nc)  
  for i in range(nr):
    for j in range(nc):
      set_draw_disk(i,j,g[i][j])
  draw_grid4()




  

if __name__=="__main__":
  g=[[2,0,0,0],[1,0,0,2],[1,0,2,1]]
  draw_connect4(g)
  wait_quit()



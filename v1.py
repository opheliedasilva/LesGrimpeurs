#!/usr/bin/env python2

# usage : python v1.py start_prot_only.pdb md_prot_only_skip100.pdb CA

import sys, os
from math import sqrt
import matplotlib.pyplot as plt
from scipy.stats.stats import pearsonr
import numpy as np

#PLAN
	#Changements conformationnels globaux

		#Calcul rayon de Giration (distance entre CdM et residu le plus eloigne du CdM)
		#et RMSD de toutes les conformations par rapport a la ref

		#Representation de la variation Giration/RMSD, Giration/Temps, RMSD/Temps.

	#Changements conformationnels locaux
	
		#RMSD de chaque residu de chaque conformation par rapport a sa position dans la ref
			#Region flexible = region dont residus ont un grand RMSD

		#Enfouissement : Calcul distance entre CdM de chaque residu et CdM du centre de la prot

		#Comparer enfouissement des residus et RMSD des residus
			#Regions flexibles enfouies ou en surface ?

		#Calcul RMSD et Enfouissement moyen pour chaque residu de chaque conformation vs reference
			#Representation Graphique

#-----------------------------------------------------------------------
def	__usage(arguments) :
	if len(arguments) != 4 :
		__erreurMes()
	if ((arguments[3] != 'CA') & (arguments[3] != 'all')) :
		__erreurMes()

def __erreurMes() :
	print "ATTENTION : Mauvais usage de Barstar \nArguments necessaires :\t<fileRef.pdb> <fileConf.pdb> <nom_atome>\n"
	print "fileRef.pdb :\t\tfichier pdb contenant la conformation de reference"
	print "fileConf.pdb :\t\tfichiers pdb contenant les conformations issues de la dynamique moleculaire"
	print "nom_atome :\t\tCA ou all (Methode de calcul du centre de masse)"
	sys.exit(0)

def conformation_analysis(l_dict) :
	centreMasseCalc(l_dict)
	RMSD(l_dict)
	distance(l_dict)
	rayonGiration(l_dict)
	corEnfouissementFlexibilite(l_dict[1])

#-----------------------------------------------------------------------
def dictionnaire() :
	global argv
	
	# Verification : les fichiers ont ete fournis dans le bon ordre
	__usage(sys.argv)
	
	# Transformation des fichiers pdb en dictionnaires
	dico1 = __parsePDBMultiConf(sys.argv[1])
	dico2 = __parsePDBMultiConf(sys.argv[2])

	# Verification ordre des fichiers
	if (__verifData(dico1, dico2) == 1) :
		__inversion(dico1, dico2)
	
	return [dico1, dico2]


def __parsePDBMultiConf(infile) :
	"""
	Cette fonction permet de parser un fichier pdb. Conversion en 
	dictionnaire directement utilisable dans le script.
	"""

	try:
		f = open(infile, "r")
		lines = f.readlines()
		f.close()
	except:
		print("Erreur chargement fichier : verifiez existance fichier et relancer\n")
		sys.exit(0) # Arret execution programme

	d_PDB = dict()
	d_PDB["liste_conformations"] = list()

	for element in lines :		
		if element[0:5] == "MODEL" :
			conformation = element[10:14]
			d_PDB["liste_conformations"].append(conformation)
			d_PDB[conformation] = dict()
			d_PDB[conformation]["liste_n_residus"] = list()
			d_PDB[conformation]["liste_seq_residus"] = list()
			d_PDB[conformation]["liste_residus"] = list()
        
		if element[0:4] == "ATOM" :
			residus = element[17:20]
			n_res = element[23:26].strip() 
			atome = element[13:16].strip() 
			identifiant = element[7:11].strip() 
			x = float(element[30:38])
			y = float(element[38:46])
			z = float(element[46:54])
			
			if not n_res in d_PDB[conformation]["liste_n_residus"] :
				d_PDB[conformation]["liste_n_residus"].append(n_res)
				d_PDB[conformation]["liste_seq_residus"].append(residus)
				
				if not residus in d_PDB[conformation]["liste_residus"] :
					d_PDB[conformation]["liste_residus"].append(residus)
				
				d_PDB[conformation][n_res] = dict()
				d_PDB[conformation][n_res]["liste_atomes"] = list()
			
			d_PDB[conformation][n_res]["liste_atomes"].append(atome)
			d_PDB[conformation][n_res][atome] = dict()
			d_PDB[conformation][n_res][atome]["x"] = x
			d_PDB[conformation][n_res][atome]["y"] = y
			d_PDB[conformation][n_res][atome]["z"] = z
			d_PDB[conformation][n_res][atome]["id"] = identifiant

	return d_PDB


#-----------------------------------------------------------------------
def __verifData(dico1, dico2) :
	'''
	Verification des fichiers : 
		- dico1 contient la conformation de reference
		- dico2 contient l'ensemble des conformations pour tous les temps consideres
	S'ils ont ete renseignes dans le bon ordre, la fonction retourne 0
	sinon elle retourne 1 : necessite d'inverser les dictionnaires
	'''
	if (dico1 == dico2) :
		print "Erreur : les dictionnaires sont identiques"
		sys.exit(0)
	if ((len(dico1["liste_conformations"]) != 1) | (len(dico2["liste_conformations"]) == 1)) :
		return 1

def __inversion(dico1, dico2) :
		d_tmp = dico2
		dico2 = dico1
		dico1 = d_tmp





#~ #Faire la verification que la methode de calcul est connue

#~ class DataException(Exception):
    #~ def __init__(self,raison):
        #~ self.raison = raison
    
    #~ def __str__(self):
        #~ return self.raison

#~ def exactData(dico1,dico2):
    
    #~ if :
		#~ raise DataException("Erreur : les conformations n'ont pas toutes les memes residus")
	
	#~ elif (dico1 == dico2) :
		#~ raise DataException("Erreur : les dictionnaires sont identiques")
    #~ else :
		#~ # Fonction qui permet de verifier si les fichiers ont ete fournis dans le bon sens
		#~ # sinon retourne 1 --> indique la necessite d'inverser les dictionnaires correspondants
		#~ if ((len(dico1["liste_conformations"]) != 1) | (len(dico2["liste_conformations"]) == 1)) :
			#~ return 1



#-----------------------------------------------------------------------
# PARTIE 2 CALCUL DU CENTRE DE MASSE
#-----------------------------------------------------------------------

def centreMasseCalc(l_dict) :
	#~ global argv
	
	#~ centreMasse = __choixMeth(sys.argv[3])
	__centreMasseResidus(l_dict[0])
	__centreMasseResidus(l_dict[1])
	__centreMasseProteine(l_dict[0])
	__centreMasseProteine(l_dict[1])

def choixMeth() :
	'''
	Deux methodes de calcul sont proposees :
	- soit en utilisant la position des carbones alpha (hyp. representatif des residus)
	- soit en calculant la position des residus a partir de l'ensemble des atomes les consituant
	'''
	global argv
	
	arg = sys.argv[3]
	
	if arg == "CA" :
		return "CM_CA"
	else :
		return "CM_moyAll"

	
#~ def __centreMasseProteine(d_prot, centreMasse) :
def __centreMasseProteine(d_prot) :
	'''
		Fonction qui calcule le centre de masse des proteines. Cela
		correspond a la position moyenne des residus la constituant.
		
		@param : indique la methode du calcul de centre de masse CM_CA ou CM_moyAll
	'''
	global centreMasse
	
	l_CM = []
	l_CMx = [] # stockage des coordonnees des CM des residus sur l'axe x
	l_CMy = [] # stockage des coordonnees des CM des residus sur l'axe y
	l_CMz = [] # stockage des coordonnees des CM des residus sur l'axe z
		
	for conf in d_prot["liste_conformations"] :
		l_CM = [list(),list(),list()] # liste de la somme des coordonnees des CM
		cpt = 0 # cpt du nombre de residus
		
		for resid in d_prot[conf]["liste_n_residus"] :
			cpt += 1
			l_CM[0].append(d_prot[conf][resid][centreMasse]["x"])
			l_CM[1].append(d_prot[conf][resid][centreMasse]["y"])
			l_CM[2].append(d_prot[conf][resid][centreMasse]["z"])
		l_CMx.append(moyenne(l_CM[0]))
		l_CMy.append(moyenne(l_CM[1]))
		l_CMz.append(moyenne(l_CM[2]))
	d_prot["liste_CM_x"] = l_CMx
	d_prot["liste_CM_y"] = l_CMy
	d_prot["liste_CM_z"] = l_CMz
	
	return d_prot

#~ def __centreMasseResidus(d_prot, centreMasse) :
def __centreMasseResidus(d_prot) :
	'''
	Le centre d'un masse d'un residus peut etre considere comme etant :
		- la position moyenne de ses atomes
		- la position de ses carbones alpha
	'''
	global centreMasse
	
	if centreMasse == "CM_CA" :
		return __centreMasseResCa(d_prot)
	return __centreMasseResAll(d_prot)


def __centreMasseResCa(d_prot) :
	'''		
	Fonction qui calcule le centre de masse des residus
	Le centre de masse d'un residus correspond a la position de son
	carbone alpha
	
	@param diconnaire de la proteine avec une ou plusieurs conformations
	@return dictionnaire de la proteine avec la valeur des centres
	de masse "CA" des residus ajoutes
	'''
	
	# Pour toutes les conformations de la proteine
	for conf in d_prot["liste_conformations"] :
		# Pour tous les residus de chaque conformation de la proteine
		
		d_prot[conf]["CM_res"] = dict()
		d_prot[conf]["CM_res"]["x"] = list()
		d_prot[conf]["CM_res"]["y"] = list()
		d_prot[conf]["CM_res"]["z"] = list()
		for resid in d_prot[conf]["liste_n_residus"] :
			d_prot[conf][resid]["CM_CA"] = dict()
			d_prot[conf][resid]["CM_CA"]["x"] = d_prot[conf][resid]["CA"]["x"]
			d_prot[conf][resid]["CM_CA"]["y"] = d_prot[conf][resid]["CA"]["y"]
			d_prot[conf][resid]["CM_CA"]["z"] = d_prot[conf][resid]["CA"]["z"]
			
			d_prot[conf]["CM_res"]["x"].append(d_prot[conf][resid]["CA"]["x"])
			d_prot[conf]["CM_res"]["y"].append(d_prot[conf][resid]["CA"]["y"])
			d_prot[conf]["CM_res"]["z"].append(d_prot[conf][resid]["CA"]["z"])

def __centreMasseResAll(d_prot) :
	'''		
	Fonction qui calcule le centre de masse des residus
	Le centre de masse d'un residus correspond a la position moyenne
	des atomes le constituant
	
	@param dictionnaire de la proteine avec une ou plusieurs conformations
	@return dictionnaire de la proteine avec la valeur des centres de masse 
	"all" des residus ajoutes
	'''
	
	# Pour toutes les conformations de la proteine
	for conf in d_prot["liste_conformations"] :
		# Pour tous les residus de chaque conformation de la proteine
		for resid in d_prot[conf]["liste_n_residus"] :
			lcoord = [list(),list(),list()] # stockage coordonnees [x,y,z] pour tous les atomes de chaque residus
			
			
			d_prot[conf]["CM_res"] = dict()
			d_prot[conf]["CM_res"]["x"] = list()
			d_prot[conf]["CM_res"]["y"] = list()
			d_prot[conf]["CM_res"]["z"] = list()

			for atom in d_prot[conf][resid]["liste_atomes"] :
				lcoord[0].append(d_prot[conf][resid][atom]["x"])
				lcoord[1].append(d_prot[conf][resid][atom]["y"])
				lcoord[2].append(d_prot[conf][resid][atom]["z"])

			xmoy = moyenne(lcoord[0])
			ymoy = moyenne(lcoord[1])
			zmoy = moyenne(lcoord[2])
			
			d_prot[conf][resid]["CM_moyAll"] = dict()
			d_prot[conf][resid]["CM_moyAll"]["x"] = xmoy
			d_prot[conf][resid]["CM_moyAll"]["y"] = ymoy
			d_prot[conf][resid]["CM_moyAll"]["z"] = zmoy

			d_prot[conf]["CM_res"]["x"].append(xmoy)
			d_prot[conf]["CM_res"]["y"].append(ymoy)
			d_prot[conf]["CM_res"]["z"].append(zmoy)

#-----------------------------------------------------------------------
# PARTIE 3 : CALCUL DU RMSD
#-----------------------------------------------------------------------
'''
Le RMSD est considere comme la distance moyenne entre les residus
	
'''

def RMSD(l_dict) :
	'''	
	Fonction permettant de realiser l'ensemble des calculs relatifs au RMSD
	C'est la seule qui peut etre utilisee par l'utilisateur
	'''
	__RMSDresidus(l_dict[0],l_dict[1])
	__RMSDconf(l_dict[1])
	__RMSDres(l_dict[0], l_dict[1])

def __RMSDresidus(d_ref, d_conf) :
	'''
	Calcul du RMSD de chaque residu
	'''
	global centreMasse
	
	REF = d_ref["liste_conformations"][0] # il n'y a qu'une conformation : celle de reference
	
	for conf in d_conf["liste_conformations"] :
		d_conf[conf]["RMSD"] = list()
		for resid in d_conf[conf]["liste_n_residus"] :
			xref = d_ref[REF][resid][centreMasse]["x"]
			yref = d_ref[REF][resid][centreMasse]["y"]
			zref = d_ref[REF][resid][centreMasse]["z"]

			xconf = d_conf[conf][resid][centreMasse]["x"]
			yconf = d_conf[conf][resid][centreMasse]["y"]
			zconf = d_conf[conf][resid][centreMasse]["z"]
			
			d_conf[conf]["RMSD"].append(sqrt((xref-xconf)**2 + (yref-yconf)**2 + (zref-zconf)**2))
	
def __RMSDconf(d_conf) :
	'''
	Calcul du RMSD de maniere globale a la conformation
	Moyenne du RMSD des residus
	'''
	
	d_conf["RMSDmoy"] = list()
	d_conf["RMSDmoy_sd"] = list()
	
	for conf in d_conf["liste_conformations"] :
		d_conf["RMSDmoy"].append(moyenne(d_conf[conf]["RMSD"]))
		d_conf["RMSDmoy_sd"].append(ecart_type(d_conf[conf]["RMSD"]))

def __RMSDres(d_ref,d_conf) :
	'''
	Calcul du RMSD de maniere locale
	Moyenne du RMSD en chaque position a partir de l'ensemble des conformations
	'''
	
	l_res = d_ref[d_ref["liste_conformations"][0]]["liste_n_residus"]

	d_ref["RMSDres_mean"] = list()
	d_ref["RMSDres_sd"] = list()

	for i in range(len(l_res)) :
		l_rmsd = list() # liste contenant les valeurs des RMSD d'un residu pour toutes ses conformations
		for conf in d_conf["liste_conformations"] :
			l_rmsd.append(d_conf[conf]["RMSD"][i])
		
		d_ref["RMSDres_mean"].append(moyenne(l_rmsd))
		d_ref["RMSDres_sd"].append(ecart_type(l_rmsd))

#~ def __RMSDratio(d_ref, d_conf) :
	#~ '''
	#~ Calcul du ratio entre le RSMD moyen d'une conformation et le RMSD
	#~ moyen de la conformation de reference
	#~ '''
	#~ ref = d_ref["RMSDmoy"][0]
	#~ d_conf["ratio_RMSD"] = [x/ref for x in d_conf["RMSDmoy"]]





#-----------------------------------------------------------------------
# PARTIE 4 : DISTANCE
#-----------------------------------------------------------------------
'''
Calcul de la distance de chaque residu au centre de Masse de la conformation
La distance calculee pour un residu represente son enfouissement au sein de la conformation
Plus la distance est grand, plus ce residu est en peripherie (faible enfouissement relatif)
'''

def distance(l_dict) :
	__distanceConf(l_dict[0])
	__distanceConf(l_dict[1])
	__distanceRes(l_dict[0], l_dict[1])
	
	
def __distanceConf(d_conf) :

	global centreMasse
	# pour chaque conformation, son centre de masse :
	xconf = d_conf["liste_CM_x"]
	yconf = d_conf["liste_CM_y"]
	zconf = d_conf["liste_CM_z"]
	
	d_conf["distance_moy"] = list()
	d_conf["distance_sd"] = list()

	for conf in d_conf["liste_conformations"] :
		l_dist = []
		
		for resid in d_conf[conf]["liste_n_residus"] :
			i=0
			xres = d_conf[conf][resid][centreMasse]["x"]
			yres = d_conf[conf][resid][centreMasse]["y"]
			zres = d_conf[conf][resid][centreMasse]["z"]
			
			distance = sqrt((xres-xconf[i])**2 + (yres-yconf[i])**2 + (zres-zconf[i])**2)
			l_dist.append(distance)
			
			i += 1
		
		d_conf[conf]["enfouissement"] = l_dist
		d_conf["distance_moy"].append(moyenne(l_dist))
		d_conf["distance_sd"].append(ecart_type(l_dist))


def __distanceRes(d_ref, d_conf) :
	'''
	Calcul de la distance moyenne de chaque residu au centre de masse de la proteine
	Distance locale moyenne
	'''

	l_res = d_ref[d_ref["liste_conformations"][0]]["liste_n_residus"]

	d_ref["enfRes_mean"] = list()
	d_ref["enfRes_sd"] = list()

	for i in range(len(l_res)) :
		l_enf = list()
		for conf in d_conf["liste_conformations"] :
			l_enf.append(d_conf[conf]["enfouissement"][i])
		
		d_ref["enfRes_mean"].append(moyenne(l_enf))
		d_ref["enfRes_sd"].append(ecart_type(l_enf))

#-----------------------------------------------------------------------
# PARTIE 5 : RAYON DE GIRATION
#-----------------------------------------------------------------------
'''
Le rayon de giration est calcule comme etant la distance maximale entre 
un residu et le centre de masse d'une conformation
C'est la distance associee au residu a l'enfouissement maximal
'''

def __maxDistance(d_prot) :
	d_prot["rayonGiration"] = list()
	for conf in d_prot["liste_conformations"] :
		d_prot["rayonGiration"].append(max(d_prot[conf]["enfouissement"]))
	return d_prot["rayonGiration"]

def rayonGiration(l_dict) :
	d_ref = l_dict[0]
	d_conf = l_dict[1]
		
	rayon = __maxDistance(d_conf)
	ref = __maxDistance(d_ref)[0]
	
	d_conf["ratio_giration"] = [x/ref for x in rayon]





#-----------------------------------------------------------------------
# FONCTIONS DE CALCUL STATISTIQUE
#-----------------------------------------------------------------------

def moyenne(liste) :
	return sum(liste)/len(liste)

def variance(liste) :
	n = len(liste)
	if (n != 0) :
		m = moyenne(liste)**2
		s = sum([x**2 for x in liste])
		return s/n-m
	print "ERREUR : Dictionnaire sans conformation associee"
	sys.exit(1)

def ecart_type(liste) :
	return sqrt(variance(liste))
        


#-----------------------------------------------------------------------
# REPRESENTATION DES DONNEES
#-----------------------------------------------------------------------

def corEnfouissementFlexibilite(d_conf) :
	'''
	Fonction qui permet de visualiser la correlation entre l'enfouissement
	des residus et la flexibilite des regions
	La flexibilite augmente avec la distance des residus aux CdM
	--> calcul de la correlation
	'''
	d_conf["corEnfFlexi"] = [list(), list()] # correlation et pvaleur
	for conf in d_conf["liste_conformations"] :
		if(d_conf[conf]["RMSD"] == [0] * len(d_conf[conf]["RMSD"])) :
			cor = [1,0]
		else :
			cor = pearsonr(d_conf[conf]["enfouissement"],d_conf[conf]["RMSD"])
		d_conf["corEnfFlexi"][0].append(cor[0])
		d_conf["corEnfFlexi"][1].append(cor[1])
	return d_conf["corEnfFlexi"]



#-----------------------------------------------------------------------
# PARTIE 6 : ECRITURE DES RESULTATS
#-----------------------------------------------------------------------

def ecriture(l_dict) :
	output1 = __verificationfFichier("res_barstar_globaux.txt") # nom de fichier par defaut, mais on ne veut pas ecraser des resultats precedents
	output2 = __verificationfFichier("res_barstar_locaux.txt")
	
	x = input("Indiquez le nombre de decimales souhaitees :\t")

	__outputGlobaux(output1, l_dict[0], l_dict[1], x)
	__outputLocaux(output2, l_dict[0], x)



def __verificationfFichier(output) :
	
	if (os.path.exists(output)) :
		decision = raw_input("Fichier de sortie "+str(output)+" deja existant : Voulez vous l'ecraser ? O/N\n")
	
		while ((decision != 'O') & (decision != 'o') & (decision != 'N')  & (decision != 'n')) :
			print "Erreur : Repondre O pour oui ou N pour non" 
			decision = raw_input("Fichier de sortie deja existant : Voulez vous l'ecraser ? O/N\n")
	
		if ((decision == 'N') | (decision == 'n')) :
			while os.path.exists(output) :
				output = raw_input("Nom de fichier de sortie deja existant : entrez un nouveau nom de fichier : \n")
	return output



def __outputGlobaux(output, d_ref, d_conf, x) :
	try:
		f = open(output, "w")
		
		texte = "Conformation\t|\tRayon Giration\t|\tDistance\t|\tRMSD\t|\tRatio Giration\t|\tcorrelation\t(p-value)\n"

		rayonG_ref = d_ref["rayonGiration"][0]
		texte += "REF\t|\t"+str(round(rayonG_ref,x))+"\t|\t0\n"
		for i in range(len(d_conf["liste_conformations"])) :
			num = d_conf["liste_conformations"][i].strip()
			rayonG = d_conf["rayonGiration"][i]
			d_moy = d_conf["distance_moy"][i]
			d_sd = d_conf["distance_sd"][i]
			rmsd = d_conf["RMSDmoy"][i]
			rmsd_sd = d_conf["RMSDmoy_sd"][i]
			ratio_gir = d_conf["ratio_giration"][i]
			cor = d_conf["corEnfFlexi"][0][i]
			pvalue = d_conf["corEnfFlexi"][1][i]
			texte += str(num)+"\t|\t"+str(round(rayonG,x))+"\t|\t"+str(round(d_moy,x))+"\t(+/-"+str(round(d_sd,x))+")\t|\t"+str(round(rmsd,x))+"\t(+/-"+str(round(rmsd_sd,x))+")\t|\t"+str(round(ratio_gir,x))+"\t|\t"+str(round(cor,x))+"\t("+str(round(pvalue,x))+")\n"

		f.write(texte)
		f.close()		

	except:
		print("Erreur chargement fichier global\n")
		sys.exit(0)

def __outputLocaux(output, d_ref, x) :
	
	try:
		f = open(output, "w")
		
		texte = "Residus\t|\t Nom \t|\tRMSD (+/- ecart-type)\t|\tDistance residu/CdM (+/- ecart-type)\n"
		conf_ref = d_ref["liste_conformations"][0]
		lres = d_ref[conf_ref]["liste_n_residus"]
		
		for i in range(len(lres)) :
			res = lres[i]
			nom = d_ref[d_ref["liste_conformations"][0]]["liste_seq_residus"][i]
			rmsd = d_ref["RMSDres_mean"][i]
			rmsd_sd = d_ref["RMSDres_sd"][i]
			d = d_ref["enfRes_mean"][i]
			d_sd = d_ref["enfRes_sd"][i]
			
			texte += str(res)+"\t|\t"+nom+"\t|\t"+str(round(rmsd,x))+"\t(+/-"+str(round(rmsd_sd,x))+")\t|\t"+str(round(d,x))+"\t(+/-"+str(round(d_sd,x))+")\n"
			
		f.write(texte)
		f.close()
		
	except:
		print("Erreur chargement fichier local\n")
		sys.exit(0)

#-----------------------------------------------------------------------
# GRAPHIQUES
#-----------------------------------------------------------------------
#~ def timeList (infile): #Recupere et met dans un liste le temps des differentes conformations
    #~ time = []
    #~ file = open(infile,"r")
    #~ lines = file.readlines()
    #~ for line in lines :
        #~ if line[0:5] == "TITLE":
            #~ timet=line[65:80].strip()
            #~ time.append(timet)
    #~ #print temps
    #~ file.close()
    #~ return(time)


#~ def plotRMSD_Giration(listRMSD, listGiration):
	#~ y=np.array(listRMSD)
	#~ x=np.array(listGiration)
	#~ plt.scatter(x,y,c='red')
	#~ axes = plt.gca()
	#~ axes.set_xlim(-30, 2100)
	#~ axes.set_ylim(-1,25)
	#~ plt.title('RMSD en fonction de la Giration')
	#~ plt.legend(['RMSD','Giration'])
	#~ plt.show()

#~ def plotRMSD_Temps(listRMSD, listTemps):

#~ def plotGiration_Temps(listGiration, listTemps):

def plotRes(l_dict) :
	plotGlobal(l_dict[1])
	plotLocal(l_dict[0])

def plotGlobal(d_conf) :
	plotGiration(d_conf)
	plotDistance(d_conf)
	plotGlobalRMSD(d_conf)
	plotFlexibiteEnfouissement(d_conf)
	
def plotGiration(d_conf) :
	plt.subplot(211)
	plt.plot(d_conf["rayonGiration"])
	plt.xlabel('Conformation')
	plt.ylabel('Rayon Giration')
	
	plt.subplot(212)
	plt.plot(d_conf["ratio_giration"])
	plt.xlabel('Conformation')
	plt.ylabel('Ratio Rayon Giration Conformation/Reference')
	
	plt.show()

def plotDistance(d_conf) :
	plt.subplot(311)
	plt.plot(d_conf["distance_moy"])
	plt.xlabel('Conformation')
	plt.ylabel('Distance moyenne')
	
	plt.subplot(312)
	plt.plot(d_conf["distance_sd"])
	plt.xlabel('Conformation')
	plt.ylabel('Ecart type')
	
	plt.subplot(313)
	moy = d_conf["distance_moy"]
	sd = d_conf["distance_sd"]
	moy_s = [x+y for (x,y) in zip(moy,sd)]
	moy_i = [x-y for (x,y) in zip(moy,sd)]

	plt.plot(moy, "b", label = "Distance moyenne")
	plt.plot(moy_s, "r--", label = "+/- ecart-type")
	plt.plot(moy_i, "r--",)
	plt.xlabel('Conformation')
	plt.ylabel('Distance')
	
	plt.show()

def plotGlobalRMSD(d_conf) :
	plt.subplot(311)
	plt.plot(d_conf["RMSDmoy"])
	plt.xlabel('Conformation')
	plt.ylabel('RMSD moyen')

	plt.subplot(212)
	plt.plot(d_conf["RMSDmoy_sd"])
	plt.xlabel('Conformation')
	plt.ylabel('Ecart type')

	plt.subplot(313)
	moy = d_conf["RMSDmoy"]
	sd = d_conf["RMSDmoy_sd"]
	moy_s = [x+y for (x,y) in zip(moy,sd)]
	moy_i = [x-y for (x,y) in zip(moy,sd)]
	
	plt.plot(moy, "b", label = "RMSD moyen")
	plt.plot(moy_s, "r--", label = "+/- ecart-type")
	plt.plot(moy_i, "r--",)
	plt.xlabel('Conformation')
	plt.ylabel('RMSD')

	plt.show()
	
def plotFlexibiteEnfouissement(d_conf) :
	plt.subplot(211)
	plt.plot(d_conf["corEnfFlexi"][0])
	plt.xlabel('Conformation')
	plt.ylabel('Correlation')
	
	plt.subplot(212)
	plt.plot(d_conf["corEnfFlexi"][1])
	plt.xlabel('Conformation')
	plt.ylabel('p-valeur')
	
	plt.show()

#-----------------------------------------------------------------------
def plotLocal(d_ref) :
	plotDistanceLocal(d_ref)
	plotRMSDLocal(d_ref)

def plotDistanceLocal(d_ref) :
	plt.subplot(311)
	plt.plot(d_ref["enfRes_mean"])
	plt.xlabel('Conformation')
	plt.ylabel('Distance')
	
	plt.subplot(312)
	plt.plot(d_ref["enfRes_sd"])
	plt.xlabel('Conformation')
	plt.ylabel('ecart type')
	
	plt.subplot(3,1,3)
	moy = d_ref["enfRes_mean"]
	sd = d_ref["enfRes_sd"]
	moy_s = [x+y for (x,y) in zip(moy,sd)]
	moy_i = [x-y for (x,y) in zip(moy,sd)]

	plt.plot(moy, "b", label = "Distance moyenne")
	plt.plot(moy_s, "r--", label = "+/- ecart-type")
	plt.plot(moy_i, "r--",)
	plt.xlabel('Conformation')
	plt.ylabel('Distance')
	plt.show()



def plotRMSDLocal(d_ref) :
	plt.subplot(311)
	plt.plot(d_ref["RMSDres_mean"])
	plt.xlabel('Conformation')
	plt.ylabel('RMSD')
	
	plt.subplot(312)
	plt.plot(d_ref["RMSDres_sd"])
	plt.xlabel('Conformation')
	plt.ylabel('ecart type')

	plt.subplot(313)
	moy = d_ref["RMSDres_mean"]
	sd = d_ref["RMSDres_sd"]
	moy_s = [x+y for (x,y) in zip(moy,sd)]
	moy_i = [x-y for (x,y) in zip(moy,sd)]
	
	plt.plot(moy, "b", label = "RMSD moyen")
	plt.plot(moy_s, "r--", label = "+/- ecart-type")
	plt.plot(moy_i, "r--",)
	plt.xlabel('Conformation')
	plt.ylabel('RMSD')


#-----------------------------------------------------------------------
# MAIN

if __name__ == '__main__':
	
	liste_dictionnaire = dictionnaire()	# creation des dictionnaires
	centreMasse = choixMeth()
	conformation_analysis(liste_dictionnaire) # calcul des variables d'interet
	ecriture(liste_dictionnaire) # ecriture dans un fichier
	
	plotRes(liste_dictionnaire) # graphiques



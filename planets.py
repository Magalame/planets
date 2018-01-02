#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#print "Content-Type: text/plain;charset=utf-8"
#print
#Most of data come from http://articles.adsabs.harvard.edu/cgi-bin/nph-iarticle_query?1994A%26A...282..663S&amp;data_type=PDF_HIGH&amp;whole_paper=YES&amp;type=PRINTER&amp;filetype=.pdf
import cgi
import numpy as np
from datetime import datetime,timedelta
import time

#Constantes:
AU=149597870700 #in meters

#Earth
epsEarth=0.0167086342 #eps stands for eccentricity
periodEarth=365*86400+6*3600+9*60+9.76 #in seconds
aEarth=1.0000010178*AU #semi major axis
pEarth=aEarth*(1-epsEarth**2) #we define p as such and then use r=p/(1+eps*cos(theta))
lastperiEarth=datetime(2017, 01, 04, 14, 17)     #last perihelion for earthwith yyyy/mm/dd/hh/mm/ss/mmmm, from wikipedia

#Moon
epsMoon=0.0555545526
periodMoon=27*86400+13*3600+18*60+33.2 #We use anomalistic month
aMoon=383397791.6 # in meters too
pMoon=aMoon*(1-epsMoon**2)
lastperiMoon=datetime(2016, 12, 12, 23, 28) # from https://www.timeanddate.com/astronomy/moon/distance.html

def TaylorInit(eps,M): #The three functions below implement the algo found at http://murison.alpheratz.net/dynamics/twobody/KeplerIterations_summary.pdf
        t34=eps**2
        t35=eps*t34
        t33=np.cos(M)
#       print "t33 t34 t35",t33,t34,t35
        return M+(-1/2*t35+eps+(t34+3/2*t33*t35)*t33)*np.sin(M)

def TaylorExp(eps,M,init):
        t1=np.cos(init)
        t2=-1+eps*t1
        t3=np.sin(init)
        t4=eps*t3
        t5=-init+t4+M
        t6=t5/(1/2*t5*t4/2+t2)
#       print "t1 t2 t3 t4 t5 t6",t1,t2,t3,t4,t5,t6
        return t5/((1/2*t3-1/6*t1*t6)*eps*t6+t2)

def EccAno(eps,M):
        precision=10e-10
        Mnorm=M%(2*np.pi)
        Ecc0=TaylorInit(eps,Mnorm)
#       print "Taylor init:", Ecc0
        deltaEcc=precision+1
        count=0
        while(deltaEcc>precision):
                Ecc=Ecc0-TaylorExp(eps,Mnorm,Ecc0)
                deltaEcc=abs(Ecc-Ecc0)
                Ecc0=Ecc
                count+=1
                if count==100:
                        print "Seems like the process is strangely long"
                        print "Value of eccentric anormality found until here:",Ecc
                        return -1
#       print "Nombre d'itérations:",count
#       print "Valeur trouvée:",Ecc
        return Ecc

#EccAno(0.5,(np.pi)/2,10e-10)

def cos(eps,Ecc):
#       print "cos:",((np.cos(Ecc)-eps)/(1-eps*np.cos(Ecc)))
        return ((np.cos(Ecc)-eps)/(1-eps*np.cos(Ecc)))

def sin(eps,Ecc):
#       print "sin:",(((1-eps**2)**0.5*np.sin(Ecc))/(1-eps*np.cos(Ecc)))
        return (((1-eps**2)**0.5*np.sin(Ecc))/(1-eps*np.cos(Ecc)))

def theta(eps,M):
        Ecc=EccAno(eps,M)
        cosPlanet=cos(eps,Ecc) #We save it to use it latter in the radial equation
        return np.arctan2(sin(eps,Ecc),cosPlanet),cosPlanet

def radius(cosPlanet,eps,p):
        return p/(1+eps*cosPlanet)

def coordonneesEarth():
        t=(datetime.utcnow()-lastperiEarth).total_seconds()
        MEarth=(2*np.pi)/periodEarth*t
        thetaEarth,cosEarth=theta(epsEarth,MEarth)
        return radius(cosEarth,epsEarth,pEarth),thetaEarth

def coordonneesMoon():
        t=(datetime.utcnow()-lastperiMoon).total_seconds()
        MMoon=(2*np.pi)/periodMoon*t
        thetaMoon,cosMoon=theta(epsMoon,MMoon)
        return radius(cosMoon,epsMoon,pMoon),thetaMoon

#while(1):

#deltimeEarth=(datetime.utcnow()-lastperiEarth).total_seconds()
#        print "Coordonnées de la Terre:",coordonneesEarth(deltime),"on",datetime.utcnow().strftime("%A %d %B %H h %M m %S s")
"""resultatEarth=coordonneesEarth()
resultatMoon=coordonneesMoon()
print resultatEarth,resultatMoon"""
#return result
        #time.sleep(5)
while(1):

     #   deltime=(datetime.utcnow()-lastperi).total_seconds()
#        print "Coordonnées de la Terre:",coordonneesEarth(deltime),"on",datetime.utcnow().strftime("%A %d %B %H h %M m %S s")
        resultatEarth=coordonneesEarth()
        resultatMoon=coordonneesMoon()
        result = str(resultatEarth[0]) + " " + str(resultatEarth[1]) + "\n"
        result = result + str(resultatMoon[0]) + " " + str(resultatMoon[1]) + "\n"

        writeth = open("result","wb")
        writeth.write(result)
        #print result
        time.sleep(0.5)

writeth.close()

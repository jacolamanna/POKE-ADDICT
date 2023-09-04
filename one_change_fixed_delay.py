import RPi.GPIO as GPIO
import sys
import time
import csv
from datetime import datetime
from numpy.random import seed
from numpy.random import shuffle
from . import function_DD


#definisco il vettore parametri
param=[
       "type_of_exp", "One_change_fixed_delay", #1
       "t_drop", 0.1, 
       "t_vac", 10.0, 
       "dt_vac",10.0,
       "after_session_delay", 20, #9
       "light_on_secs", 20.0,
       "punishment_seconds", 0.0, 
       "serious_session_number", 10,
       "sampling_time", 0.1, 
       "n_drop1", 20,
       "n_drop2", 20, #21
       "delay_1", 0,
       "delay_2", 0,
       "after_session_delay", 0.0,
       "n_flash", 4,
       "dt_flash", .1, #31
       "training", 1,   # 1 per farlo, 0 per saltarlo
       "N_trining", 4, #AGGIUNGERE I PARAMETRI DEL TRAINING QUI SOTTO 
       "light_on_training", 300.0,
       "punishment_training", 0.0,
       "training_after_session_delay", 6, #41
       "N_BACK", 3,
       "d_magnitude", 5, #49
       "date", datetime.today(),
       "rat_id", "1_control",   
       ]
       
       
file1 = open("./In_case_of_emergency.txt","a") #salviamo i dati in questo foglio txt (da creare se non esiste)
file1.write(str(param)+"\n")
file1.close()


#definisco le porte e le spengo tutte       
led1=0
led2=0
poke1=0
poke2=0
val_juice=0
val_vac=0

GPIO.setmode(GPIO.BCM)
GPIO.setup(poke1,GPIO.IN)
GPIO.setup(poke2,GPIO.IN)
GPIO.setup(led1,GPIO.OUT)
GPIO.output(led1,GPIO.LOW)
GPIO.setup(led2,GPIO.OUT)
GPIO.output(led2,GPIO.LOW)
GPIO.setup(val_juice,GPIO.OUT)
GPIO.output(val_juice,GPIO.LOW)
GPIO.setup(val_vac,GPIO.OUT)
GPIO.output(val_vac,GPIO.LOW)

#DEFINISCO FUNZIONI:  
# funzione per attivare il rilascio di succo e il vuoto
def J_flow(t_drop, n_drop, dt_vac, t_vac):
 for i in range(n_drop):
   GPIO.output(val_juice,GPIO.HIGH)
   sleep(t_drop)
   GPIO.output(val_juice,GPIO.LOW)
   sleep(t_drop)
   
  sleep(dt_vac)
  GPIO.output(val_vac,GPIO.HIGH)
  sleep(t_vac)
  GPIO.output(val_vac,GPIO.LOW)
  
  
  
# funzione per far lampeggiare un led
def flashing(led,n_flash,dt_flash):  
 for i in range(n_flash):
  GPIO.output(led,GPIO.HIGH)
  sleep(dt_flash)
  GPIO.output(led,GPIO.LOW)
  sleep(dt_flash)
  
#funzione per il training (bisogna definire prima pero alcuni valori)         
def exposion(param, m1,m2,d1,d2,led1,led2,poke1,poke2):

 for block in range(param[15]): #quanti blocchi facciamo in tutto 
  if param[33]==1: #lo obblighiamo a scegliere?  
   for session_training in range(param[35]):
 
    print("Training session n°")
    print(session)
    start = time.time() 
 
    if CHOICE==1:  #inverto le porte (per eliminare mettere choiche >-1)
     if led==led1:
      led=led2
      poke=poke2
      d=d2
      m=m2
    else:
      led=led1
      poke=poke1
      d=d1[-1]
      m=m1[-1]
   
   
    counter=0
    CHOICE=0
    GPIO.output(led,GPIO.HIGH)
 
    while counter<(param[37]*(1/param[17])): #sono in cerca dello stimolo per il tempo in cui la luce è accesa
 
     if  GPIO.input(poke)==FALSE:
      CHOICE=1
      counter=(param[37]*(1/param[17]))
      stop = time.time()
      rt=stop-start
      print(rt)
      hit=1
      flashing(led,param[21],param[23]) 
 
     sleep(param[17])
     counter=counter+1
  
    if CHOICE==1:
     print("HIT!")
     sleep(d)
     J_flow(param[3], m, param[7],param[5])
  
 
    else:
     print("Failed!")
     if param[39]>0.0:
      GPIO.output(led,GPIO.LOW)
      sleep(param[39])
     stop = time.time()
     rt=stop-start
     print(rt)
     hit=0
  
    outcomes=['training', 1, 'hit', hit, 'rt', rt, 'poke', poke, 'session', session, 'D', d, 'M', m]  
    file1 = open("./In_case_of_emergency.txt","a") #salviamo i dati in questo foglio txt (da creare se non esiste)
    file1.write(str(outcomes)+"\n")
    file1.close()   

    f = open('/home/pi/Desktop/data.csv', 'a') #salviamo il .csv perchè più facile da importare e analizzare
    listone= otucomes + param
    writer = csv.writer(f)
    writer.writerow(listone)
    print("I'm recording...")
    sleep(param[41])
    
    return


#funzione per la vera sessione
def block_sessions(param,m1,m2,d1,d2,led1,led2,poke1,poke2):
 for session in range(param[45]):
   print("Serious session n°")
   print(session)
   start = time.time()


      
   counter=0
   CHOICE=0
   GPIO.output(led1,GPIO.HIGH)
   GPIO.output(led2,GPIO.HIGH)
 
   while counter<(param[11]*(1/param[17])): #sono in cerca dello stimolo per il tempo in cui la luce è accesa
 
    if  GPIO.input(poke1)==FALSE:
     CHOICE=1
     counter=(param[11]*(1/param[17]))
     stop = time.time()
     rt=stop-start
     print(rt)
     flashing(led1,param[29],param[31])
     flashing(led2,param[29],param[31])    
   
   
    if  GPIO.input(poke2)==FALSE:
     CHOICE=2   
     counter=(param[11]*(1/param[17]))
     stop = time.time()
     rt=stop-start
     print(rt)
     flashing(led1,param[29],param[31])
     flashing(led2,param[29],param[31])          
 
    sleep(param[17])
    counter=counter+1
  
   if CHOICE==1:
    print("Ratto in 1")
    print(rt)
    sleep(d1[-1:)
    J_flow(param[3], m1[-1], param[7],param[5])
 
   if CHOICE==2:
    print("Ratto in 2")
    print(rt)
    sleep(d2[-1])
    J_flow(param[3], m2[-1], param[7],param[5]) 
 
   if CHOICE==0:
    print("Failed!")
    if param[13]>0.0:
     GPIO.output(led1,GPIO.LOW)
     GPIO.output(led2,GPIO.LOW)
     sleep(param[13])
    stop = time.time()
    rt=stop-start
    print(rt)



   choice.append(CHOICE) 
   outcomes=['training', 0,'hit', choice[-1], 'rt', rt, 'poke', poke, 'session', session, 'M1', m1[-1],'M2', m2,'D1', d1[-1],'D2', d2]


   file1 = open("./In_case_of_emergency.txt","a") #salviamo i dati in questo foglio txt (da creare se non esiste)
   file1.write(str(outcomes)+"\n")
   file1.close()   

   f = open('/home/pi/Desktop/data.csv', 'a') #salviamo il .csv perchè più facile da importare e analizzare
   listone= otucomes + param
   writer = csv.writer(f)
   writer.writerow(listone)
   sleep(param[27])
  return choice

   
  
#lancio l'algoritmo
end=o
choice=[]
d1=[param[23]]
d2=[param[25]]
m1=[param[19]]
m2=[param[21]]
CHOICE=0
led=led1
poke=poke1
d=d1
m=m1
countdown=0
aggiunta=param[49]

while end==0: #forse devo aggiungere anche l'invertito

 choice=[]
 if param[33]==1:
  exposion(param, m1,m2,d1,d2,led1,led2,poke1,poke2)
 
 block_sessions(param,m1,m2,d1,d2,led1,led2,poke1,poke2):
 
 if mode(choice[-param[43]:])==1 and countdown==0: #sceglie quello instantaneo
   m2=m2+aggiunta

      
 if mode(choice[-param[43]:])==2 and aggiunta >1:
     countdown=1
     m2=m2 - round(aggiunta)
     aggiunta=aggiunta/2
   
 if mode(choice[-param[43]:])==1 and countdown==1 and aggiunta >1: #sceglie quello instantaneo
    aggiunta=aggiunta/2
    m2=m2 + round(aggiunta)
    
 if aggiunta <=1:
    end=1   
    print('Solution found! This is the END')
   
 
 
 
 







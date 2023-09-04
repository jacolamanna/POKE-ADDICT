import RPi.GPIO as GPIO
import sys
import time
import csv
from datetime import datetime
from numpy.random import seed
from numpy.random import shuffle


#definisco il vettore parametri
param=[
       "type_of_exp", "training",
       "t_drop", 0.2,
       "t_vac", 10.0,
       "dt_vac",10.0,
       "n_drop", 20,
       "light_on_secs", 20.0,
       "punishment_seconds", 0.0, 
       "cycle_number", 100.0,
       "sampling_time", 0.1, 
       "after_session_delay", 0,
       "n_flash", 4,
       "dt_flash", .1,
       "delay", 0.0,
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


  
#lancio il training
choiche=0
led=led1
poke=poke1
for session in range(param[15]):
 print("session n°")
 print(session)
 start = time.time()

 
 if choiche==1:  #inverto le porte (per eliminare mettere choiche >-1)
  if led==led1:
   led=led2
   poke=poke2
  else:
   led=led1
   poke=poke1
   
   
 counter=0
 choiche=0
 GPIO.output(led,GPIO.HIGH)
 
 while counter<(param[11]*(1/param[17])): #sono in cerca dello stimolo per il tempo in cui la luce è accesa
 
  if  GPIO.input(poke)==FALSE:
   choiche=1
   counter=(param[11]*(1/param[17]))
   stop = time.time()
   rt=stop-start
   print(rt)
   hit=1
   flashing(led,param[21],param[23]) 
 
  sleep(param[17])
  counter=counter+1
  
 if choiche==1:
  print("HIT!")
  sleep(param(25))
  J_flow(param[3], param[9], param[7],param[5])
  
 
 else:
  print("Failed!")
  if param[13]>0.0:
   GPIO.output(led,GPIO.LOW)
   
  sleep(param[13])
  stop = time.time()
  rt=stop-start
  print(rt)
  hit=0
  
  
outcomes=['hit', hit, 'rt', rt, 'poke', poke, 'session', session]  
file1 = open("./In_case_of_emergency.txt","a") #salviamo i dati in questo foglio txt (da creare se non esiste)
file1.write(str(outcomes)+"\n")
file1.close()   

f = open('/home/pi/Desktop/data.csv', 'a') #salviamo il .csv perchè più facile da importare e analizzare
listone= otucomes + param
writer = csv.writer(f)
writer.writerow(listone)

print("I'm recording...")
sleep(param[19])
  
 
 
 
  
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
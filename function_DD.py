# Le Funzioni che mi servono per lanciare i protocolli sperimentali
from statistics import mode

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
  
  
# funzione per aggiustare il ritardo e dimensione dello stimolo automaticamente
def adj_val(m1,m2,d1,d2,choice_seq, N_BACK, UPDATE, d_delay, d_magnitude, starting_session): #funzione di aggiustamento

# m1,m2,d1,d2,choice_seq sono tutti vettori con i valori del passato 
# N_BACK, UPDATE sono: quanto tornare indietro e ogni quanto aggiornare il sistema
# d_delay, d_magnitude corrispondono a quanto devo aumentare ritardo e quantità
# starting_session: quando iniziare a fare gli aggiustamenti (starting_session > si di UPDATE che di N_BACK)

 if length(choice_seq)%UPDATE==0 and length(choice_seq)>=starting_session: #controllo per vedere ogni quanto aggiornare 
 
 
  
   if mode(choice_seq[-N_BACK:])>1.5: # meglio la moda (the problem of no-choice)
     
      if d2[-2] == d2[-1]:  #controllo se ho aumentato già il delay, aumento la magnitude dell'altro
         d2.append(d2[-1] + d_delay)
         d1.append(d1[-1])
         m1.append(m1[-1])
         m2.append(m2[-1])
         
      else:        
         d2.append(d2[-1])
         d1.append(d1[-1])
         m1.append(m1[-1] + d_magnitude)
         m2.append(m2[-1])
         
   if mode(choice_seq[-N_BACK:])<1.5:  #se viene scelto maggiormente il 2
   
         if d1[-2] == d1[-1]:  
         d1.append(d1[-1] + d_delay)
         d2.append(d2[-1])
         m1.append(m1[-1])
         m2.append(m2[-1])
         
      else:        
         d2.append(d2[-1])
         d1.append(d1[-1])
         m1.append(m1[-1])
         m2.append(m2[-1]+ d_magnitude)
         

  
         
return m1,m2,d1,d2
         
         
#funzione di aggiustamento di un solo valore         
def adj_val_one_choice(m1,d1,choice_seq, N_BACK, d_delay, d_magnitude):

# m, d, choice_seq sono tutti vettori con i valori del passato 
# N_BACK: quanto tornare indietro e ogni quanto aggiornare il sistema
# d_delay, d_magnitude corrispondono a quanto devo aumentare ritardo e quantità

#cosa fare se non sceglie
  
   if mode(choice_seq[-N_BACK:])>1.5: # Choice is between 1 or 2 (the problem of no-choice)... facciamo la mediana
         d1.append(d1[-1])
         m1.append(m1[-1] + d_magnitude)
    
         
      else:        
         d1.append(d1[-1]+ d_delay)
         m1.append(m1[-1])
         
         
 return m1,d1
         
         
         
         
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
 
   else:
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




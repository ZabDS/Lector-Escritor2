import logging
import threading
import time

global info

def Escritor(lock,barrier,cond):
    global info
    
    print(threading.current_thread().name,
          'Esperando en la barrera con {} hilos más'.format(barrier.n_waiting))
    worker_id = barrier.wait()

    with cond:
        cond.notifyAll()
        print("Poniendo los recursos disponibles")
        
    while True:
        flag=lock.acquire(0)
        try:
            if flag:
                logging.debug("Accedió al libro")
                info.append("Hola")
                time.sleep(.5)
            else:
                logging.debug("Intentó acceder al libro sin éxito")
                time.sleep(.2)
        finally:
            if flag:
                lock.release()
                break
    logging.debug("Termino de escribir")


def Lector(lock,cond):
    global info
    
    with cond:
        cond.wait()
        print("Entrando al recurso")
                
    while True:
        flag=lock.acquire(0)
        try:
            if flag:
                logging.debug("Accedió al libro")
                print(info)
                time.sleep(.5)
            else:
                logging.debug("Intentó acceder al libro sin éxito")
                time.sleep(.2)
        finally:
            if flag:
                lock.release()
                break
    logging.debug("Terminado")
    
logging.basicConfig(
    level=logging.DEBUG,
    format='(%(threadName)-10s) %(message)s',
)
    
info=[]

barrier = threading.Barrier(2)
lock = threading.Lock()
condition = threading.Condition()


Lectores = [threading.Thread(target=Lector,args=(lock,condition,), name='Lector-%s'%i)
              for i in range(3) ]

for L in Lectores:
    print(L.name, 'Iniciando')
    L.start()
    time.sleep(.2)

Escritores = [threading.Thread(target=Escritor,args=(lock,barrier,condition,), name='Escritor-%s'%i)
              for i in range(2) ]

for E in Escritores:
    E.start()
    time.sleep(.2)

for L in Lectores:
    L.join()
    
for E in Escritores:
    E.join()
    
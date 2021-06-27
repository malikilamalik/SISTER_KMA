# import paho mqtt
import paho.mqtt.client as mqtt
# import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCServer

# import SimpleXMLRPCRequestHandler
from xmlrpc.server import SimpleXMLRPCRequestHandler
import threading
import uuid

# Restrict the access to path /RPC2 only
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Create the RPC server 
server = SimpleXMLRPCServer(("26.53.0.146", 32621), requestHandler=RequestHandler)
server.register_introspection_functions()

# buat callback on_publish untuk publish data
########################################
def on_publish(client, userdata, result):
    print("Pemenang Berhasil Diumumkan \n")
    pass
# definisikan nama broker yang akan digunakan
broker_address = "broker.hivemq.com"
client = mqtt.Client("KMA_SERVER")

client.connect(broker_address, port=1883)

candidate_list = {
    "SNSD" : 5,
    "2NE1" : 20
}

kode_vote = []   
    
    # ---critical section---
    # create a lock to prevent race condition when client vote
mutex = threading.Lock()
    
# create a function named vote_candidate()
def vote_candidate(code, x):
        
    # critical section started, acquire the lock
    mutex.acquire()
    print(code)
    for candidate in candidate_list:
        if x in candidate_list:
            for kode in kode_vote:
                if code in kode :
                    if(kode[code] == False):
                        kode[code] = True
                        candidate_list[x] += 1
                        mutex.release()
                        return x ,"Berhasil di vote"
                    else:
                        mutex.release()
                        return"Kode Vote Sudah Digunakan"
        else :
            message = x, "Tidak Ada"
        
        
    # critical section ended, release the lock
    mutex.release()
        # return msg --IMPORTANT--
    return message
    
# register function vote_candidate() as "vote"
server.register_function(vote_candidate, name="vote")

# create a function named publish_pemenang()
def publish_pemenang():
    mutex.acquire()
    skor = 0
    key = ''
    for candidate in candidate_list:
        if candidate_list[candidate] > skor:
            skor = candidate_list[candidate]
            key = candidate
    total_vote = 0
    for candidate in candidate_list:
        total_vote += candidate_list[candidate]
    message = "\nPEMENANG KMA ADALAH : %s\nDENGAN PEROLEHAN : %s\nLEADERBORD\n" % (str(key),str(skor))
    for candidate in candidate_list:
       message = message + '%s = %s Jumlah Vote : %s\n' % (str(candidate),str(candidate_list[candidate] / total_vote * 100),str(candidate_list[candidate]))
    mutex.release()
    client.publish("KMA_WINNER", message)
    return message

server.register_function(publish_pemenang, name="publish_pemenang")

# create a function named vote_candidate()
def check_code(code):
    mutex.acquire()
    for kode in kode_vote:
        if code in kode :
            if(kode[code] == False):
                mutex.release()
                return True
    mutex.release()
    return False
    
    # register function vote_candidate() as "vote"

server.register_function(check_code, name="check_code")

# create a function named generate_code()
def generate_code():
        
    # critical section started, acquire the lock
    mutex.acquire()
    kode = uuid.uuid1()
    print(kode)
    dict_vote = {
        str(kode) : False,
        }
    kode_vote.append(dict_vote)
    mutex.release()
        
    # return msg --IMPORTANT--
    return str(kode)
    
# register function vote_candidate() as "code"
server.register_function(generate_code, name="generate_code")

# create a function named get_code()
def get_code():
    return kode_vote

# create a function named get_candidate()
def get_candidate():
    return candidate_list

# register function vote_candidate() as "code"
server.register_function(get_candidate, name="get_candidate")
# register function vote_candidate() as "code"
server.register_function(get_code, name="get_code")


# create a function named querry_result
def querry_result():
        # critical section started
    mutex.acquire()
    total_vote = 0
    for candidate in candidate_list:
        total_vote += candidate_list[candidate]
    message = "Total vote : %s \n" % (total_vote)
    for candidate in candidate_list:
         message = message + '%s = %s Jumlah Vote : %s\n' % (str(candidate),str(candidate_list[candidate] / total_vote * 100),str(candidate_list[candidate]))
        # critical section ended
    mutex.release() 
        # return msg --IMPORTANT--
    return message
        
    # register querry_result as "querry"
server.register_function(querry_result)


    # Run the server -- serve forever
server.serve_forever()



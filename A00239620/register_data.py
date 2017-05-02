import psutil
from model import Data, db
import threading
import time

class RegisterTimer(threading.Thread):
    def __init__(self, seconds):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.seconds = seconds
        psutil.cpu_percent()
        time.sleep(1)
        

    def run(self):
        while not self.event.is_set():
            
            cpu = psutil.cpu_percent()
            mem = psutil.virtual_memory().available
            disk = psutil.disk_usage('/').free
            t = int(time.time())
            data = Data(event_time=t, cpu_usage=cpu, free_ram=mem, free_disk=disk)
            db.session.add(data)
            db.session.commit()


            _count = Data.query.count()
            if _count > 100:
                deletable = Data.query.order_by(Data.event_time).first()
                db.session.delete(deletable)
                db.session.commit()

            self.event.wait(self.seconds)
            

    
    def stop(self):
        self.event.set()
    

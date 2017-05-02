from model import Data
import json

def data_history(size):    
    return Data.query.order_by(Data.event_time.desc()).limit(size)

def get_cpu_history(size):
    
    if size > 100: return 'size must be less that 100', 404

    data_list = data_history(size)
    ret = []

    for d in data_list:
        ret.append("{0}%".format(d.cpu_usage))
    return ret

def get_free_ram_history(size):
    
    if size > 100: return 'size must be less that 100', 404

    data_list = data_history(size)
    ret = []

    for d in data_list:
        ret.append("{0} bytes".format(d.free_ram))
    return ret  

def get_free_disk_history(size):
    
    if size > 100: return 'size must be less that 100', 404

    data_list = data_history(size)
    ret = []

    for d in data_list:
        ret.append("{0} bytes".format(d.free_disk))
    return ret


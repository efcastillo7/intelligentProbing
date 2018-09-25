from __future__ import (unicode_literals, division, print_function,
                        absolute_import)
import sys
sys.path.insert(0, '/home/ryu/ryu/intelligentProbing/')
#from write_csv import *
import os.path as path
import time
import argparse
sys.path.insert(0, '/home/ryu/ryu/ryu/app/intelligentProbing/database/')
#import ConnectionBD_v2


def get_percent(process):
    try:
        return process.cpu_percent()
    except AttributeError:
        return process.get_cpu_percent()


def get_memory(process):
    try:
        return process.memory_info()
    except AttributeError:
        return process.get_memory_info()


def all_children(pr):
    processes = []
    children = []
    try:
        children = pr.children()
    except AttributeError:
        children = pr.get_children()
    except Exception:  # pragma: no cover
        pass

    for child in children:
        processes.append(child)
        processes += all_children(child)
    return processes


def main(process_id_or_command,probing_f,duration,interval):

    # Attach to process
    try:
        pid = int(process_id_or_command)
        print("Attaching to process {0}".format(pid))
        sprocess = None
    except Exception:
        import subprocess
        command = process_id_or_command
        print("Starting up command '{0}' and attaching to process"
              .format(command))
        sprocess = subprocess.Popen(command, shell=True)
        pid = sprocess.pid

    cpu_usage = monitor(pid, probing_f,duration,interval)

    if sprocess is not None:
        sprocess.kill()
    return  cpu_usage

def monitor(pid, probing_f=None,duration=None, interval=None):
    
    import psutil
    pr = psutil.Process(pid)
    # Record start time
    start_time = time.time()
    log = {}
    log['times'] = []
    log['cpu'] = []
    log['mem_real'] = []
    log['mem_virtual'] = []

    # Start main event loop
    while True:
    
        # Find current time
        current_time = time.time()
    
        try:
            pr_status = pr.status()
        except TypeError:  # psutil < 2.0
            pr_status = pr.status
        except psutil.NoSuchProcess:  # pragma: no cover
            break
    
        # Check if process status indicates we should exit
        if pr_status in [psutil.STATUS_ZOMBIE, psutil.STATUS_DEAD]:
            print("Process finished ({0:.2f} seconds)"
                  .format(current_time - start_time))
            break
    
        # Check if we have reached the maximum time
        if duration is not None and current_time - start_time > duration:
            break
    
        # Get current CPU and memory
        try:
            current_cpu = get_percent(pr)
            current_mem = get_memory(pr)
        except Exception:
            break
        current_mem_real = current_mem.rss / 1024. ** 2
        current_mem_virtual = current_mem.vms / 1024. ** 2
    
        if probing_f:
            dict_data = [{
                'TIME': current_time - start_time,
                'CPU': current_cpu,
                'REAL_MB': current_mem_real,
                'VIRTUAL_MB': current_mem_virtual
            }]
            # logfile_csv = 'cpu_usage_' + probing_f + '.csv'
            # WriteDictToCSV(logfile_csv,csv_columns,dict_data)
            cpu_data = {}
            cpu_data['times'] = current_time - start_time
            cpu_data['cpu'] = current_cpu
            cpu_data['real_mb'] = current_mem_real
            cpu_data['virtual_mb'] = current_mem_virtual
            # ConnectionBD_v2.insertStatcpu(cpu_data)
            #print("CPU",current_mem_real)
    
        if interval is not None:
            time.sleep(interval)
        #print("CPUxxxxx", current_mem_real)
        if current_mem_real > 100:
            current_mem_real = current_mem_real/10
        return current_mem_real
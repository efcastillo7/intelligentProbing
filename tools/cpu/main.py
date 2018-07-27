#https://github.com/astrofrog/psrecord

# sudo find / -name "psrecord"	

from __future__ import (unicode_literals, division, print_function,
                        absolute_import)
import sys
sys.path.insert(0, '/home/efcastillo/ryu/ryu/app/intelligentProbing/tools/')
from write_csv import *
import os.path as path

import time
import argparse


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


def main():

    parser = argparse.ArgumentParser(
        description='Record CPU and memory usage for a process')

    parser.add_argument('process_id_or_command', type=str,
                        help='the process id or command')

    parser.add_argument('--log', type=str,
                        help='output the statistics to a file')

    parser.add_argument('--plot', type=str,
                        help='output the statistics to a plot')

    parser.add_argument('--probing_f', type=str,
                        help='output the statistics to a csv')

    parser.add_argument('--duration', type=float,
                        help='how long to record for (in seconds). If not '
                             'specified, the recording is continuous until '
                             'the job exits.')

    parser.add_argument('--interval', type=float,
                        help='how long to wait between each sample (in '
                             'seconds). By default the process is sampled '
                             'as often as possible.')

    parser.add_argument('--include-children',
                        help='include sub-processes in statistics (results '
                             'in a slower maximum sampling rate).',
                        action='store_true')

    args = parser.parse_args()

    # Attach to process
    try:
        pid = int(args.process_id_or_command)
        print("Attaching to process {0}".format(pid))
        sprocess = None
    except Exception:
        import subprocess
        command = args.process_id_or_command
        print("Starting up command '{0}' and attaching to process"
              .format(command))
        sprocess = subprocess.Popen(command, shell=True)
        pid = sprocess.pid

    monitor(pid, probing_f=args.probing_f, logfile=args.log, plot=args.plot, duration=args.duration,
            interval=args.interval, include_children=args.include_children)

    if sprocess is not None:
        sprocess.kill()


def monitor(pid, probing_f=None, logfile=None, plot=None, duration=None, interval=None,
            include_children=False):

    # We import psutil here so that the module can be imported even if psutil
    # is not present (for example if accessing the version)
    import psutil

    pr = psutil.Process(pid)

    # Record start time
    start_time = time.time()

    if logfile:
        f = open(logfile, 'w')
        f.write("# {0:12s} {1:12s} {2:12s} {3:12s}\n".format(
            'Elapsed time'.center(12),
            'CPU (%)'.center(12),
            'Real (MB)'.center(12),
            'Virtual (MB)'.center(12))
        )
    csv_columns = ['TIME','CPU','REAL_MB','VIRTUAL_MB']

    logfile_csv = 'cpu_usage_' + probing_f + '.csv'

    if (os.path.isfile(logfile_csv) ):
        os.remove(logfile_csv)        

    log = {}
    log['times'] = []
    log['cpu'] = []
    log['mem_real'] = []
    log['mem_virtual'] = []

    try:

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

            # Get information for children
            if include_children:
                for child in all_children(pr):
                    try:
                        current_cpu += get_percent(child)
                        current_mem = get_memory(child)
                    except Exception:
                        continue
                    current_mem_real += current_mem.rss / 1024. ** 2
                    current_mem_virtual += current_mem.vms / 1024. ** 2

            if logfile:
                f.write("{0:12.3f} {1:12.3f} {2:12.3f} {3:12.3f}\n".format(
                    current_time - start_time,
                    current_cpu,
                    current_mem_real,
                    current_mem_virtual))
                f.flush()
                
            if probing_f:             

                dict_data = [{
                    'TIME': current_time - start_time,
                    'CPU': current_cpu,
                    'REAL_MB': current_mem_real, 
                    'VIRTUAL_MB':current_mem_virtual 
                    }]            
                
                WriteDictToCSV(logfile_csv,csv_columns,dict_data)                

            if interval is not None:
                time.sleep(interval)

            # If plotting, record the values
            if plot:
                log['times'].append(current_time - start_time)
                log['cpu'].append(current_cpu)
                log['mem_real'].append(current_mem_real)
                log['mem_virtual'].append(current_mem_virtual)

    except KeyboardInterrupt:  # pragma: no cover
        pass

    if logfile:
        f.close()

    if plot:

        import matplotlib.pyplot as plt

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)

        ax.plot(log['times'], log['cpu'], '-', lw=1, color='r')

        ax.set_ylabel('CPU (%)', color='r')
        ax.set_xlabel('time (s)')
        ax.set_ylim(0., max(log['cpu']) * 1.2)

        ax2 = ax.twinx()

        ax2.plot(log['times'], log['mem_real'], '-', lw=1, color='b')
        ax2.set_ylim(0., max(log['mem_real']) * 1.2)

        ax2.set_ylabel('Real Memory fer (MB)', color='b')

        ax.grid()

        fig.savefig(plot)

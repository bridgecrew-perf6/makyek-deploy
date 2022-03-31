#!/usr/bin/python3
import argparse
import os
import shutil
import subprocess
import sys
from string import Template

stage2_wrapper_template = Template('''
set -eu

ulimit -t $cpu_time_sec
ulimit -p $processes
ulimit -m $memory_KB
ulimit -n $fds

exec "$$@"
''')

def generate_stage2_wrapper(cpu_time_sec=120, processes=1, memory_KB=524288, fds=3):
    return stage2_wrapper_template.substitute(locals())

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--use-desktop', action='store_true')
    parser.add_argument('--use-logon', action='store_true')
    parser.add_argument('--active-process', type=int, default=1)
    parser.add_argument('--memory', type=int, default=524288)
    parser.add_argument('--affinity', type=int) # not implemented
    parser.add_argument('cmd', nargs='+')
    args = parser.parse_args()

    f = open("/tmp/sandbox.log", "a") # for debugging only
    f.write("args %s\n" % args)

    # write stage 2 wrapper
    with open("wrapper.sh", "w") as wrapper_fd:
        wrapper_fd.write(generate_stage2_wrapper(processes=args.active_process, memory_KB=args.memory))
    
    # copy stage 2 wrapper runtime
    shutil.copy("/bin/busybox", "busybox")

    try:
        # ls_ret = subprocess.Popen("ls -lh", stdout=subprocess.PIPE, shell=True).communicate()
        # f.write("ls %s\n" % str(ls_ret))

        # note: fakechroot is not a security boundary. It is only used to verify if static linking is working.
        # cmd = ["/usr/bin/fakechroot", "chroot", os.getcwd()]
        cmd = ["/usr/sbin/chroot", "--userspec=nobody:nogroup", "--", os.getcwd()] # chroot + drop privilege
        cmd.extend(["./busybox", "ash", "--", "./wrapper.sh"]) # stage 2 wrapper
        cmd.extend(args.cmd), # actual program
        f.write("cmd %s\n" % cmd)

        p = subprocess.Popen(
            cmd,
            stdin=sys.stdin,
            stdout=sys.stdout,
            stderr=sys.stderr,
        )
        ret = p.wait()
        p.communicate() # flush pipes

        f.write("ret %d\n" % ret)
        sys.exit(ret)

    except Exception as ex:
        f.write("err %s\n" % ex)

    finally:
        f.close()
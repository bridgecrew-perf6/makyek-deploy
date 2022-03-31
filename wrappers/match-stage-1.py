#!/usr/bin/python3
import argparse
import os
import psutil
import shutil
import subprocess
import sys
from string import Template

NICE_SELF = -19
NICE_SUBPROCESS = 20

stage2_wrapper_template = Template('''
ulimit -H -t $cpu_time_sec
ulimit -H -p $processes
ulimit -H -m $memory_KB
ulimit -H -n $fds

exec "$@"
''')

def generate_stage2_wrapper(cpu_time_sec=120, processes=1, memory_KB=524288, fds=1):
    return stage2_wrapper_template.substitute(locals())

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--use-desktop', action='store_true')
    parser.add_argument('--use-logon', action='store_true')
    parser.add_argument('--active-process', type=int)
    parser.add_argument('--memory', type=int)
    parser.add_argument('--affinity', type=int)
    parser.add_argument('cmd', nargs='+')
    args = parser.parse_args()

    # set self nice
    psutil.Process(os.getpid()).set_nice(NICE_SELF)

    f = open("/tmp/sandbox.log", "a")
    f.write("args %s\n" % args)

    # write stage 2 wrapper
    with open("wrapper.sh", "w") as f:
        f.write(generate_stage2_wrapper())
    
    # copy stage 2 wrapper runtime
    shutil.copy("/usr/bin/busybox", "busybox")

    try:
        # ls_ret = subprocess.Popen("ls -lh", stdout=subprocess.PIPE, shell=True).communicate()
        # f.write("ls %s\n" % str(ls_ret))

        # generate stage 2 wrapper which must be an ash shell script


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
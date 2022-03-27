#!/usr/bin/python3
import argparse
import os
import subprocess
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--use-desktop', action='store_true')
    parser.add_argument('--use-logon', action='store_true')
    parser.add_argument('--active-process', type=int)
    parser.add_argument('--memory', type=int)
    parser.add_argument('--affinity', type=int)
    parser.add_argument('cmd', nargs='+')
    args = parser.parse_args()

    f = open("/tmp/sandbox.log", "a")
    f.write("args %s\n" % args)

    try:
        # ls_ret = subprocess.Popen("ls -lh", stdout=subprocess.PIPE, shell=True).communicate()
        # f.write("ls %s\n" % str(ls_ret))

        cmd = ["/usr/bin/fakechroot", "chroot", os.getcwd()]
        cmd.extend(args.cmd),
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
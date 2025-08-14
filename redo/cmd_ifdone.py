"""redo-ifdone: return non-zero when target(s) need rebuilding"""
from __future__ import print_function
import sys, os
from . import deps, env, logs, state

cache = {}


def is_checked(f):
    return cache.get(f.id, 0)


def set_checked(f):
    cache[f.id] = 1


def log_override(name):
    pass


def main():
    if len(sys.argv[1:]) == 0:
        sys.stderr.write('%s: arguments expected.\n' % sys.argv[0])
        sys.exit(1)
    targets = sys.argv[1:]
    state.init(targets)
    logs.setup(
        tty=sys.stderr, parent_logs=env.v.LOG,
        pretty=env.v.PRETTY, color=env.v.COLOR)

    for t in targets:
        f = state.File(name=t)
        if f.is_target():
            if deps.isdirty(f,
                            depth='',
                            max_changed=env.v.RUNID,
                            already_checked=[],
                            is_checked=is_checked,
                            set_checked=set_checked,
                            log_override=log_override):
                sys.exit(1)
        elif os.path.exists(t):
            pass
        else:
            sys.exit(1)


if __name__ == '__main__':
    main()

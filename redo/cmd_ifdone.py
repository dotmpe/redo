"""redo-ifdone: return non-zero when target(s) need rebuilding

Normally redo works recursively and effectively creates a single depedency tree.
That tree needs to be rechecked on each run for upstream updates. This is not
practical if the build scripts cover separate lifecycle phases or when
otherwise distinct, parallel states are required. E.g. upstream projects,
platform and other environment aspects can logically be fully integrated
into a project build, but that involves significant effort and is an unrealistic
excercise. The platform is already layered, and we can assume that updates
affect its functionality.

However exact tracking of prerequisites is a core Redo feature and main
consideration during recipe authoring. Bernstein's build system focusses on
creating file targets, but the effective toolset works very well with 'virtual'
targets that have no file presence of their own but still leave a build state or
stamp and dependencies.

When project builds or more complex systems do their configuration and
provisioning, the build environment logically changes. Hence for such targets
recursion makes no sense as when the prerequisites are in an uncertain state
then the parent will need to restart once the upstream state has been satisfied
and determined. And that is not how Redo normally works.

Redo-ifdone does not register the given targets as dependencies, but acts like
they are prerequisites. There is no logical way the Redo can recover from that,
so running this recipe requires for the correct sequence of targets to be input
(at once or subsequently) or else the build always fails. Those prerequisites
targets are otherwise separate from the recipe, and so tracking of that state is
left to the user or calling system as well. You could say they are logically
exclusive, and have separate meanings. In practice it allows to write build
scripts for systems with distinct states, but where upstream changes still are
detected across separate states. They also do not invalidate the current target
per se, but do prevent any attempt to try re-evaluting the current recipe
without re-evaluting upstream targets first.

TODO: more helpful output in err log
- possibly start using exit codes to signal build state
  (missing/OTD/unknown/fail)

XXX: this should afaics check entire dep tree for given target, its just a
derivation on existing redo-ood command.

Ideas for enhancements:

redo-ifdone -n nostat?
redo-ifdone -s use exit status tables
redo-ifdone -q quiet err

"""
from __future__ import print_function
import sys, os
from . import deps, env, logs, state
from .logs import err

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
        if f.is_source():
            pass # source is OK (present with matching stamp)
        elif f.is_target():
            if deps.isdirty(f,
                            depth='',
                            max_changed=env.v.RUNID,
                            already_checked=[],
                            is_checked=is_checked,
                            set_checked=set_checked,
                            log_override=log_override):
                err('rebuild needed of %s' % t)
                sys.exit(1)
        #elif os.path.exists(t):
        #    pass
        else:
            err('unknown prerequisite %s' % t)
            sys.exit(1)


if __name__ == '__main__':
    main()

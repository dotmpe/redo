. ${scr_pre:?}/common_env.sh

{
  ./do -j10 clean &&
  ./do -j10 build &&
  sudo DESTDIR= PREFIX=/usr/local ./do -j10 install &&
  \builtin command -v redo >/dev/null 2>&1
} ||
  _failerr "Failed to build+install redo (E$?)"

sudo chown -R "$(id -u):$(id -g)" . .do_built

BRANCH_NAME=${GITHUB_REF##*/}

if [[ $BRANCH_NAME == test ]]; then
  ./do -j10 clean &&
  ./do -j10 test ||
    _failerr "Failed to complete full redo test (E$?)"
fi

# Id: ci_run                                     vim:set ft=bash sw=2 sts=2 et:

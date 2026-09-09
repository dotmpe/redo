#
# common_env.sh
# Copyright (C) 2026 hari <hari@t470p>
#
# Distributed under terms of the MIT license.
#
set -eETuo pipefail
shopt -s nullglob failglob extdebug
IFS=$' \t\n'

_failerr() {
  stat=$?
  echo "$*" >&2
  exit $stat
}

# Id: common_setup                               vim:set ft=bash sw=2 sts=2 et:

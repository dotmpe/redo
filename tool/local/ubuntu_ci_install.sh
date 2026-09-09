. ${scr_pre:?}/common_env.sh

sudo apt-get update -q &&

# TODO: no shellcheck scans done
sudo apt-get install -qy shellcheck fakechroot debootstrap ||
  _failerr "Failed to provision apt packages (E$?)"

# FIXME: tried adding apt/pip mkdocs/markdown to CI but those were not picked up
# pip install mkdocs mkdocs-exclude markdown ||
#   _failerr "Failed to provision pip packages (E$?)"

# { curl -s https://bashunit.com/install.sh | bash; } &&
# sudo mv -v lib/bashunit /usr/local/bin/ &&
# command -v bashunit >/dev/null 2>&1 ||
#   _failerr "Failed to provision bashunit (E$?)"

# Id: ubuntu_ci_install                          vim:set ft=bash sw=2 sts=2 et:

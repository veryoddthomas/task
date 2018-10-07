pylint() {
    python3 /usr/bin/pylint "$@"
}
pycodestyle() {
    python3 -m pycodestyle "$@"
}
export -f pylint
export -f pycodestyle

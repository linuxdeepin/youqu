_my_script_completion() {
    local cur prev opts
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    case "$prev" in
        "youqu")
            COMPREPLY=($(compgen -W "manage.py" -- "$cur"))
            ;;
        "manage.py")
            COMPREPLY=($(compgen -W "run remote playbook pmsctl csvctl startapp git" -- "$cur"))
            ;;
        "run")
            COMPREPLY=($(compgen -W "-a --app -k --keyword -t --tags --slaves" -- "$cur"))
            ;;
        "remote")
            COMPREPLY=($(compgen -W "-c --clients -s --send_code -e -y -a --app -k --keyword -t --tags --slaves" -- "$cur"))
            ;;
        *)
            ;;
    esac
}

complete -F _my_script_completion youqu
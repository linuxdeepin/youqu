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
        *)
            COMPREPLY=($(compgen -o default -- "$cur"))
          ;;
    esac
}

complete -F _my_script_completion youqu
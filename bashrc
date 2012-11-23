PS1='\[\033[35m\]\t\[\033[m\] - \[\e[36m\]saipanno\[\e[m\]@\[\033[32m\]\h\[\033[m\] \[\e[34m\]\w\[\e[m\] \[\e[32m\]\$ \[\e[m\]'

alias psf='ps f'

function s {
    TMUX=`whereis tmux | awk '{ print $2 }'`
    $TMUX has-session -t default
    if [ $? = 1 ]; then
        $TMUX new-session -s default
    else
        $TMUX attach-session -d -t default
    fi 
}
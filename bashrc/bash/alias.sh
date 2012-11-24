

function s {
    TMUX=`whereis tmux | awk '{ print $2 }'`
    $TMUX has-session -t default
    if [ $? = 1 ]; then
        $TMUX new-session -s default
    else
    $TMUX attach-session -d -t default
fi 
}


alias l='ls -la'
alias ll='ls -l'
alias psf='ps f'
alias lsa='ls -lah'

alias p='cd ~/Projects'
alias d='cd ~/Downloads'

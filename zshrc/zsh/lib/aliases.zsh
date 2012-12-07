# Basic directory operations
alias ...='cd ../..'

#alias g='grep -in'

# Show history
alias history='fc -l 1'

# List direcory contents
alias lsa='ls -lah'
alias l='ls -la'
alias ll='ls -l'

alias p='cd ~/Projects'
alias d='cd ~/Downloads'

alias psf='ps f'
alias gp='git pull'

[ -f /usr/local/bin/mvim ] && alias vim='mvim -v'

function s {
    TMUX=`whereis tmux | awk '{ print $2 }'`
    $TMUX has-session -t default
    if [ $? = 1 ]; then
        $TMUX new-session -s default
    else
        $TMUX attach-session -d -t default
    fi
}

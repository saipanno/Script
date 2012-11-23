# If not running interactively, don't do anything
[ -z "$PS1" ] && return

# append to the history file, don't overwrite it
shopt -s histappend
# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# If this is an xterm set the title to user@host:dir
case "$TERM" in
xterm*|rxvt*)
    PS1="\[\e]0;${debian_chroot:+($debian_chroot)}saipanno@\h: \w\a\]$PS1"
    ;;
*)
    ;;
esac

function s {
    TMUX=`whereis tmux | awk '{ print $2 }'`
    $TMUX has-session -t default
    if [ $? = 1 ]; then
        $TMUX new-session -s default
    else
        $TMUX attach-session -d -t default
    fi 
}

function git_prompt_info {
      ref=$(git symbolic-ref HEAD 2> /dev/null) || return
      echo "on ${ref#refs/heads/} $(parse_git_dirty)"
}
# Checks if working tree is dirty
function parse_git_dirty {
	if [[ -n $(git status -s 2> /dev/null) ]]; then
		echo '!'
  	else
		echo '√'
  	fi
}

# Add git and svn branch names
PS1='\[\033[35m\]\t\[\033[m\] - \[\e[36m\]saipanno\[\e[m\] at \[\033[32m\]\h\[\033[m\] in \[\e[34m\]\w\[\e[m\] $(git_prompt_info)\n\[\e[32m\]\$\[\e[m\] '

# Alias definitions.
alias l='ls -la'
alias ll='ls -l'
alias psf='ps f'
alias lsa='ls -lah'

alias p='cd ~/Projects'
alias d='cd ~/Downloads'

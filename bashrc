# If not running interactively, don't do anything
[ -z "$PS1" ] && return

# append to the history file, don't overwrite it
shopt -s histappend
# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

#PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
PS1='\[\033[01;31m\]\w\[\033[00m\]\n${debian_chroot:+($debian_chroot)}\[\033[01;34m\]\u\[\033[01;32m\]@\[\033[01;34m\]\h\[\033[00m\]\$ '

# If this is an xterm set the title to user@host:dir
case "$TERM" in
xterm*|rxvt*)
    PS1="\[\e]0;${debian_chroot:+($debian_chroot)}saipanno@\h: \w\a\]$PS1"
    ;;
*)
    ;;
esac

# dircolors... make sure that we have a color terminal, dircolors exists, and ls supports it.
if $TERM_IS_COLOR && ( dircolors --help && ls --color ) &> /dev/null; then
  # For some reason, the unixs machines need me to use $HOME instead of ~
  # List files from highest priority to lowest. As soon as the loop finds one that works, it will exit.
  for POSSIBLE_DIR_COLORS in "$HOME/.dir_colors" "/etc/DIR_COLORS"; do
    [[ -f "$POSSIBLE_DIR_COLORS" ]] && [[ -r "$POSSIBLE_DIR_COLORS" ]] && eval `dircolors -b "$POSSIBLE_DIR_COLORS"` && break
  done

  alias ls="ls --color=auto"
  alias ll="ls --color=auto -l"
  alias grep='grep --color=auto'
  alias fgrep='fgrep --color=auto'
  alias egrep='egrep --color=auto'
else
  # No color, so put a slash at the end of directory names, etc. to differentiate.
  alias ls="ls -F"
  alias ll="ls -lF"
fi

# Alias definitions.
if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

parse_git_branch ()
{
  git branch 2> /dev/null | grep '*' | sed 's#*\ \(.*\)#(git::\1)#'
}

export EDITOR="$vim"
export GIT_EDITOR="$vim"

# Add git and svn branch names
export PS1="$PS1\$(parse_git_branch) "














#PS1='\[\033[35m\]\t\[\033[m\] - \[\e[36m\]saipanno\[\e[m\]@\[\033[32m\]\h\[\033[m\] \[\e[34m\]\w\[\e[m\] \[\e[32m\]\$ \[\e[m\]'

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


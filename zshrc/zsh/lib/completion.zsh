setopt auto_menu # show completion menu on succesive tab press
setopt always_to_end
setopt complete_in_word

unsetopt flowcontrol
unsetopt menu_complete # do not autoselect the first completion entry

WORDCHARS=''

zmodload -i zsh/complist

## case-insensitive (all),partial-word and then substring completion
if [ "x$CASE_SENSITIVE" = "xtrue" ]; then
    zstyle ':completion:*' matcher-list 'r:|[._-]=* r:|=*' 'l:|=* r:|=*'
    unset CASE_SENSITIVE
else
    zstyle ':completion:*' matcher-list 'm:{a-zA-Z}={A-Za-z}' 'r:|[._-]=* r:|=*' 'l:|=* r:|=*'
fi

zstyle ':completion:*' list-colors ''

zstyle ':completion:*:*:*:*:*' menu select
zstyle ':completion:*:*:kill:*:processes' list-colors '=(#b) #([0-9]#) ([0-9a-z-]#)*=01;34=0=01'

# disable named-directories autocompletion
zstyle ':completion:*:cd:*' tag-order local-directories directory-stack path-directories
cdpath=(.)

# Use caching so that commands like apt and dpkg complete are useable
zstyle ':completion::complete:*' use-cache 1
zstyle ':completion::complete:*' cache-path ~/.oh-my-zsh/cache/

# Use ~/.ssh/config hostname completion
[ -r ~/.ssh/config ] && _ssh_hosts=(`awk '/^Host/ { print $2 }' $HOME/.ssh/config`) || _ssh_hosts=()
zstyle ':completion:*:hosts' hosts $_ssh_hosts[@]

# Don't complete uninteresting users
_hide_users=(`awk 'BEGIN {FS=":"} /nologin|halt|shutdown|sync/ { print $1 }' /etc/passwd`) || _hide_users=()
zstyle ':completion:*:*:*:users' ignored-patterns $_hide_users[@]

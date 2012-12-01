setopt auto_menu         # show completion menu on succesive tab press
setopt complete_in_word
setopt always_to_end
# setopt glob bareglobqual nullglob rcexpandparam extendedglob unset

unsetopt flowcontrol
unsetopt menu_complete   # do not autoselect the first completion entry
unsetopt markdirs globsubst shwordsplit shglob ksharrays cshnullglob
unsetopt allexport aliases errexit octalzeroes

WORDCHARS=''

zmodload -i zsh/complist

# Use ~/.ssh/config hostname completion
[ -r ~/.ssh/config ] && _ssh_hosts=(`awk '/^Host/ { print $2 }' $HOME/.ssh/config`) || _ssh_hosts=()
zstyle ':completion:*:hosts' hosts $_ssh_hosts[@]

# Don't complete uninteresting users
_hide_users=(`awk 'BEGIN {FS=":"} /nologin|halt|shutdown|sync/ { print $1 }' /etc/passwd`) || _hide_users=()
zstyle ':completion:*:*:*:users' ignored-patterns $_hide_users[@]

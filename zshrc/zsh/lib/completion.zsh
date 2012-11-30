unsetopt menu_complete   # do not autoselect the first completion entry
unsetopt flowcontrol
setopt auto_menu         # show completion menu on succesive tab press
#setopt complete_in_word
#setopt always_to_end

WORDCHARS=''

zmodload -i zsh/complist

# use ~/.ssh/config hostname completion
[ -r ~/.ssh/config ] && _ssh_hosts=(`awk 'BEGIN {ORS=" "} /^Host/ { print $2 }' $HOME/.ssh/config`) || _ssh_hosts=()
hosts=(
  "$_ssh_hosts[@]"
  localhost
)
zstyle ':completion:*:hosts' hosts $hosts

# Don't complete uninteresting users
zstyle ':completion:*:*:*:users' ignored-patterns \
        adm amanda apache avahi beaglidx bin cacti canna clamav daemon \
        dbus distcache dovecot fax ftp games gdm gkrellmd gopher \
        hacluster haldaemon halt hsqldb ident junkbust ldap lp mail \
        mailman mailnull mldonkey mysql nagios \
        named netdump news nfsnobody nobody nscd ntp nut nx openvpn \
        operator pcap postfix postgres privoxy pulse pvm quagga radvd \
        rpc rpcuser rpm shutdown squid sshd sync uucp vcsa xfs

zstyle ':completion:*:*:(ssh|scp):*:*' hosts `sed 's/^\([^ ,]*\).*$/\1/' ~/.ssh/known_hosts`

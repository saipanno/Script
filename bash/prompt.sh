#!/bin/bash


c_red='\e[31m'
c_blue='\e[36m'
c_green='\e[32m'
c_yellow='\e[1;33m'
c_clear='\e[0m'

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
PS1='\['$c_green'\]saipanno\['$c_clear'\] at \['$c_blue'\]\h\['$c_clear'\] in \['$c_yellow'\]\w\['$c_clear'\] $(git_prompt_info)\n\$ '
#export PS1

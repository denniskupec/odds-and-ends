# echo your external IP (version 4) address
# --no-check-certificate might not be required for you

alias ip="echo -e '$(tput bold)IP Address: $(tput sgr0)$(wget --no-check-certificate --no-dns-cache -4qO - https://doma$

#!/bin/bash

# Генерируем SSH хостовые ключи если их нет
if [ ! -f /etc/ssh/ssh_host_rsa_key ]; then
    ssh-keygen -A
fi

# Настройка ForceCommand для пользователя pgbackresthost
echo "Match User pgbackresthost
    ForceCommand sudo -u pgbackresthost /usr/bin/pgbackrest $SSH_ORIGINAL_COMMAND
    AllowTcpForwarding no
    PermitTTY no
    X11Forwarding no" >> /etc/ssh/sshd_config

# Запуск SSH сервера
exec /usr/sbin/sshd -D
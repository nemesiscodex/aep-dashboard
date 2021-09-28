#!/bin/sh

# Ensure log file exists
touch /app/crontab.log

# Ensure permission on the command
chmod a+x /app/updatecollected.sh

# Create crontab file
echo "" > /etc/crontab

# Add environment variables to crontab
echo "DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}" >> /etc/crontab
echo "DJANGO_DEBUG=${DJANGO_DEBUG}" >> /etc/crontab
echo "DATABASE_HOST=${DATABASE_HOST}" >> /etc/crontab
echo "DATABASE_PORT=${DATABASE_PORT}" >> /etc/crontab
echo "DATABASE_NAME=${DATABASE_NAME}" >> /etc/crontab
echo "DATABASE_USER=${DATABASE_USER}" >> /etc/crontab
echo "DATABASE_PASSWORD=${DATABASE_PASSWORD}" >> /etc/crontab

# Added a cronjob
# with log file
# echo "* * * * * /app/updatecollected.sh >> /app/crontab.log 2>&1" >> /etc/crontab
# without log file
echo "* * * * * /app/updatecollected.sh > /dev/null 2>&1" >> /etc/crontab

# Registering the new crontab
crontab /etc/crontab

# Starting the cron
/usr/sbin/service cron start

# Displaying logs
# Useful when executing docker-compose logs mycron
tail -f /app/crontab.log

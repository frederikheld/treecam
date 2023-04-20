FROM ubuntu:22.04

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
      cron \
      curl

WORKDIR /app

COPY transfer.sh .
COPY debug.sh .
RUN chmod +x transfer.sh
RUN chmod +x debug.sh

RUN ls -la /app

# Set up cronjob:
COPY cronjobs /etc/cron.d/cronjobs
RUN chmod 0644 /etc/cron.d/cronjobs
RUN crontab /etc/cron.d/cronjobs
RUN touch /var/log/cron.log

# make env variables (that were passed to docker run command) available in cron jobs
# then start cron service and logging:
CMD [ "/bin/bash", "-c", "env >> /etc/environment && service cron start && tail -f /var/log/cron.log"]

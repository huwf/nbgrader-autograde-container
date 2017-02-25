FROM jupyterhub/systemuser

# This bit installs the postgres client library
RUN apt-get update && apt-get install -y libpq-dev gcc
# need gcc to compile psycopg2
RUN python -m pip install psycopg2
RUN apt-get autoremove -y gcc

RUN python -m pip install nbgrader
RUN rm -rf /home/jovyan
RUN useradd -ms /bin/bash instructor


WORKDIR /home/instructor

RUN mkdir -p /home/instructor/submitted
RUN mkdir /home/instructor/autograded

RUN mkdir -p /home/instructor/source/mongodb
RUN mkdir -p /home/instructor/source/stats
RUN mkdir -p /home/instructor/source/visualisation

# Folders for mounting
RUN mkdir -p /home/instructor/user-submission
RUN mkdir -p /home/instructor/autograded-docker

RUN touch .nbgrader.log
RUN mkdir .jupyter

ADD autograde.sh /autograde
RUN chmod 755 /autograde

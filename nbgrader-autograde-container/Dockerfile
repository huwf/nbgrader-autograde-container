FROM jupyterhub/systemuser

RUN python -m pip install nbgrader
RUN rm -rf /home/jovyan
RUN useradd -ms /bin/bash instructor

RUN nbgrader extension install --symlink --debug
RUN nbgrader extension activate

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

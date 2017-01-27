# NBGrader Autograding Container

This image allows `nbgrader autograde` to run, offering some isolation from the main filesystem.  It reduces access to the `autograde/` and `submitted/` directories, and creates a fake submitted directory.  

It assumes that there is already a directory for the user in the `autograded` directory, so that needs to be created prior to running it.  Expected usage is as follows:

	path = os.path.join(NBGRADER_DIR, 'autograded', username, assignment_name
	if not os.path.exists(path):
		os.makedirs(path)
	
    listy = [
        'docker', 'run', '-it', '--rm',
        '-v', '%s/submitted/%s:/home/instructor/user-submission/%s' 
        		% (NBGRADER_DIR, username, username),
        '-v', '%s/autograded/%s:/home/instructor/autograded-docker/%s' 
        		% (NBGRADER_DIR, username, username),
        '-v', '%s/gradebook.db:/home/instructor/gradebook.db' % NBGRADER_DIR,
        '-v', '%s/nbgrader_config.py:/home/instructor/nbgrader_config.py' % NBGRADER_DIR,
        '-v', '/home/instructor/students.csv:/home/instructor/students.csv',# % NBGRADER_DIR,
        'nbgrader-autograde-container',
        '/autograde', username, assignment_name, str(instructor_id)]
    run_cmd(listy, 'huw')

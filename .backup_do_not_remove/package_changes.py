#!/usr/bin/python2

import sys, getopt, pwd, datetime, shutil, grp, hashlib, os, subprocess


assignment = ''
username = "UNKNOWN"
filename = ""

def create_tarball():
	global assignment 
	global username 
	global filename 
	os.system("mv *.tgz ../assignment-history");
	print("You may see an error saying the scripts can not stat *.tgz. This is fine. Don't worry");
	print("Searching for new files:");
	new_files_result = subprocess.check_output("diff -pqr ../linux-5.8/ ../.backup_do_not_remove/ 2>/dev/null|grep -v \"*\.o\.cmd\" | grep -v \"DocBook\" |grep -v \"vmlinux\" | grep -v \"gitignore\" | grep -v \"scripts\" | grep -v \"builtin-policy\" |grep Only |awk -e \'{print $3$4}\'", shell=True);
	print ( new_files_result )
	if new_files_result:
		print ( "Found "+str(len(new_files_result.split('\n'))-1)+":" )
		new_files_result = new_files_result.replace(':','/');
		print ( new_files_result )

	print("Searching for modified files:");
	modified_files_result = subprocess.check_output("diff -pqr ../linux-5.8/ ../.backup_do_not_remove/ 2>/dev/null|grep differ |awk -e \'{print $2}\'", shell=True);
	if modified_files_result:
		print ( "Found "+str(len(modified_files_result.split('\n'))-1)+":" )
		print ( modified_files_result )

	if ( ( len( new_files_result.split('\n'))-1 == 0 ) and 
           ( len( modified_files_result.split('\n'))-1 == 0 ) ):
		print("No new or modified files found!")
		sys.exit(2)

	print("Creating the tarball to submit.");
	new_files_result = new_files_result.replace('\n',' ').replace('\r','').replace(':','/');
	modified_files_result = modified_files_result.replace('\n',' ').replace('\r','');

	submit_time = str(datetime.datetime.now()).replace(' ','-').replace(':','_');
	file_name = username + "_" + assignment + "_" + submit_time+".tgz"

	tar_command = "tar czf "+ file_name + " "+ new_files_result + modified_files_result;

	os.system(tar_command);

	print ( "File "+file_name + " is ready to upload to Canvas." )

def main(argv):

	global assignment 
	global username 
	global filename 

	try:
		opts, args = getopt.getopt(argv, "a:u:", ["assignment=", "user="])
		if len(opts) == 0:
			print ( 'package_changes.py --assignment <assignment> --user <your UTA netid>')
			sys.exit(2)

	except getopt.GetoptError:
		print ( 'package_changes.py --assignment <assignment> --user <your UTA netid>')
		sys.exit(2)

	for opt, arg in opts:
		if opt in ('-a', '--assignment'):
			assignment = arg
		elif opt in ('-u', '--user'):
			username = arg

	if assignment == '':
		print ( 'Invalid assignment number! Try again.' )
		print ( 'package_changes.py --assignment <assignment> --user <your UTA netid>')
		sys.exit(2)

	if username == "UNKNOWN":
		print ( 'Invalid user name! Try again.' )
		print ( 'package_changes.py --assignment <assignment> --user <your UTA netid>' )
		sys.exit(2)

	create_tarball()

if __name__ == "__main__":
	main(sys.argv[1:])

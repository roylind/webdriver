import psutil
from loguru import logger


def kill_only_child_proc(parent_proc, name_child=None, is_cmd_child=None):
	for child in parent_proc.children(recursive=True):
		try:
			if name_child is not None:
				if name_child != child.name():
					continue
			if is_cmd_child is not None:
				if is_cmd_child not in " ".join(child.cmdline()[1:]):
					continue
			kill_proc_all_child(child)
		except (OSError, psutil.NoSuchProcess) as E:
			logger.exception(E)


def kill_proc_conditions(name_child, is_cmd_child=None):
	process = list(psutil.process_iter())
	print(len(process))
		# try:
		# 	if name_child is not None:
		# 		if name_child != proc.name():
		# 			continue
		# 	if is_cmd_child is not None:
		# 		if is_cmd_child not in " ".join(proc.cmdline()[1:]):
		# 			continue
		# 	kill_proc_all_child(proc)
		# except OSError:
		# 	pass
		# except psutil.NoSuchProcess:
		# 	pass


def kill_proc_all_child(proc):
	try:
		for child in proc.children(recursive=True):
			try:
				child.kill()
			except (OSError, psutil.NoSuchProcess) as E:
				logger.exception(E)
		proc.kill()
	except (OSError, psutil.NoSuchProcess) as E:
		logger.exception(E)

# def kill_proc_all_child(proc):
# 	try:
# 		for child in proc.children(recursive=True):
# 			try:
# 				child.kill()
# 			except OSError:
# 				pass
# 			except psutil.NoSuchProcess:
# 				pass
# 		proc.kill()
# 	except OSError:
# 		pass
# 	except psutil.NoSuchProcess:
# 		pass


# def find_procs_by_path_and_iscmd(path, is_cmd):
#
#
# 	result_list_proc = []
# 	for proc in psutil.process_iter():
# 		name, exe, cmdline = "", "", []
# 		try:
# 			name = proc.name()
# 			cmdline = proc.cmdline()
# 			exe = proc.exe()
# 		except (psutil.AccessDenied, psutil.ZombieProcess):
# 			pass
# 		except psutil.NoSuchProcess:
# 			continue
# 		if (exe == path) and (is_cmd in " ".join(cmdline)):
# 			result_list_proc.append(proc)
#
# 	return(result_list_proc)
#
#
# def kill_child_proc(proc):
# 	try:
# 		for child in psutil.Process(pid = proc.pid).children(recursive=True):
# 			try:
# 				psutil.Process(pid = child.pid).kill()
# 			except Exception as E:
# 				pass
# 		proc.kill()
# 	except:
# 		pass

# import time
if __name__ == "__main__":
	kill_proc_conditions("firefox.exe")

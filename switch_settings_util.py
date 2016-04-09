import sublime, sublime_plugin

def reboot():
	import os, subprocess

	opened_file = sublime.active_window().active_view().file_name()
	if opened_file is None:
		opened_file = os.path.join(sublime.packages_path(), 'User', 'Preferences.sublime-settings')

	if sublime.platform() == 'linux':
		subl_path = sublime.executable_path().replace(' ','\ ')
		command = ' '.join([
			subl_path, '--command', 'exit',
			'&&', 'sleep', '0.5',
			'&&', subl_path, opened_file.replace(' ','\ '),
			'&',  'kill', '-9', '$$'
		])

	elif sublime.platform() == 'osx':
		subl_path = sublime.executable_path().replace(' ','\ ')
		subl_path = subl_path[:subl_path.rfind('.app/') + 5] + '/Contents/SharedSupport/bin/subl'
		command = ' '.join([
			subl_path, '--command', 'exit',
			'&&', 'sleep', '0.5',
			'&&', subl_path, opened_file.replace(' ','\ '),
			'&',  'kill', '-9', '$$'
		])

	elif sublime.platform() == 'windows':
		subl_path = sublime.executable_path()
		subl_path = '"' + subl_path[:subl_path.rfind('\\') + 1] + 'subl' + '"'
		command = ' '.join([
			subl_path, '--command', 'exit',
			'&&', 'ping', '-n', '1', 'localhost',
			'&&', subl_path, '"' + opened_file.replace + '"'
		])
	
	subprocess.Popen(command, shell=True)
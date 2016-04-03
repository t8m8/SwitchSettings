import sublime, sublime_plugin

def reboot():
	import os, subprocess

	subl_path = sublime.executable_path().replace(' ','\ ')
	if sublime.platform() == 'osx':
		subl_path = subl_path[:subl_path.rfind('.app/') + 5] + '/Contents/SharedSupport/bin/subl'
	
	opened_file = sublime.active_window().active_view().file_name()
	if opened_file is None:
		opened_file = os.path.join(sublime.packages_path(), 'User', 'Preferences.sublime-settings')

	command = ' '.join([
		subl_path, '--command', 'exit',
		'&&', 'sleep', '0.5',
		'&&', subl_path, opened_file.replace(' ','\ '),
		'&',  'kill', '-9', '$$'
	])
	subprocess.Popen(command, shell=True)
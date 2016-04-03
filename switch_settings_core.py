import sublime, sublime_plugin

class SettingsWrapper():

	SETTINGS_FILE_NAME = 'SwitchSettings.sublime-settings'

	SS_CURRENT_SETTINGS_NAME = 'current_settings_name'
	SS_SETTINGS_NAMES = 'settings_names'
	SS_SETTINGS_CONTENTS = 'settings_contents'
	
	def __init__(self):
		self._buf = None
		self.settings = sublime.load_settings(SettingsWrapper.SETTINGS_FILE_NAME)
		self.settings.add_on_change(SettingsWrapper.SS_CURRENT_SETTINGS_NAME, self.on_change)

	def __save(self):  
		import os
		if self._buf is None: return False

		preferences = os.path.join(sublime.packages_path(), 'User', 'Preferences.sublime-settings')
		with open(preferences, mode='r') as f:
			preferences_settings = sublime.decode_value(f.read())

		contents = self.get_settings_contents()
		contents[self._buf] = preferences_settings
		self.settings.set(SettingsWrapper.SS_SETTINGS_CONTENTS, contents)

		self._buf = None
		return True

	def __overwrite(self):
		import os
		cur_name = self.get_current_settings()
		contents = self.get_settings_contents()
		current_content = contents[cur_name] 
		
		preferences = os.path.join(sublime.packages_path(), 'User', 'Preferences.sublime-settings')
		with open(preferences, mode='w') as f:
			f.write(sublime.encode_value(current_content, True))

		return True

	def on_change(self):
		from . import switch_settings_util as ss_util
		if self.__save() and self.__overwrite():
			self.save_ss_settings()
			ss_util.reboot()

	def save_ss_settings(self):
		sublime.save_settings(SettingsWrapper.SETTINGS_FILE_NAME)

	def set_buffer(self, buf):
		self._buf = buf



	def get_current_settings(self):
		return self.settings.get(SettingsWrapper.SS_CURRENT_SETTINGS_NAME)

	def set_current_settings(self, name):
		self.settings.set(SettingsWrapper.SS_CURRENT_SETTINGS_NAME, name)



	def get_settings(self):
		return self.settings.get(SettingsWrapper.SS_SETTINGS_NAMES)

	def add_settings(self, name):
		names = self.get_settings()
		names.append(name)
		self.settings.set(SettingsWrapper.SS_SETTINGS_NAMES, names);

	def remove_settings(self, name):
		names = self.get_settings()
		names.remove(name)
		self.settings.set(SettingsWrapper.SS_SETTINGS_NAMES, names)



	def get_settings_contents(self):
		return self.settings.get(SettingsWrapper.SS_SETTINGS_CONTENTS)

	def add_settings_content(self, name, item):
		contents = self.get_settings_contents()
		contents[name] = item
		self.settings.set(SettingsWrapper.SS_SETTINGS_CONTENTS, contents)

	def pop_settings_content(self, name):
		contents = self.get_settings_contents()
		tmp = contents.pop(name)
		self.settings.set(SettingsWrapper.SS_SETTINGS_CONTENTS, contents)
		return tmp






		
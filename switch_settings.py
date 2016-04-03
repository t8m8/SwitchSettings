import sublime, sublime_plugin

settings = None

def plugin_loaded():
	from . import switch_settings_core as ss_core
	global settings
	settings = ss_core.SettingsWrapper()


class RunQuickPanelMixin():
	
	def run(self):
		names = settings.get_settings()
		cur_name = settings.get_current_settings()
		index = names.index(cur_name)
		names[index] = names[index] + ' (Current Settings)'

		sublime.active_window().show_quick_panel(names, self.on_done)


class SwitchSettingsChangeSettingsCommand(RunQuickPanelMixin, sublime_plugin.ApplicationCommand):

	def on_done(self, index):
		if index == -1:
			return

		target = settings.get_settings()[index]

		settings.set_buffer(settings.get_current_settings())
		settings.set_current_settings(target)

		settings.save_ss_settings()


class SwitchSettingsDeleteSettingsCommand(RunQuickPanelMixin, sublime_plugin.ApplicationCommand):

	def on_done(self, index):
		if index == -1:
			return

		target = settings.get_settings()[index]

		if target == settings.get_current_settings():
			sublime.error_message(u'SwitchSettings\n\nSorry, current settings cannot be deleted.\n')
			return

		if not sublime.ok_cancel_dialog(u'SwitchSettings\n\n Do you want to delete "{0}"?\n'.format(target)):
			return

		settings.remove_settings(target)
		settings.pop_settings_content(target)

		settings.save_ss_settings()


class SwitchSettingsShowSettingsListCommand(RunQuickPanelMixin, sublime_plugin.ApplicationCommand):

	def on_done(self, index):
		pass


class SwitchSettingsNewSettingsCommand(sublime_plugin.ApplicationCommand):
	
	def run(self):
		sublime.active_window().show_input_panel('New Settings Name:', '', self.on_done, None, None)

	def on_done(self, new_settings_name):
		import re

		if new_settings_name in settings.get_settings():
			sublime.error_message(u'SwitchSettings\n\n"{0}" already exists.\n'.format(new_settings_name))
			return

		if not re.match('^[_0-9A-Za-z]+$', new_settings_name):
			sublime.error_message(u'SwitchSettings\n\nPlease use only letters (a-z,A-z), numbers (0-9), and underscore.\n')
			return
		
		settings.add_settings(new_settings_name)
		settings.add_settings_content(new_settings_name, {})

		if sublime.ok_cancel_dialog(u'SwitchSettings\n\n"{0}" has been successfully created!\nDo you want to change it now?\n'.format(new_settings_name), 'Change'):
			settings.set_buffer(settings.get_current_settings())
			settings.set_current_settings(new_settings_name)

		settings.save_ss_settings()


class SwitchSettingsRenameSettingsCommand(RunQuickPanelMixin, sublime_plugin.ApplicationCommand):

	def on_done(self, index):
		import functools

		if index == -1:
			return

		old_name = settings.get_settings()[index]
		view = sublime.active_window().show_input_panel('New Name:', old_name, functools.partial(self.__on_done, old_name), None, None)
		view.sel().clear()
		view.sel().add(sublime.Region(0, view.size()))

	def __on_done(self, old_name, new_name):
		import re

		if new_name in settings.get_settings():
			sublime.error_message(u'SwitchSettings\n\n"{0}" already exists.\n'.format(new_name))
			return

		if not re.match('^[_0-9A-Za-z]+$', new_name):
			sublime.error_message(u'SwitchSettings\n\nPlease use only letters (a-z,A-z), numbers (0-9), and underscore.\n')
			return

		if settings.get_current_settings() == old_name:
			settings.set_current_settings(new_name)

		settings.remove_settings(old_name)
		settings.add_settings(new_name)
		tmp = settings.pop_settings_content(old_name)
		settings.add_settings_content(new_name, tmp)

		settings.save_ss_settings()















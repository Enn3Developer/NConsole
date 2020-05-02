from NConsole.console import ConsoleLogType
from os import path
import json

# Overriden by a class that handle a command
class Command:
	# Initialize a command
	def __init__(self, command: str, help_message: str, aliases=[], subcommands=[], args_accepted=[]):
		self.command = command
		self.help_message = help_message
		self.aliases = aliases
		self.subcommands = subcommands
		self.vars_to_save = {}

	# vars_to_save must be a dict with key as name, and value as your var
	def set_vars_to_save(self, vars_to_save):
		self.vars_to_save = vars_to_save
	
	# Called by CommandsRegister, don't override
	def save_all(self):
		if self.vars_to_save:
			file_json = open(f"{self.command}.json", "w+")
			json.dump(self.vars_to_save, file_json, indent=4)
			file_json.close()
	
	# You have to override this and get savings from the file
	def get_savings(self):
		pass

	# You have to override this, here you handle your commands
	# ATTENTION: the first statement has to be args = args[0] or else it will be bugged
	def on_command(self, *args):
		pass


# Is a register of all commands
class CommandsRegister:
	# Initialize the class
	def __init__(self):
		self.commands = []

	# You have to pass your command class
	def register_command(self, command: Command):
		self.commands.append(command)

	# Return a Command from a command name, not alias
	def get_command_from_command_name(self, command_name: str) -> Command:
		for command in self.commands:
			if command_name == command.command:
				return command
	
	# Calls save_all() of all commands registered
	def save_all(self):
		for command in self.commands:
			command.save_all()
	
	# Calls get_savings() of all commands registered
	def get_savings(self):
		for command in self.commands:
			command.get_savings()

	# Called by Console, it handles input and calls on_command() of the right class
	def check_input(self, input_check: str):
		input_check = input_check.lower()
		input_check_splitted = input_check.split(" ")
		command_name = input_check_splitted[0]
		args = input_check_splitted[1:]
		error_command = 0
		max_error = 0
		for command in self.commands:
			if not command.aliases:
				max_error += 1
				if command_name == command.command:
					if not args:
						command.on_command()
					else:
						command.on_command(args)
			else:
				for alias in command.aliases:
					max_error += 1
					if command_name == command.command or command_name == alias:
						if not args:
							command.on_command()
						else:
							command.on_command(args)
					else:
						error_command += 1
		if error_command == max_error:
			print(f"\033[91m[ERROR] {command_name} is an invalid command")

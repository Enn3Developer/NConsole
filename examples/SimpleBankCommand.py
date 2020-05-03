from NConsole.commands import Command, CommandsRegister
from NConsole.console import Console, ConsoleLogType
from os import path

commands_register = CommandsRegister()
console = Console("> ", commands_register)


class BankCommand(Command):
    def __init__(self):
        super().__init__("bank", "Simple command to manage a simple bank", ["b"], ["add", "sub", "create", "print"], ["money", "name"])
        self.accounts = {}
        vars_to_save = {
            "accounts": self.accounts
        }
        self.set_vars_to_save(vars_to_save)
    
    def create_account(self, name):
        self.accounts[name] = 0
    
    def add_money(self, name, money):
        self.accounts[name] += money
    
    def sub_money(self, name, money):
        self.accounts[name] -= money

    def on_command(self, *args):
        args = args[0]
        if len(args) == 2:
            subcommand = args[0].lower()
            account_name = args[1]
            if subcommand == "create":
                self.create_account(account_name)
            elif subcommand == "print":
                console.log(ConsoleLogType.INFO, self.accounts[account_name])
        elif len(args) == 3:
            subcommand = args[0].lower()
            account_name = args[1]
            money = int(args[2])
            if subcommand == "add":
                self.add_money(account_name, money)
            elif subcommand == "sub":
                self.sub_money(account_name, money)


class QuitCommand(Command):
    def __init__(self):
        super().__init__("quit", "Quit program", ["q", "exit", "e"])
    
    def on_command(self, *args):
        commands_register.save_all()
        exit(0)


def start():
    console.log(ConsoleLogType.INFO, "Try various input, then relaunch and check if everything is correct.")
    commands_register.register_command(BankCommand())
    commands_register.register_command(QuitCommand())


def main():
    start()
    if path.exists("bank.json"):
        commands_register.get_savings()
        print("yay")
    while True:
        console.update()


if __name__ == "__main__":
    main()
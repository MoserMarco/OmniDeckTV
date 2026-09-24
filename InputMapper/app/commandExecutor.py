from app.command import Command

class CommandExecutor:
    def execute(self, command: Command):


        print(f"[EXECUTOR] Command received -> Exectuting: {command.type}")
        return
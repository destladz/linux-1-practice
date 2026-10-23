import unittest

from parser import parse_command
from shell import Shell


class ParserTests(unittest.TestCase):
    def test_command_without_arguments(self):
        self.assertEqual(parse_command("ls"), ("ls", []))

    def test_command_with_arguments(self):
        self.assertEqual(
            parse_command("ls -l /home"),
            ("ls", ["-l", "/home"]),
        )

    def test_empty_input(self):
        self.assertEqual(parse_command("   "), (None, []))


class ShellTests(unittest.TestCase):
    def setUp(self):
        self.shell = Shell("student", "computer")

    def test_ls_stub(self):
        result, should_exit = self.shell.execute("ls -l")
        self.assertEqual(result, "ls: аргументы: -l")
        self.assertFalse(should_exit)

    def test_cd_invalid_arguments(self):
        result, should_exit = self.shell.execute("cd one two")
        self.assertIn("Ошибка:", result)
        self.assertFalse(should_exit)

    def test_unknown_command(self):
        result, should_exit = self.shell.execute("unknown")
        self.assertIn("неизвестная команда", result)
        self.assertFalse(should_exit)

    def test_exit(self):
        result, should_exit = self.shell.execute("exit")
        self.assertTrue(should_exit)

    def test_exit_with_arguments(self):
        result, should_exit = self.shell.execute("exit now")
        self.assertIn("Ошибка:", result)
        self.assertFalse(should_exit)


if __name__ == "__main__":
    unittest.main()

"""Tests for the bash completion in completions/check_remote_load."""
import os
import pwd
import re
import shutil
import subprocess
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PLUGIN = os.path.join(ROOT, "check_remote_load")
COMPLETION = os.path.join(ROOT, "completions", "check_remote_load")


def complete(*words, env=None):
    """The candidates bash offers for the last of words, which may be empty."""
    words = ("check_remote_load",) + words
    script = 'source "$1"; shift; COMP_WORDS=("$@"); COMP_CWORD=$(($# - 1)); ' \
             '$(complete -p "$1" | sed -E "s/.*-F ([^ ]+) .*/\\1/"); printf "%s\\n" "${COMPREPLY[@]}"'
    result = subprocess.run(["bash", "-c", script, "bash", COMPLETION] + list(words),
                            capture_output=True, text=True, check=True, env=env)
    return [line for line in result.stdout.split("\n") if line]


def help_options():
    """The options -h lists; it exits with UNKNOWN."""
    text = subprocess.run(["bash", PLUGIN, "-h"], capture_output=True, text=True).stdout
    return set(re.findall(r"^ (-\w)\s", text, re.MULTILINE))


@unittest.skipUnless(shutil.which("bash"), "bash is not installed")
class CompletionTests(unittest.TestCase):
    def test_syntax(self):
        subprocess.run(["bash", "-n", COMPLETION], check=True)

    def test_offers_exactly_the_options_of_help(self):
        self.assertEqual(len(help_options()), 5)
        self.assertEqual(set(complete("")), help_options())

    def test_option_prefix(self):
        self.assertEqual(complete("-H", "x", "-u"), ["-u"])

    def test_host_names(self):
        with tempfile.NamedTemporaryFile("w") as hosts:
            hosts.write("192.0.2.1 server.example.com\n192.0.2.2 backup.example.com\n")
            hosts.flush()
            env = dict(os.environ, HOSTFILE=hosts.name)
            self.assertEqual(complete("-H", "se", env=env), ["server.example.com"])

    def test_user_names(self):
        user = pwd.getpwuid(os.getuid()).pw_name
        self.assertIn(user, complete("-u", user))

    def test_no_candidates_for_thresholds(self):
        for option in ("-w", "-c"):
            self.assertEqual(complete(option, ""), [], option)


if __name__ == "__main__":
    unittest.main()

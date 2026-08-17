"""Run esoteric-language source files using an interpreter already
installed on the host system (found via PATH)."""

import os
import platform
import shutil
import subprocess
from pathlib import Path


class Esoteric:
    """
    Runs esoteric-language source files using an interpreter that is
    already installed on the host system (found via PATH), rather than
    a binary bundled inside this package.

    Rationale: shipping precompiled platform binaries inside a PyPI
    package means every user has to trust the maintainer's build/upload
    pipeline for those binaries specifically, and there's no way for an
    installer or auditor to verify them against an upstream source. By
    resolving the interpreter from the system instead, trust shifts to
    whatever the user already installed and vetted themselves (e.g. via
    their OS package manager), and the pip package stays pure Python.

    Interpreter names searched on PATH:
        - Befunge: "bef98"
        - LOLCODE: "lci"

    An explicit override is supported via environment variables
    (FORMATTING_LIBRARY_BEFUNGE_BIN / FORMATTING_LIBRARY_LOLCODE_BIN)
    for users who have the interpreter installed under a nonstandard
    name or location. Overrides must point to an existing, executable
    file; a project-local config file is deliberately NOT consulted
    here, since a path silently read from the current working
    directory (e.g. a repo you just cloned or CI checked out) could be
    used to redirect execution to an attacker-controlled binary without
    the user's awareness. Only explicit, session-scoped environment
    variables are honored.
    """

    INTERPRETER_NAMES = {
        "befunge": "bef98",
        "lolcode": "lci",
    }

    ENV_OVERRIDES = {
        "befunge": "FORMATTING_LIBRARY_BEFUNGE_BIN",
        "lolcode": "FORMATTING_LIBRARY_LOLCODE_BIN",
    }

    INSTALL_HINTS = {
        "befunge": (
            "No 'bef98' interpreter found on PATH.\n"
            "Install a Befunge-98 interpreter and ensure it is on your PATH,\n"
            "or set the FORMATTING_LIBRARY_BEFUNGE_BIN environment variable\n"
            "to the full path of a trusted interpreter executable."
        ),
        "lolcode": (
            "No 'lci' (LOLCODE) interpreter found on PATH.\n"
            "Install lci (https://github.com/justinmeza/lci) and ensure it is\n"
            "on your PATH, or set the FORMATTING_LIBRARY_LOLCODE_BIN\n"
            "environment variable to the full path of a trusted interpreter\n"
            "executable."
        ),
    }

    @staticmethod
    def _resolve_interpreter(language):
        if language not in Esoteric.INTERPRETER_NAMES:
            raise ValueError(f"Unknown language: {language}")

        # 1. Explicit, user-provided override (never read from a
        #    project-local file, only an environment variable the
        #    user themselves set for this session).
        env_var = Esoteric.ENV_OVERRIDES[language]
        override = os.environ.get(env_var)
        if override:
            override_path = Path(override)
            if not override_path.is_file():
                raise FileNotFoundError(
                    f"{env_var} is set to '{override}', but no file exists there."
                )
            if platform.system().lower() != "windows" and not os.access(override_path, os.X_OK):
                raise PermissionError(
                    f"{env_var} points to '{override}', which is not executable."
                )
            return str(override_path)

        # 2. Search the system PATH for the interpreter.
        interpreter_name = Esoteric.INTERPRETER_NAMES[language]
        found = shutil.which(interpreter_name)
        if found:
            return found

        raise FileNotFoundError(Esoteric.INSTALL_HINTS[language])

    @staticmethod
    def _run_language(language, filename=''):
        if not filename:
            raise ValueError("Filename cannot be empty")

        executable_path = Esoteric._resolve_interpreter(language)

        try:
            result = subprocess.run(
                [executable_path, filename],
                check=True,
                capture_output=False
            )
            return result.returncode
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Execution failed with code {e.returncode}")

    @staticmethod
    def runBefunge(filename=''):
        return Esoteric._run_language("befunge", filename)

    @staticmethod
    def runLOLCODE(filename=''):
        return Esoteric._run_language("lolcode", filename)


# Aliases
runBefunge = Esoteric.runBefunge
runLOLCODE = Esoteric.runLOLCODE

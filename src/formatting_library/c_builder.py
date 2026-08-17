"""Build and load C shared libraries for Python (ctypes) integration."""

import ctypes
import os
import platform


class CBuilder:
    """
    WARNING: This class uses os.system() to compile C code and creates
    directories. Only use with trusted source files in secure environments.

    Builds and loads C shared libraries for Python integration.
    Supports Windows (.dll), macOS (.dylib), and Linux (.so).
    """

    def __init__(self, directory=".", filename="main", build_command=None):
        self.directory = directory
        self.filename = filename
        self.build_command = build_command
        self.lib = None
        self.platform = platform.system().lower()
        self._build()

    def _get_library_extension(self):
        extensions = {
            'windows': '.dll',
            'darwin': '.dylib',
            'linux': '.so'
        }
        return extensions.get(self.platform, '.so')

    def _get_default_compiler_command(self, output_path, input_path):
        if self.platform == 'windows':
            return f"gcc -Ofast -shared -o {output_path} {input_path}"
        elif self.platform == 'darwin':
            return f"gcc -Ofast -march=native -mtune=native -funroll-loops -fomit-frame-pointer -DNDEBUG -shared -fPIC -undefined dynamic_lookup -o {output_path} {input_path}"
        else:
            return f"gcc -Ofast -march=native -mtune=native -funroll-loops -fomit-frame-pointer -DNDEBUG -shared -fPIC -o {output_path} {input_path} -lrt"

    def _build(self):
        lib_extension = self._get_library_extension()

        if self.directory == ".":
            output_path = f"build/{self.filename}{lib_extension}"
            lib_path = f"./build/{self.filename}{lib_extension}"
        else:
            output_path = f"{self.directory}/build/{self.filename}{lib_extension}"
            lib_path = f"./{self.directory}/build/{self.filename}{lib_extension}"

        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        input_path = f"{self.directory}/{self.filename}.c"

        if self.build_command is None:
            compile_command = self._get_default_compiler_command(output_path, input_path)
        else:
            compile_command = self.build_command.format(
                output=output_path,
                input=input_path
            )

        result = os.system(compile_command)

        if result == 0:
            self.lib = ctypes.CDLL(lib_path)
        else:
            platform_info = {
                'windows': 'Ensure MinGW, MSYS2, or Visual Studio Build Tools are installed',
                'darwin': 'Ensure Xcode Command Line Tools are installed (xcode-select --install)',
                'linux': 'Ensure GCC and build-essential are installed'
            }
            suggestion = platform_info.get(self.platform, 'Ensure GCC compiler is available')
            raise RuntimeError(
                f"Compilation failed with code {result} on {self.platform.title()}. "
                f"{suggestion}"
            )

    def define_function(self, func_name, args=None, rtype=None):
        if self.lib is None:
            raise RuntimeError("Library not loaded")

        if args is None:
            args = []

        func_obj = getattr(self.lib, func_name)

        if isinstance(args, list):
            func_obj.argtypes = args
        else:
            func_obj.argtypes = []

        func_obj.restype = rtype
        return func_obj

    def get_platform_info(self):
        return {
            'platform': self.platform,
            'library_extension': self._get_library_extension(),
            'python_architecture': platform.architecture(),
            'machine': platform.machine()
        }

#!/usr/bin/env python3

import os
import platform
import subprocess
import sys

from formatting import Formatter as fmt


class SafeSubprocess:
    __safe_commands = ["node", "brew", "git"]

    def __init__(self, is_test: bool):
        self.is_test = is_test

    def run(self, cmd):
        if isinstance(cmd, list):
            print("$", fmt.underline(" ".join(cmd)))
        else:
            print("$", fmt.underline(cmd))

        # Only run command if not testing, or command is safe
        if (not self.is_test) or (cmd[0] in self.__safe_commands):
            return subprocess.run(cmd)


def error(msg: str):
    print(fmt.error(msg))
    sys.exit(1)


def info(msg: str):
    print()
    print(fmt.info(fmt.bold(msg)))


def success(msg: str):
    print(fmt.success(fmt.bold(msg)))


class Test:
    def __init__(self, user_os: str):
        self.is_test = len(sys.argv) > 1 and "--test" in sys.argv[1:]

        if self.is_test:
            info("Running in TEST mode")

            self.paths = {
                "config_file": "./tests/.config/nvim/init.vim",
                "config_folder": "./tests/.config/nvim",
                "plugin_folder": "./tests/plug.vim",
                "node_folder": ["./tests/local/bin/node"],
                "brew_folder": "./tests/homebrew/bin/brew",
                "sh_rc": "./tests/.bashrc" if os == "linux" else "./tests/.zshrc",
            }
        else:
            self.paths = {
                "config_file": f"{os.environ['HOME']}/.config/nvim/init.vim",
                "config_folder": f"{os.environ['HOME']}/.config/nvim",
                "plugin_folder": f"{os.environ['HOME']}/.local/share/nvim/site/autoload/plug.vim",
                "node_folder": "/usr/local/bin/node",
                "brew_folder": "/opt/homebrew/bin/brew",
                "sh_rc": f"{os.environ['HOME']}/.bashrc"
                if user_os == "linux"
                else f"{os.environ['HOME']}/.zshrc",
            }

    def run_tests(self):
        # Check nvim
        # Check nvim config
        # Check vim-plug
        # Check node
        # Check ctags
        # Check plugins
        pass


class Commands:
    def __init__(self, is_dcu: bool, test: Test):
        # Collect info about the system
        self.is_dcu = is_dcu
        self.test = test
        self.cwd = os.getcwd()
        self.subprocess = SafeSubprocess(test.is_test)

    def install_nvim(self):
        raise NotImplementedError("nvim installation not implemented")

    def install_ctags(self):
        raise NotImplementedError("ctags installation not implemented")

    def add_aliases(self):
        info("Adding aliases to your shell rc file...")
        if not os.path.exists(self.test.paths["sh_rc"]):
            self.subprocess.run(["touch", self.test.paths["sh_rc"]])
            success(f"Created shell rc file at {self.test.paths['sh_rc']}")

        with open(self.test.paths["sh_rc"], "a") as f:
            f.write("\n# Nvim aliases\n")
            f.write(f"alias nvim='{self.cwd}/nvim'\n")
            f.write(f"alias nv='{self.cwd}/nvim'\n")

        success("Added aliases")

    def copy_config(self):
        info("Copying nvim config...")
        if not os.path.exists(self.test.paths["config_folder"]):
            self.subprocess.run(["mkdir", "-p", self.test.paths["config_folder"]])

        if not os.path.exists(self.test.paths["config_file"]):
            self.subprocess.run(
                ["cp", f"./scripts/init.vim", self.test.paths["config_file"]]
            )
        else:
            with open(self.test.paths["config_file"], "a") as f:
                with open(f"./scripts/init.vim", "r") as f2:
                    f.write(f2.read())

        success("Copied nvim config")

    def install_vim_plug(self):
        info("Installing vim-plug...")
        self.subprocess.run(
            [
                "curl",
                "-fLo",
                self.test.paths["plugin_folder"],
                "--create-dirs",
                "https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim",
            ]
        )

        success("Installed vim-plug")

    def check_node(self):
        info("Checking for node installation...")
        node = self.subprocess.run(["node", "-v"])
        if not node:
            error("Node is not installed. Please install node before continuing.")

        success("Node is installed")

    def check_git(self):
        info("Checking for git installation...")
        git = self.subprocess.run(["git", "--version"])
        if not git:
            error("Git is not installed. Please install git before continuing.")

        success("Git is installed")

    def install_plugins(self):
        info("Installing nvim plugins...")
        self.subprocess.run(["nvim", "--headless", "+PlugInstall", "+qall"])

        if not self.is_dcu:
            self.subprocess.run(
                ["nvim", "--headless", "+CocInstall coc-pyright", "+qall"]
            )

        success("Installed nvim plugins")

    def install(self):
        # Determine OS -
        # Check if node is installed -
        # Check if git is installed -
        # Check/install nvim -
        # Copy nvim config to ~/.config/nvim -
        # Install vim-plug -
        # Install ctags -
        # Add aliases if not root -
        # Install plugins -
        info("Starting installation...")
        self.check_node()
        self.check_git()

        self.install_nvim()
        self.copy_config()
        self.install_vim_plug()

        if self.is_dcu:
            self.add_aliases()
        else:
            self.install_ctags()

        self.install_plugins()

        with open(self.test.paths["config_file"], "a") as f:
            f.write("\n:colorscheme onehalfdark")


class MacCommands(Commands):
    def install_nvim(self):
        info("Installing nvim...")
        self.subprocess.run(["brew", "install", "neovim"])
        success("Installed nvim")

    def install_ctags(self):
        info("Installing ctags...")
        self.subprocess.run(["xcode-select", "--install"])
        self.subprocess.run(["brew", "tap", "universal-ctags/universal-ctags"])
        self.subprocess.run(["brew", "install", "--HEAD", "universal-ctags"])
        success("Installed ctags")

    def check_brew(self):
        info("Checking for brew installation...")

        brew = self.subprocess.run(["brew", "-v"])

        if not brew:
            error("Brew is not installed. Please install brew before continuing.")

        success("Brew is installed")


class LinuxCommands(Commands):
    def install_nvim(self):
        info("Installing nvim...")
        if not self.is_dcu:
            self.subprocess.run("sudo apt install neovim")
        else:
            self.subprocess.run(
                [
                    "curl",
                    "-LO",
                    "https://github.com/neovim/neovim/releases/latest/download/nvim.appimage",
                ]
            )
            self.subprocess.run(["chmod", "u+x", "nvim.appimage"])
            self.subprocess.run(["mv", "nvim.appimage", "nvim"])

        success("Installed nvim")

    def install_ctags(self):
        info("Installing ctags...")
        self.subprocess.run(
            ["git", "clone", "https://github.com/universal-ctags/ctags.git"]
        )
        self.subprocess.run(["cd", "ctags"])

        self.subprocess.run(
            [
                "sudo",
                "apt",
                "install",
                "gcc",
                "make",
                "pkg-config",
                "autoconf",
                "automake",
                "python3-docutils",
                "libseccomp-dev",
                "libjansson-dev",
                "libyaml-dev",
                "libxml2-dev",
            ]
        )

        self.subprocess.run(["./autogen.sh"])
        self.subprocess.run(["./configure"])
        self.subprocess.run(["make"])
        self.subprocess.run(["make", "install"])
        self.subprocess.run(["cd", ".."])

        success("Installed ctags")


def main():
    user_os = platform.system()

    test = Test(user_os)

    # Kill the script if the OS is not supported
    if user_os == "Windows":
        error(
            "Windows is not supported. Please use WSL or switch to Linux and run this script again."
        )

    is_dcu = len(sys.argv) > 1 and "--dcu" in sys.argv[1:]

    if user_os == "Darwin":
        commands = MacCommands(is_dcu, test)
        commands.check_brew()
    else:
        commands = LinuxCommands(is_dcu, test)

    commands.install()

    if test.is_test:
        test.run_tests()


if __name__ == "__main__":
    main()

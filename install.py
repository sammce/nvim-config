#!/usr/bin/env python3
import os
import platform
import subprocess
import sys
from pprint import pprint

from formatting import Formatter as fmt


class test_subprocess:
    @staticmethod
    def run(cmd):
        print(fmt.bold("Running command: "))
        print(fmt.underline(" ".join(cmd)))


class Test:
    def __init__(self, os: str):
        self.test = len(sys.argv) > 1 and "--test" in sys.argv[1:]

        if self.test:
            print(fmt.bold(fmt.info("Running in TEST mode")))
            print("-" * 40)

            subprocess.run = test_subprocess.run
            self.paths = {
                "config_file": "./tests/.config/nvim/init.vim",
                "config_folder": "./tests/.config/nvim",
                "plugin_folder": "./tests/plug.vim",
                "node_folder": "./tests/local/bin/node",
                "brew_folder": "./tests/homebrew/bin/brew",
                "sh_rc": "./tests/.bashrc" if os == "linux" else "./tests/.zshrc",
            }
        else:
            self.paths = {
                "config_file": "~/.config/nvim/init.vim",
                "config_folder": "~/.config/nvim",
                "plugin_folder": '"${XDG_DATA_HOME:-$HOME/.local/share}"/nvim/site/autoload/plug.vim',
                "node_folder": "/usr/local/bin/node",
                "brew_folder": "/opt/homebrew/bin/brew",
                "sh_rc": "~/.bashrc" if os == "linux" else "~/.zshrc",
            }

    def run_tests(self):
        # Check nvim
        # Check nvim config
        # Check vim-plug
        # Check node
        # Check ctags
        # Check plugins
        pass


def error(msg: str):
    print(fmt.error(msg))
    sys.exit(1)


class Commands:
    def __init__(self, is_root: bool, test: Test):
        # Collect info about the system
        self.is_root = is_root
        self.test = test
        self.cwd = os.getcwd()

    def install_nvim(self):
        raise NotImplementedError("nvim installation not implemented")

    def install_ctags(self):
        raise NotImplementedError("ctags installation not implemented")

    def add_aliases(self):
        with open(self.test.paths["sh_rc"], "a") as f:
            f.write("\n# Nvim aliases\n")
            f.write(f"alias nvim='{self.cwd}/nvim'\n")
            f.write(f"alias nv='{self.cwd}/nvim'\n")

    def copy_config(self):
        print(fmt.bold("Copying nvim config..."))
        if not os.path.exists(self.test.paths["config_folder"]):
            subprocess.run(["mkdir", "-p", self.paths["config_folder"]])

        filename = "sudo_init.vim" if self.is_root else "init.vim"

        if not os.path.exists(self.test.paths["config_file"]):
            subprocess.run(
                ["cp", f"./scripts/{filename}", self.test.paths["config_file"]]
            )
        else:
            with open(self.test.paths["config_file"], "a") as f:
                with open(f"./scripts/{filename}", "r") as f2:
                    f.write(f2.read())

    def install_vim_plug(self):
        print(fmt.bold("Installing vim-plug..."))
        subprocess.run(
            [
                "sh",
                "-c",
                f"'curl -fLo {self.test.paths['plugin_folder']} --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'",
            ]
        )

    def check_node(self):
        print(fmt.bold("Checking for node installation..."))
        if not os.path.exists(self.test.paths["node_folder"]):
            error("Node is not installed. Please install node before continuing.")

    def check_git(self):
        print(fmt.bold("Checking for git installation..."))
        if not os.path.exists("/usr/bin/git"):
            error("Git is not installed. Please install git before continuing.")

    def install_plugins(self):
        print(fmt.bold("Installing nvim plugins..."))
        subprocess.run(["nvim", "--headless", "+PlugInstall", "+qall"])

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
        print(fmt.bold("Starting installation..."))
        self.check_node()
        self.check_git()

        self.install_nvim()
        self.copy_config()
        self.install_vim_plug()

        if self.is_root:
            self.install_ctags()
            self.add_aliases()

        self.install_plugins()


class MacCommands(Commands):
    def install_nvim(self):
        print(fmt.bold("Installing nvim..."))
        subprocess.run("brew install neovim")

    def install_ctags(self):
        print(fmt.bold("Installing ctags..."))
        subprocess.run(["xcode-select", "--install"])
        subprocess.run(["brew", "tap", "universal-ctags/universal-ctags"])
        subprocess.run(["brew", "install", "--HEAD", "universal-ctags"])


class LinuxCommands(Commands):
    def install_nvim(self):
        print(fmt.bold("Installing nvim..."))
        if self.is_root:
            subprocess.run("sudo apt install neovim")
        else:
            subprocess.run(
                [
                    "curl",
                    "-LO",
                    "https://github.com/neovim/neovim/releases/latest/download/nvim.appimage",
                ]
            )
            subprocess.run(["chmod", "u+x", "nvim.appimage"])
            subprocess.run(["mv", "nvim.appimage", "nvim"])
            subprocess.run(["cd", ".."])

            with open("~/.bashrc", "a") as f:
                f.write(f"alias nvim='{os.getcwd()}/nvim'")

    def install_ctags(self):
        print(fmt.bold("Installing ctags..."))
        subprocess.run(["git", "clone", "https://github.com/universal-ctags/ctags.git"])
        subprocess.run(["cd", "ctags"])

        subprocess.run(
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

        subprocess.run(["./autogen.sh"])
        subprocess.run(["./configure"])
        subprocess.run(["make"])
        subprocess.run(["make", "install"])
        subprocess.run(["cd", ".."])


def main():
    is_root = os.geteuid() == 0
    user_os = platform.system()

    # Kill the script if the OS is not supported
    if user_os == "Windows":
        error(
            "Windows is not supported. Please use WSL or switch to Linux and run this script again."
        )

    # Check if user meant to run without sudo, only if not on dcu lab computer.
    if (not is_root) and platform.node() != "soc-razor1":
        print(
            fmt.error(
                "You are not root. Some plugins (such as autocomplete) won't be installed. You can run as root (sudo) to fix this."
            )
        )
        continue_install = input(fmt.bold("Continue without sudo? [y/N]: ")).lower()
        if continue_install != "y":
            print(fmt.info("Exiting..."))
            sys.exit(0)

    test = Test(user_os)

    if user_os == "Darwin":
        if not os.path.exists(test.paths["brew_folder"]):
            error("Homebrew is not installed. Install it and then rerun this script.")

        commands = MacCommands(is_root, test)
    else:
        commands = LinuxCommands(is_root, test)

    commands.install()

    if test.test:
        test.run_tests()


if __name__ == "__main__":
    main()

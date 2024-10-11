import os
from conan import ConanFile
from conan.tools.files import get, copy, download
from conan.errors import ConanInvalidConfiguration
from conan.tools.scm import Version

class ArmToolchainPackage(ConanFile):
    name = "arm-toolchain"
    version = "12.2"
    ...
    settings = "os", "arch"
    package_type = "application"

    def _archs32(self):
        return ["armv6", "armv7", "armv8"]

    def _get_toolchain(self, target_arch):
        return ("arm-none-eabi",
                "84be93d0f9e96a15addd490b6e237f588c641c8afdf90e7610a628007fc96867")

    def validate(self):
        if self.settings.arch != "x86_64" or self.settings.os != "Linux":
            raise ConanInvalidConfiguration(f"This toolchain is not compatible with {self.settings.os}-{self.settings.arch}. "
                                            "It can only run on Linux-x86_64.")

        valid_archs = self._archs32()
        if self.settings_target.os != "baremetal" or self.settings_target.arch not in valid_archs:
            raise ConanInvalidConfiguration(f"This toolchain only supports building for baremetal-{valid_archs.join(',')}. "
                                        f"{self.settings_target.os}-{self.settings_target.arch} is not supported.")

        if self.settings_target.compiler != "gcc":
            raise ConanInvalidConfiguration(f"The compiler is set to '{self.settings_target.compiler}', but this "
                                            "toolchain only supports building with gcc.")

        if Version(self.settings_target.compiler.version) >= Version("13") or Version(self.settings_target.compiler.version) < Version("12"):
           raise ConanInvalidConfiguration(f"Invalid gcc version '{self.settings_target.compiler.version}'. "
                                                "Only 12.X versions are supported for the compiler.")

    def source(self):
        download(self, "https://developer.arm.com/GetEula?Id=37988a7c-c40e-4b78-9fd1-62c20b507aa8", "LICENSE", verify=False)

    def build(self):
        # Source is actually downloaded here since we can potentially setup multiple targets
        toolchain, sha = self._get_toolchain(self.settings_target.arch)
        get(self, f"https://developer.arm.com/-/media/Files/downloads/gnu/12.2.rel1/binrel/arm-gnu-toolchain-12.2.rel1-x86_64-{toolchain}.tar.xz",
            sha256=sha, strip_root=True)

    def package_id(self):
        self.info.settings_target = self.settings_target
        # We only want the ``arch`` setting
        self.info.settings_target.rm_safe("os")
        self.info.settings_target.rm_safe("compiler")
        self.info.settings_target.rm_safe("build_type")

    def package(self):
        toolchain, _ = self._get_toolchain(self.settings_target.arch)
        dirs_to_copy = [toolchain, "bin", "include", "lib", "libexec"]
        for dir_name in dirs_to_copy:
            copy(self, pattern=f"{dir_name}/*", src=self.build_folder, dst=self.package_folder, keep_path=True)
        copy(self, "LICENSE", src=self.build_folder, dst=os.path.join(self.package_folder, "licenses"), keep_path=False)

    def package_info(self):
        toolchain, _ = self._get_toolchain(self.settings_target.arch)
        self.cpp_info.bindirs.append(os.path.join(self.package_folder, toolchain, "bin"))

        self.conf_info.define("tools.build:compiler_executables", {
            "c":   f"{toolchain}-gcc",
            "cpp": f"{toolchain}-g++",
            "asm": f"{toolchain}-as"
        })


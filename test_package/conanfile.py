import os
from io import StringIO

from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout


class TestPackageConan(ConanFile):
    settings = "os", "arch", "compiler", "build_type"
    generators = "VirtualBuildEnv"

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["CMAKE_TRY_COMPILE_TARGET_TYPE"] = "STATIC_LIBRARY"
        tc.generate()

    def build_requirements(self):
        self.tool_requires(self.tested_reference_str)

    def layout(self):
        cmake_layout(self)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        assert self.settings.arch in ["armv6", "armv7", "armv8"]
        toolchain = "arm-none-eabi"
        self.run(f"{toolchain}-gcc --version")
        test_file = os.path.join(self.cpp.build.bindirs[0], "libtest_package.a")
        stdout = StringIO()
        self.run(f"file {test_file}", stdout=stdout)
        assert "ar archive" in stdout.getvalue()

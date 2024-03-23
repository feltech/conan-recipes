import os

from conan import ConanFile
from conan.tools.scm import Git
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.tools.files import copy, replace_in_file, apply_conandata_patches


class CucumberCppRecipe(ConanFile):
    name = "cucumbercpp"
    version = "main"
    package_type = "library"

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    def requirements(self):
        self.requires("tclap/1.2.5")
        self.requires("asio/1.29.0")
        self.requires("nlohmann_json/3.11.3")

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.rm_safe("fPIC")

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def layout(self):
        cmake_layout(self, src_folder="src")

    def source(self):
        git = Git(self)
        git.clone(url="https://github.com/cucumber/cucumber-cpp.git", target=".")
        git.folder = "."
        git.checkout(commit=self.version)
        apply_conandata_patches(self)

    def export_sources(self):
        copy(self, "patches/*", ".", self.export_sources_folder)
        copy(self, "CMakeLists.txt", self.folders.source, self.export_sources_folder)
        copy(self, "cmake/*.cmake", self.folders.source, self.export_sources_folder)
        copy(self, "src/*.cpp", self.folders.source, self.export_sources_folder)
        copy(self, "include/*.hpp", self.folders.source, self.export_sources_folder)

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.cache_variables.update({

        })
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.builddirs = [self.package_folder]
        self.cpp_info.set_property("cmake_find_mode", "none")

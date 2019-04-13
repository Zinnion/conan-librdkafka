#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from conans import ConanFile, tools, AutoToolsBuildEnvironment, CMake
from conans.model.version import Version
from conans.errors import ConanInvalidConfiguration


class librdkafkaRecipe(ConanFile):
    name = "librdkafka"
    version = "1.0.0"
    settings = "os", "compiler", "build_type", "arch", "cppstd"
    description = "The Apache Kafka C/C++ libraryL"
    url = "https://github.com/Zinnion/conan-librdkafka"
    homepage = "https://github.com/edenhill/librdkafka"
    author = "Zinnion <mauro@zinnion.com>"
    license = "BSD-3-Clause"
    topics = ("conan", "librdkafka", "kafka", "streaming")
    generators = "cmake"
    exports = "LICENSE.md"
    exports_sources = "CMakeLists.txt"
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"
    _autotools = None

    def configure(self):
        compiler_version = Version(self.settings.compiler.version.value)

        if self.settings.os == "Windows" and \
           self.settings.compiler == "Visual Studio" and \
           compiler_version < "14":
            raise ConanInvalidConfiguration(
                "Your MSVC version is too old, librdkafka requires C++14")

        if self.settings.os == "Macos" and \
           self.settings.compiler == "apple-clang" and \
           compiler_version < "8.0":
            raise ConanInvalidConfiguration(("librdkafka requires thread-local storage features,"
                                             " could not be built by apple-clang < 8.0"))

    def source(self):
        sha256 = "b00a0d9f0e8c7ceb67b93b4ee67f3c68279a843a15bf4a6742eb64897519aa09"
        tools.get("{0}/archive/v{1}.tar.gz".format(self.homepage,
                                                  self.version), sha256=sha256)
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def configure_cmake(self):
        cmake = CMake(self)
        cmake.configure()
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        cmake = self.configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")
        elif self.settings.os == "Windows":
            self.cpp_info.libs.append("ws2_32")

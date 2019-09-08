import os
from conans import ConanFile, AutoToolsBuildEnvironment, tools
from conans.errors import ConanInvalidConfiguration


class ReadLineConan(ConanFile):
    name = "librdkafka"
    version = "1.1.0"
    description = "The Apache Kafka C/C++ library"
    url = "https://github.com/zinnion/conan-librdkafka"
    homepage = "https://github.com/edenhill/librdkafka"
    topics = ("conan", "librdkafka", "kafka", "streaming")
    author = "Zinnion <mauro@zinnion.com>"
    license = "GPL-3"
    exports = ["LICENSE.md"]
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False] }
    default_options = {"shared": False }
    _source_subfolder = "source_subfolder"
    _autotools = None

    def source(self):
        sha256 = "123b47404c16bcde194b4bd1221c21fdce832ad12912bd8074f88f64b2b86f2b"
        tools.get("{0}/archive/v{1}.tar.gz".format(self.homepage,self.version), sha256=sha256)
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def build_requirements(self):
        self.build_requires("OpenSSL/1.1.1b@zinnion/stable")
        self.build_requires("zlib/1.2.11@zinnion/stable")

    def _configure_autotools(self):
        if not self._autotools:
            configure_args = []
            self._autotools = AutoToolsBuildEnvironment(self)
            self._autotools.configure(args=configure_args)
        return self._autotools

    def build(self):
        with tools.chdir(self._source_subfolder):
            autotools = self._configure_autotools()
            autotools.make()

    def package(self):
        self.copy("COPYING", dst="licenses", src=self._source_subfolder)
        with tools.chdir(self._source_subfolder):
            autotools = self._configure_autotools()
            autotools.install()

    def package_info(self):
        self.cpp_info.libs = ["rdkafka", "rdkafka++"]
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")
        elif self.settings.os == "Windows":
            self.cpp_info.libs.append("ws2_32")

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import tools
from bincrafters import build_template_default

if __name__ == "__main__":
    shared_option_name = False if platform.system() == "Darwin" else "readline:shared"
    builder = build_template_default.get_builder(pure_c=True, shared_option_name=shared_option_name)
    builder.run()

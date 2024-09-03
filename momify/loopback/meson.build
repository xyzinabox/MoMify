
pybind11_dep = dependency('pybind11')
unicode_define = ['-DUNICODE', '-D_UNICODE']
system_libs = ['-lmmdevapi', '-lmf', '-levr', '-lmfplat']

py.extension_module(
    'record',
    sources: ['LoopbackCapture.cpp', 'Record.cpp'],
    cpp_args: unicode_define,
    dependencies : [pybind11_dep],
    install: true,
    subdir: 'momify/loopback'
)

py.install_sources(
  [
    '__init__.py'
  ],
  subdir: 'momify/loopback'
)
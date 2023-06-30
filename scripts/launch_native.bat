@echo off

start /W scripts\\build_native.bat Debug Debug
set RUST_BACKTRACE="1",
start /W build\\windows\\runner\\Debug\\flutter_rust_bridge_template.exe

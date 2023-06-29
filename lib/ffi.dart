import 'dart:ffi';
import 'dart:io' as io;

import "bridge_generated_Api.dart";

const _base = 'native';
final _dylibPath = io.Platform.isWindows ? '$_base.dll' : 'lib$_base.so';
final _dylib = io.Platform.isIOS || io.Platform.isMacOS
    ? DynamicLibrary.executable()
    : DynamicLibrary.open(_dylibPath);

final Api api = ApiImpl(_dylib);

# Client run: 1.3.2+1.21.11

**PASS** — exit joined after 48 s

Software rendering under Xvfb (Mesa llvmpipe): this proves the pack starts and loads a world,
and shows the screens. Its frame rate is not a benchmark.

```
[11:35:56] [main/INFO]: Loading 121 mods:
```

## Metrics

| metric | value |
| --- | --- |

## Crashes

none

## Harness

```
```

## Errors and warnings worth reading (24)

```
[11:35:57] [main/WARN]: Error loading class: net/caffeinemc/mods/sodium/client/render/chunk/compile/pipeline/BlockOcclusionCache (java.lang.ClassNotFoundException: net/caffeinemc/mods/sodium/client/render/chunk/compile/pipeline/BlockOcclusionCache)
[11:35:57] [main/WARN]: Error loading class: dev/emi/emi/screen/StackBatcher (java.lang.ClassNotFoundException: dev/emi/emi/screen/StackBatcher)
[11:35:57] [main/WARN]: Could not find any graphics adapters! Probably the device is not on a bus we can probe, or there are no devices supporting 3D acceleration.
[11:36:01] [Download-2/ERROR]: Failed to fetch user properties
com.mojang.authlib.exceptions.InvalidCredentialsException: Status: 401
	at knot//com.mojang.authlib.exceptions.MinecraftClientHttpException.toAuthenticationException(MinecraftClientHttpException.java:59)
Caused by: com.mojang.authlib.exceptions.MinecraftClientHttpException: Status: 401
[11:36:03] [Render thread/ERROR]: Failed to open pack /home/runner/work/streamline-master/streamline-master/.dev/1.21.11/assets/objects/f2/f262efb6e4797419f8e998db5330c3b006dd6283
java.nio.file.NoSuchFileException: /home/runner/work/streamline-master/streamline-master/.dev/1.21.11/assets/objects/f2/f262efb6e4797419f8e998db5330c3b006dd6283
	at java.base/sun.nio.fs.UnixException.translateToIOException(UnixException.java:92)
	at java.base/sun.nio.fs.UnixException.rethrowAsIOException(UnixException.java:106)
	at java.base/sun.nio.fs.UnixException.rethrowAsIOException(UnixException.java:111)
[11:36:03] [Render thread/ERROR]: Failed to open pack /home/runner/work/streamline-master/streamline-master/.dev/1.21.11/assets/objects/70/703c3ac27bdea2798e46ae5fb93666e670373af1
java.nio.file.NoSuchFileException: /home/runner/work/streamline-master/streamline-master/.dev/1.21.11/assets/objects/70/703c3ac27bdea2798e46ae5fb93666e670373af1
	at java.base/sun.nio.fs.UnixException.translateToIOException(UnixException.java:92)
	at java.base/sun.nio.fs.UnixException.rethrowAsIOException(UnixException.java:106)
	at java.base/sun.nio.fs.UnixException.rethrowAsIOException(UnixException.java:111)
[11:36:03] [Render thread/ERROR]: Error while loading the narrator
com.mojang.text2speech.Narrator$InitializeException: Failed to load library flite
	Suppressed: java.io.IOException: Native library (linux-x86-64/libflite.so) not found in resource path (/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/lz4-java-1.8.1.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/azure-json-1.4.0.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/oshi-core-6.9.0.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/gson-2.13.2.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/failureaccess-1.0.3.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/guava-33.5.0-jre.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/icu4j-77.1.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/msal4j-1.23.1.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/authlib-7.0.61.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/blocklist-1.0.10.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/brigadier-1.3.10.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/datafixerupper-9.0.19.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/jtracy-1.0.37.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/jtracy-1.0.37-natives-linux.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/logging-1.6.11.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/patchy-2.2.10.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/text2speech-1.18.11.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/commons-codec-1.19.0.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/commons-io-2.20.0.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/netty-buffer-4.2.7.Final.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/netty-codec-base-4.2.7.Final.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/netty-codec-compression-4.2.7.Final.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/netty-codec-http-4.2.7.Final.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/netty-common-4.2.7.Final.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/netty-handler-4.2.7.Final.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/netty-resolver-4.2.7.Final.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/netty-transport-classes-epoll-4.2.7.Final.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/netty-transport-classes-kqueue-4.2.7.Final.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/netty-transport-native-epoll-4.2.7.Final-linux-aarch_64.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/netty-transport-native-epoll-4.2.7.Final-linux-x86_64.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/netty-transport-native-unix-common-4.2.7.Final.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/netty-transport-4.2.7.Final.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/fastutil-8.5.18.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/jna-platform-5.17.0.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/jna-5.17.0.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/jopt-simple-5.0.4.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/commons-compress-1.28.0.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/commons-lang3-3.19.0.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/log4j-api-2.25.2.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/log4j-core-2.25.2.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/log4j-slf4j2-impl-2.25.2.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/jorbis-0.0.17.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/joml-1.10.8.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/jspecify-1.0.0.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/lwjgl-freetype-3.3.3.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/lwjgl-freetype-3.3.3-natives-linux.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/lwjgl-glfw-3.3.3.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/lwjgl-glfw-3.3.3-natives-linux.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/lwjgl-jemalloc-3.3.3.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/lwjgl-jemalloc-3.3.3-natives-linux.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/lwjgl-openal-3.3.3.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/lwjgl-openal-3.3.3-natives-linux.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/lwjgl-opengl-3.3.3.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/lwjgl-opengl-3.3.3-natives-linux.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/lwjgl-stb-3.3.3.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/lwjgl-stb-3.3.3-natives-linux.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/lwjgl-tinyfd-3.3.3.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/lwjgl-tinyfd-3.3.3-natives-linux.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/lwjgl-3.3.3.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/lwjgl-3.3.3-natives-linux.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/libs/slf4j-api-2.0.17.jar:/home/runner/work/streamline-master/streamline-master/.dev/fabric/asm-9.10.1.jar:/home/runner/work/streamline-master/streamline-master/.dev/fabric/asm-analysis-9.10.1.jar:/home/runner/work/streamline-master/streamline-master/.dev/fabric/asm-commons-9.10.1.jar:/home/runner/work/streamline-master/streamline-master/.dev/fabric/asm-tree-9.10.1.jar:/home/runner/work/streamline-master/streamline-master/.dev/fabric/asm-util-9.10.1.jar:/home/runner/work/streamline-master/streamline-master/.dev/fabric/sponge-mixin-0.17.3+mixin.0.8.7.jar:/home/runner/work/streamline-master/streamline-master/.dev/fabric/intermediary-1.21.11.jar:/home/runner/work/streamline-master/streamline-master/.dev/fabric/fabric-loader-0.19.3.jar:/home/runner/work/streamline-master/streamline-master/.dev/1.21.11/client.jar)
[11:36:03] [Download-2/INFO]: Could not authorize you against Realms server: java.lang.RuntimeException: Failed to parse into SignedJWT: 0
[11:36:03] [Download-2/ERROR]: Failed to fetch Realms feature flags
net.minecraft.class_4355: Realms authentication error with message 'java.lang.RuntimeException: Failed to parse into SignedJWT: 0'
[ALSOFT] (EE) Could not query RTKit: No such file or directory (2)
```

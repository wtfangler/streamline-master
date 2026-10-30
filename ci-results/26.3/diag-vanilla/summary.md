# Client run: 1.6.3+26.3

**PASS** — exit 0 after 32 s

Software rendering under Xvfb (Mesa llvmpipe): this proves the pack starts and loads a world,
and shows the screens. Its frame rate is not a benchmark.

```
[12:19:23] [main/INFO]: Loading 5 mods:
```

## Metrics

| metric | value |
| --- | --- |
| heap_after_gc_mb | 343.12 |
| startup_s | 12.23 |
| world_ready_s | 18.18 |

## Crashes

none

## Harness

```
[12:19:30] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] tick 1: overlay net.minecraft.client.gui.screens.LoadingOverlay / screen net.minecraft.client.gui.screens.GenericMessageScreen
[12:19:35] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] tick 47: screen net.minecraft.client.gui.screens.LevelLoadingScreen
[12:19:35] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] metric startup_s 12.23
[12:19:39] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] tick 145: screen net.minecraft.client.gui.screens.LevelLoadingScreen / in world
[12:19:40] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] tick 174: screen none / in world
[12:19:40] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] metric world_ready_s 18.18
[12:19:49] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] fps 4 (software rendering in CI, not a benchmark)
[12:19:49] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] metric heap_after_gc_mb 343.12
[12:19:50] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] tick 365: screen net.minecraft.client.gui.screens.GenericMessageScreen / in world
[12:19:52] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] finished
```

## Errors and warnings worth reading (24)

```
[12:19:28] [Render thread/ERROR]: Failed to create backend OpenGL
com.mojang.renderpearl.api.device.BackendCreationException: Failed to create window for OpenGL context: Couldn't find matching GLX visual
[12:19:28] [Download-2/ERROR]: Failed to fetch user properties
com.mojang.authlib.exceptions.InvalidCredentialsException: Status: 401
	at knot//com.mojang.authlib.exceptions.MinecraftClientHttpException.toAuthenticationException(MinecraftClientHttpException.java:70)
Caused by: MinecraftClientHttpException[type=HTTP_ERROR, status=401, response=ErrorResponse[path=/player/attributes, error=null, errorMessage=null, details=null]]
	at knot//com.mojang.authlib.minecraft.client.MinecraftClient.buildHttpException(MinecraftClient.java:170)
[12:19:28] [Render thread/ERROR]: Failed to open pack /home/runner/work/streamline-master/streamline-master/.dev/26.3/assets/objects/3d/3d50584e5111fa2a9d28ab07a5383f9e577ab63e
java.nio.file.NoSuchFileException: /home/runner/work/streamline-master/streamline-master/.dev/26.3/assets/objects/3d/3d50584e5111fa2a9d28ab07a5383f9e577ab63e
	at java.base/sun.nio.fs.UnixException.translateToIOException(UnixException.java:92)
	at java.base/sun.nio.fs.UnixException.rethrowAsIOException(UnixException.java:106)
	at java.base/sun.nio.fs.UnixException.rethrowAsIOException(UnixException.java:111)
[12:19:28] [Render thread/ERROR]: Failed to open pack /home/runner/work/streamline-master/streamline-master/.dev/26.3/assets/objects/13/13ab19f0b4dfe3571f8247561f08ea5d98b0dcfa
java.nio.file.NoSuchFileException: /home/runner/work/streamline-master/streamline-master/.dev/26.3/assets/objects/13/13ab19f0b4dfe3571f8247561f08ea5d98b0dcfa
	at java.base/sun.nio.fs.UnixException.translateToIOException(UnixException.java:92)
	at java.base/sun.nio.fs.UnixException.rethrowAsIOException(UnixException.java:106)
	at java.base/sun.nio.fs.UnixException.rethrowAsIOException(UnixException.java:111)
[12:19:29] [Render thread/ERROR]: Error while loading the narrator
com.mojang.text2speech.Narrator$InitializeException: Failed to load library flite
	Suppressed: java.io.IOException: Native library (linux-x86-64/libflite.so) not found in resource path (/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/lz4-java-1.10.1.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/azure-json-1.4.0.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/oshi-core-6.9.0.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/gson-2.14.0.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/failureaccess-1.0.3.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/guava-33.6.0-jre.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/icu4j-78.3.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/msal4j-1.24.1.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/authlib-10.0.77.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/blocklist-1.0.10.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/brigadier-1.3.11.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/datafixerupper-10.0.21.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/jtracy-1.14.38.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/jtracy-1.14.38-natives-linux.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/logging-1.7.12.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/patchy-2.2.10.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/text2speech-1.19.12.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/commons-codec-1.22.0.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/commons-io-2.20.0.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/netty-buffer-4.2.16.Final.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/netty-codec-base-4.2.16.Final.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/netty-codec-compression-4.2.16.Final.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/netty-codec-http-4.2.16.Final.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/netty-common-4.2.16.Final.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/netty-handler-4.2.16.Final.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/netty-resolver-4.2.16.Final.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/netty-transport-classes-epoll-4.2.16.Final.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/netty-transport-classes-kqueue-4.2.16.Final.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/netty-transport-native-epoll-4.2.16.Final-linux-aarch_64.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/netty-transport-native-epoll-4.2.16.Final-linux-x86_64.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/netty-transport-native-unix-common-4.2.16.Final.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/netty-transport-4.2.16.Final.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/fastutil-8.5.18.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/jna-platform-5.17.0.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/jna-5.17.0.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/jopt-simple-5.0.4.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/commons-compress-1.28.0.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/commons-lang3-3.20.0.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/log4j-api-2.26.0.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/log4j-core-2.26.0.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/log4j-slf4j2-impl-2.26.0.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/jorbis-0.0.17.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/joml-1.10.9.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/jspecify-1.0.0.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/lwjgl-freetype-3.4.3.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/lwjgl-freetype-3.4.3-natives-linux.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/lwjgl-jemalloc-3.4.3.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/lwjgl-jemalloc-3.4.3-natives-linux.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/lwjgl-openal-3.4.3.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/lwjgl-openal-3.4.3-natives-linux.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/lwjgl-opengl-3.4.3.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/lwjgl-opengl-3.4.3-natives-linux.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/lwjgl-sdl-3.4.3.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/lwjgl-sdl-3.4.3-natives-linux.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/lwjgl-shaderc-3.4.3.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/lwjgl-shaderc-3.4.3-natives-linux.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/lwjgl-spvc-3.4.3.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/lwjgl-spvc-3.4.3-natives-linux.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/lwjgl-stb-3.4.3.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/lwjgl-stb-3.4.3-natives-linux.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/lwjgl-vma-3.4.3.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/lwjgl-vma-3.4.3-natives-linux.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/lwjgl-vulkan-3.4.3.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/lwjgl-3.4.3.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/lwjgl-3.4.3-natives-linux.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/libs/slf4j-api-2.0.17.jar:/home/runner/work/streamline-master/streamline-master/.dev/fabric/asm-9.10.1.jar:/home/runner/work/streamline-master/streamline-master/.dev/fabric/asm-analysis-9.10.1.jar:/home/runner/work/streamline-master/streamline-master/.dev/fabric/asm-commons-9.10.1.jar:/home/runner/work/streamline-master/streamline-master/.dev/fabric/asm-tree-9.10.1.jar:/home/runner/work/streamline-master/streamline-master/.dev/fabric/asm-util-9.10.1.jar:/home/runner/work/streamline-master/streamline-master/.dev/fabric/sponge-mixin-0.17.4+mixin.0.8.7.jar:/home/runner/work/streamline-master/streamline-master/.dev/fabric/fabric-loader-0.19.5.jar:/home/runner/work/streamline-master/streamline-master/.dev/26.3/client.jar)
[12:19:29] [Download-2/INFO]: Could not authorize you against Realms server: java.lang.RuntimeException: Failed to parse into SignedJWT: 0
[12:19:29] [Download-2/ERROR]: Failed to fetch Realms feature flags
com.mojang.realmsclient.exception.RealmsServiceException: Realms authentication error with message 'java.lang.RuntimeException: Failed to parse into SignedJWT: 0'
[ALSOFT] (EE) Could not query RTKit: No such file or directory (2)
```

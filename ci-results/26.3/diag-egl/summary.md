# Client run: 1.6.3+26.3

**PASS** — exit 0 after 37 s

Software rendering under Xvfb (Mesa llvmpipe): this proves the pack starts and loads a world,
and shows the screens. Its frame rate is not a benchmark.

```
[12:20:05] [main/INFO]: Loading 138 mods:
```

## Metrics

| metric | value |
| --- | --- |
| heap_after_gc_mb | 326.60 |
| world_ready_s | 25.95 |

## Crashes

none

## Harness

```
[12:20:22] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] tick 1: screen net.minecraft.client.gui.screens.LevelLoadingScreen
[12:20:25] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] tick 69: screen net.minecraft.client.gui.screens.LevelLoadingScreen / in world
[12:20:30] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] tick 148: screen none / in world
[12:20:30] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] metric world_ready_s 25.95
[12:20:36] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] fps 7 (software rendering in CI, not a benchmark)
[12:20:36] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] metric heap_after_gc_mb 326.60
[12:20:37] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] tick 289: screen net.minecraft.client.gui.screens.GenericMessageScreen / in world
[12:20:39] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] finished
```

## Errors and warnings worth reading (27)

```
[12:20:06] [main/WARN]: Error loading class: dev/emi/emi/screen/StackBatcher (java.lang.ClassNotFoundException: dev/emi/emi/screen/StackBatcher)
[12:20:06] [main/WARN]: Could not find any graphics adapters! Probably the device is not on a bus we can probe, or there are no devices supporting 3D acceleration.
[12:20:13] [Download-2/ERROR]: Failed to fetch user properties
com.mojang.authlib.exceptions.InvalidCredentialsException: Status: 401
	at knot//com.mojang.authlib.exceptions.MinecraftClientHttpException.toAuthenticationException(MinecraftClientHttpException.java:70)
Caused by: MinecraftClientHttpException[type=HTTP_ERROR, status=401, response=ErrorResponse[path=/player/attributes, error=null, errorMessage=null, details=null]]
	at knot//com.mojang.authlib.minecraft.client.MinecraftClient.buildHttpException(MinecraftClient.java:170)
[ALSOFT] (EE) Could not query RTKit: No such file or directory (2)
[12:20:15] [Render thread/ERROR]: Failed to open pack /home/runner/work/streamline-master/streamline-master/.dev/26.3/assets/objects/3d/3d50584e5111fa2a9d28ab07a5383f9e577ab63e
java.nio.file.NoSuchFileException: /home/runner/work/streamline-master/streamline-master/.dev/26.3/assets/objects/3d/3d50584e5111fa2a9d28ab07a5383f9e577ab63e
	at java.base/sun.nio.fs.UnixException.translateToIOException(UnixException.java:92)
	at java.base/sun.nio.fs.UnixException.rethrowAsIOException(UnixException.java:106)
	at java.base/sun.nio.fs.UnixException.rethrowAsIOException(UnixException.java:111)
[12:20:15] [Render thread/ERROR]: Failed to open pack /home/runner/work/streamline-master/streamline-master/.dev/26.3/assets/objects/13/13ab19f0b4dfe3571f8247561f08ea5d98b0dcfa
java.nio.file.NoSuchFileException: /home/runner/work/streamline-master/streamline-master/.dev/26.3/assets/objects/13/13ab19f0b4dfe3571f8247561f08ea5d98b0dcfa
	at java.base/sun.nio.fs.UnixException.translateToIOException(UnixException.java:92)
	at java.base/sun.nio.fs.UnixException.rethrowAsIOException(UnixException.java:106)
	at java.base/sun.nio.fs.UnixException.rethrowAsIOException(UnixException.java:111)
[12:20:16] [Render thread/WARN]: Failed to initialize Linux Narrator. Make sure you have libflite installed!
[12:20:16] [Download-2/INFO]: Could not authorize you against Realms server: java.lang.RuntimeException: Failed to parse into SignedJWT: 0
[12:20:16] [Download-2/ERROR]: Failed to fetch Realms feature flags
com.mojang.realmsclient.exception.RealmsServiceException: Realms authentication error with message 'java.lang.RuntimeException: Failed to parse into SignedJWT: 0'
[12:20:16] [Download-3/INFO]: Could not authorize you against Realms server: java.lang.RuntimeException: Failed to parse into SignedJWT: 0
[12:20:16] [Download-3/ERROR]: Couldn't connect to realms
com.mojang.realmsclient.exception.RealmsServiceException: Realms authentication error with message 'java.lang.RuntimeException: Failed to parse into SignedJWT: 0'
[ALSOFT] (EE) Could not query RTKit: No such file or directory (2)
[12:20:23] [Worker-ResourceReload-1/INFO]: Force-loading class net.minecraft.server.ChainedJsonException
```

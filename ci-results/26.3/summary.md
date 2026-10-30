# Client run: 1.6.3+26.3

**PASS** — exit 0 after 47 s

Software rendering under Xvfb (Mesa llvmpipe): this proves the pack starts and loads a world,
and shows the screens. Its frame rate is not a benchmark.

```
[12:23:46] [main/INFO]: Loading 138 mods:
```

## Metrics

| metric | value |
| --- | --- |
| heap_after_gc_mb | 313.22 |
| world_ready_s | 36.96 |

## Crashes

none

## Harness

```
[12:24:11] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] tick 1: screen net.minecraft.client.gui.screens.LevelLoadingScreen
[12:24:11] [IO-Worker-1/INFO]: [STDOUT]: [SLM-HARNESS] saved slm_2_world_2_LevelLoadingScreen
[12:24:11] [IO-Worker-3/INFO]: [STDOUT]: [SLM-HARNESS] saved slm_2_world_1_LevelLoadingScreen
[12:24:11] [IO-Worker-4/INFO]: [STDOUT]: [SLM-HARNESS] saved slm_2_world_4_LevelLoadingScreen
[12:24:11] [IO-Worker-2/INFO]: [STDOUT]: [SLM-HARNESS] saved slm_2_world_3_LevelLoadingScreen
[12:24:15] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] tick 101: screen net.minecraft.client.gui.screens.LevelLoadingScreen / in world
[12:24:22] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] tick 204: screen none / in world
[12:24:22] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] metric world_ready_s 36.96
[12:24:26] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] fps 5 (software rendering in CI, not a benchmark)
[12:24:26] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] metric heap_after_gc_mb 313.22
[12:24:27] [IO-Worker-3/INFO]: [STDOUT]: [SLM-HARNESS] saved slm_3_ingame
[12:24:27] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] tick 321: screen net.minecraft.client.gui.screens.GenericMessageScreen / in world
[12:24:28] [IO-Worker-3/INFO]: [STDOUT]: [SLM-HARNESS] saved slm_4_saving
[12:24:29] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] finished
```

## Errors and warnings worth reading (27)

```
[12:23:49] [main/WARN]: Error loading class: dev/emi/emi/screen/StackBatcher (java.lang.ClassNotFoundException: dev/emi/emi/screen/StackBatcher)
[12:23:49] [main/WARN]: Could not find any graphics adapters! Probably the device is not on a bus we can probe, or there are no devices supporting 3D acceleration.
[12:23:57] [Download-2/ERROR]: Failed to fetch user properties
com.mojang.authlib.exceptions.InvalidCredentialsException: Status: 401
	at knot//com.mojang.authlib.exceptions.MinecraftClientHttpException.toAuthenticationException(MinecraftClientHttpException.java:70)
Caused by: MinecraftClientHttpException[type=HTTP_ERROR, status=401, response=ErrorResponse[path=/player/attributes, error=null, errorMessage=null, details=null]]
	at knot//com.mojang.authlib.minecraft.client.MinecraftClient.buildHttpException(MinecraftClient.java:170)
[ALSOFT] (EE) Could not query RTKit: No such file or directory (2)
[12:24:00] [Render thread/ERROR]: Failed to open pack /home/runner/work/streamline-master/streamline-master/.dev/26.3/assets/objects/3d/3d50584e5111fa2a9d28ab07a5383f9e577ab63e
java.nio.file.NoSuchFileException: /home/runner/work/streamline-master/streamline-master/.dev/26.3/assets/objects/3d/3d50584e5111fa2a9d28ab07a5383f9e577ab63e
	at java.base/sun.nio.fs.UnixException.translateToIOException(UnixException.java:92)
	at java.base/sun.nio.fs.UnixException.rethrowAsIOException(UnixException.java:106)
	at java.base/sun.nio.fs.UnixException.rethrowAsIOException(UnixException.java:111)
[12:24:00] [Render thread/ERROR]: Failed to open pack /home/runner/work/streamline-master/streamline-master/.dev/26.3/assets/objects/13/13ab19f0b4dfe3571f8247561f08ea5d98b0dcfa
java.nio.file.NoSuchFileException: /home/runner/work/streamline-master/streamline-master/.dev/26.3/assets/objects/13/13ab19f0b4dfe3571f8247561f08ea5d98b0dcfa
	at java.base/sun.nio.fs.UnixException.translateToIOException(UnixException.java:92)
	at java.base/sun.nio.fs.UnixException.rethrowAsIOException(UnixException.java:106)
	at java.base/sun.nio.fs.UnixException.rethrowAsIOException(UnixException.java:111)
[12:24:01] [Download-2/INFO]: Could not authorize you against Realms server: java.lang.RuntimeException: Failed to parse into SignedJWT: 0
[12:24:01] [Download-2/ERROR]: Failed to fetch Realms feature flags
com.mojang.realmsclient.exception.RealmsServiceException: Realms authentication error with message 'java.lang.RuntimeException: Failed to parse into SignedJWT: 0'
[12:24:02] [Render thread/WARN]: Failed to initialize Linux Narrator. Make sure you have libflite installed!
[12:24:02] [Download-2/INFO]: Could not authorize you against Realms server: java.lang.RuntimeException: Failed to parse into SignedJWT: 0
[12:24:02] [Download-2/ERROR]: Couldn't connect to realms
com.mojang.realmsclient.exception.RealmsServiceException: Realms authentication error with message 'java.lang.RuntimeException: Failed to parse into SignedJWT: 0'
[ALSOFT] (EE) Could not query RTKit: No such file or directory (2)
[12:24:11] [Worker-ResourceReload-2/INFO]: Force-loading class net.minecraft.server.ChainedJsonException
```

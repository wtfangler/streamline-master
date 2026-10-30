# Client run: 1.5.2+26.2

**PASS** — exit 0 after 51 s

Software rendering under Xvfb (Mesa llvmpipe): this proves the pack starts and loads a world,
and shows the screens. Its frame rate is not a benchmark.

```
[12:23:55] [main/INFO]: Loading 124 mods:
```

## Metrics

| metric | value |
| --- | --- |
| heap_after_gc_mb | 308.50 |
| startup_s | 32.48 |
| world_ready_s | 37.92 |

## Crashes

none

## Harness

```
[12:24:17] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] tick 1: overlay net.minecraft.client.gui.screens.LoadingOverlay / screen net.minecraft.client.gui.screens.LevelLoadingScreen
[12:24:17] [IO-Worker-1/INFO]: [STDOUT]: [SLM-HARNESS] saved slm_1_startup_1
[12:24:17] [IO-Worker-3/INFO]: [STDOUT]: [SLM-HARNESS] saved slm_1_startup_2
[12:24:18] [IO-Worker-2/INFO]: [STDOUT]: [SLM-HARNESS] saved slm_1_startup_3
[12:24:26] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] tick 206: screen net.minecraft.client.gui.screens.LevelLoadingScreen
[12:24:26] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] metric startup_s 32.48
[12:24:26] [IO-Worker-3/INFO]: [STDOUT]: [SLM-HARNESS] saved slm_2_world_1_LevelLoadingScreen
[12:24:26] [IO-Worker-3/INFO]: [STDOUT]: [SLM-HARNESS] saved slm_2_world_2_LevelLoadingScreen
[12:24:27] [IO-Worker-3/INFO]: [STDOUT]: [SLM-HARNESS] saved slm_2_world_3_LevelLoadingScreen
[12:24:27] [IO-Worker-3/INFO]: [STDOUT]: [SLM-HARNESS] saved slm_2_world_4_LevelLoadingScreen
[12:24:30] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] tick 261: screen net.minecraft.client.gui.screens.LevelLoadingScreen / in world
[12:24:31] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] tick 296: screen none / in world
[12:24:31] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] metric world_ready_s 37.92
[12:24:40] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] fps 6 (software rendering in CI, not a benchmark)
[12:24:40] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] metric heap_after_gc_mb 308.50
[12:24:40] [IO-Worker-3/INFO]: [STDOUT]: [SLM-HARNESS] saved slm_3_ingame
[12:24:41] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] tick 481: screen net.minecraft.client.gui.screens.GenericMessageScreen / in world
[12:24:42] [IO-Worker-8/INFO]: [STDOUT]: [SLM-HARNESS] saved slm_4_saving
[12:24:42] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] finished
```

## Errors and warnings worth reading (29)

```
[12:23:57] [main/WARN]: Error loading class: dev/emi/emi/screen/StackBatcher (java.lang.ClassNotFoundException: dev/emi/emi/screen/StackBatcher)
[12:23:57] [main/WARN]: Could not find any graphics adapters! Probably the device is not on a bus we can probe, or there are no devices supporting 3D acceleration.
[12:24:05] [Download-2/ERROR]: Failed to fetch user properties
com.mojang.authlib.exceptions.InvalidCredentialsException: Status: 401
	at knot//com.mojang.authlib.exceptions.MinecraftClientHttpException.toAuthenticationException(MinecraftClientHttpException.java:70)
Caused by: MinecraftClientHttpException[type=HTTP_ERROR, status=401, response=ErrorResponse[path=/player/attributes, error=null, errorMessage=null, details=null]]
	at knot//com.mojang.authlib.minecraft.client.MinecraftClient.buildHttpException(MinecraftClient.java:170)
[12:24:08] [Render thread/ERROR]: Failed to open pack /home/runner/work/streamline-master/streamline-master/.dev/26.2/assets/objects/a6/a69c478840bda10432420c9cd57469320cf33a3b
java.nio.file.NoSuchFileException: /home/runner/work/streamline-master/streamline-master/.dev/26.2/assets/objects/a6/a69c478840bda10432420c9cd57469320cf33a3b
	at java.base/sun.nio.fs.UnixException.translateToIOException(UnixException.java:92)
	at java.base/sun.nio.fs.UnixException.rethrowAsIOException(UnixException.java:106)
	at java.base/sun.nio.fs.UnixException.rethrowAsIOException(UnixException.java:111)
[12:24:08] [Render thread/ERROR]: Failed to open pack /home/runner/work/streamline-master/streamline-master/.dev/26.2/assets/objects/bd/bde50ccdd1e00729f4d187c8ff25ebed357a761a
java.nio.file.NoSuchFileException: /home/runner/work/streamline-master/streamline-master/.dev/26.2/assets/objects/bd/bde50ccdd1e00729f4d187c8ff25ebed357a761a
	at java.base/sun.nio.fs.UnixException.translateToIOException(UnixException.java:92)
	at java.base/sun.nio.fs.UnixException.rethrowAsIOException(UnixException.java:106)
	at java.base/sun.nio.fs.UnixException.rethrowAsIOException(UnixException.java:111)
[12:24:09] [Download-1/INFO]: Could not authorize you against Realms server: java.lang.RuntimeException: Failed to parse into SignedJWT: 0
[12:24:09] [Download-1/ERROR]: Failed to fetch Realms feature flags
com.mojang.realmsclient.exception.RealmsServiceException: Realms authentication error with message 'java.lang.RuntimeException: Failed to parse into SignedJWT: 0'
[12:24:09] [Render thread/WARN]: Failed to initialize Linux Narrator. Make sure you have libflite installed!
[12:24:09] [Download-1/INFO]: Could not authorize you against Realms server: java.lang.RuntimeException: Failed to parse into SignedJWT: 0
[12:24:09] [Download-1/ERROR]: Couldn't connect to realms
com.mojang.realmsclient.exception.RealmsServiceException: Realms authentication error with message 'java.lang.RuntimeException: Failed to parse into SignedJWT: 0'
[ALSOFT] (EE) Could not query RTKit: No such file or directory (2)
[12:24:17] [Worker-ResourceReload-0/INFO]: Force-loading class net.minecraft.server.ChainedJsonException
[12:24:29] [Download-1/ERROR]: Failed to retrieve profile key pair
MinecraftClientHttpException[type=HTTP_ERROR, status=401, response=ErrorResponse[path=/player/certificates, error=null, errorMessage=null, details=null]]
	at knot//com.mojang.authlib.minecraft.client.MinecraftClient.buildHttpException(MinecraftClient.java:170)
```

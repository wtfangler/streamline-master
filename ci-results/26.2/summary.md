# Client run: 1.5.2+26.2

**PASS** — exit 0 after 49 s

Software rendering under Xvfb (Mesa llvmpipe): this proves the pack starts and loads a world,
and shows the screens. Its frame rate is not a benchmark.

```
[12:18:04] [main/INFO]: Loading 124 mods:
```

## Metrics

| metric | value |
| --- | --- |
| heap_after_gc_mb | 310.84 |
| startup_s | 31.01 |
| world_ready_s | 35.52 |

## Crashes

none

## Harness

```
[12:18:24] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] tick 1: overlay net.minecraft.client.gui.screens.LoadingOverlay / screen net.minecraft.client.gui.screens.LevelLoadingScreen
[12:18:25] [IO-Worker-1/INFO]: [STDOUT]: [SLM-HARNESS] saved slm_1_startup_1
[12:18:25] [IO-Worker-3/INFO]: [STDOUT]: [SLM-HARNESS] saved slm_1_startup_2
[12:18:25] [IO-Worker-4/INFO]: [STDOUT]: [SLM-HARNESS] saved slm_1_startup_3
[12:18:34] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] tick 209: screen net.minecraft.client.gui.screens.LevelLoadingScreen
[12:18:34] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] metric startup_s 31.01
[12:18:34] [IO-Worker-2/INFO]: [STDOUT]: [SLM-HARNESS] saved slm_2_world_1_LevelLoadingScreen
[12:18:34] [IO-Worker-2/INFO]: [STDOUT]: [SLM-HARNESS] saved slm_2_world_2_LevelLoadingScreen
[12:18:34] [IO-Worker-2/INFO]: [STDOUT]: [SLM-HARNESS] saved slm_2_world_3_LevelLoadingScreen
[12:18:35] [IO-Worker-1/INFO]: [STDOUT]: [SLM-HARNESS] saved slm_2_world_4_LevelLoadingScreen
[12:18:36] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] tick 246: screen net.minecraft.client.gui.screens.LevelLoadingScreen / in world
[12:18:38] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] tick 284: screen none / in world
[12:18:38] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] metric world_ready_s 35.52
[12:18:46] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] fps 6 (software rendering in CI, not a benchmark)
[12:18:46] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] metric heap_after_gc_mb 310.84
[12:18:47] [IO-Worker-2/INFO]: [STDOUT]: [SLM-HARNESS] saved slm_3_ingame
[12:18:47] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] tick 466: screen net.minecraft.client.gui.screens.GenericMessageScreen / in world
[12:18:48] [IO-Worker-6/INFO]: [STDOUT]: [SLM-HARNESS] saved slm_4_saving
[12:18:49] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] finished
```

## Errors and warnings worth reading (29)

```
[12:18:06] [main/WARN]: Error loading class: dev/emi/emi/screen/StackBatcher (java.lang.ClassNotFoundException: dev/emi/emi/screen/StackBatcher)
[12:18:06] [main/WARN]: Could not find any graphics adapters! Probably the device is not on a bus we can probe, or there are no devices supporting 3D acceleration.
[12:18:14] [Download-2/ERROR]: Failed to fetch user properties
com.mojang.authlib.exceptions.InvalidCredentialsException: Status: 401
	at knot//com.mojang.authlib.exceptions.MinecraftClientHttpException.toAuthenticationException(MinecraftClientHttpException.java:70)
Caused by: MinecraftClientHttpException[type=HTTP_ERROR, status=401, response=ErrorResponse[path=/player/attributes, error=null, errorMessage=null, details=null]]
	at knot//com.mojang.authlib.minecraft.client.MinecraftClient.buildHttpException(MinecraftClient.java:170)
[12:18:16] [Render thread/ERROR]: Failed to open pack /home/runner/work/streamline-master/streamline-master/.dev/26.2/assets/objects/a6/a69c478840bda10432420c9cd57469320cf33a3b
java.nio.file.NoSuchFileException: /home/runner/work/streamline-master/streamline-master/.dev/26.2/assets/objects/a6/a69c478840bda10432420c9cd57469320cf33a3b
	at java.base/sun.nio.fs.UnixException.translateToIOException(UnixException.java:92)
	at java.base/sun.nio.fs.UnixException.rethrowAsIOException(UnixException.java:106)
	at java.base/sun.nio.fs.UnixException.rethrowAsIOException(UnixException.java:111)
[12:18:16] [Render thread/ERROR]: Failed to open pack /home/runner/work/streamline-master/streamline-master/.dev/26.2/assets/objects/bd/bde50ccdd1e00729f4d187c8ff25ebed357a761a
java.nio.file.NoSuchFileException: /home/runner/work/streamline-master/streamline-master/.dev/26.2/assets/objects/bd/bde50ccdd1e00729f4d187c8ff25ebed357a761a
	at java.base/sun.nio.fs.UnixException.translateToIOException(UnixException.java:92)
	at java.base/sun.nio.fs.UnixException.rethrowAsIOException(UnixException.java:106)
	at java.base/sun.nio.fs.UnixException.rethrowAsIOException(UnixException.java:111)
[12:18:18] [Render thread/WARN]: Failed to initialize Linux Narrator. Make sure you have libflite installed!
[12:18:18] [Download-1/INFO]: Could not authorize you against Realms server: java.lang.RuntimeException: Failed to parse into SignedJWT: 0
[12:18:18] [Download-1/ERROR]: Failed to fetch Realms feature flags
com.mojang.realmsclient.exception.RealmsServiceException: Realms authentication error with message 'java.lang.RuntimeException: Failed to parse into SignedJWT: 0'
[12:18:18] [Download-2/INFO]: Could not authorize you against Realms server: java.lang.RuntimeException: Failed to parse into SignedJWT: 0
[12:18:18] [Download-2/ERROR]: Couldn't connect to realms
com.mojang.realmsclient.exception.RealmsServiceException: Realms authentication error with message 'java.lang.RuntimeException: Failed to parse into SignedJWT: 0'
[ALSOFT] (EE) Could not query RTKit: No such file or directory (2)
[12:18:25] [Worker-ResourceReload-1/INFO]: Force-loading class net.minecraft.server.ChainedJsonException
[12:18:36] [Download-2/ERROR]: Failed to retrieve profile key pair
MinecraftClientHttpException[type=HTTP_ERROR, status=401, response=ErrorResponse[path=/player/certificates, error=null, errorMessage=null, details=null]]
	at knot//com.mojang.authlib.minecraft.client.MinecraftClient.buildHttpException(MinecraftClient.java:170)
```

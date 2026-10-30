# Client run: 1.5.2+26.2

**PASS** — exit 0 after 52 s

Software rendering under Xvfb (Mesa llvmpipe): this proves the pack starts and loads a world,
and shows the screens. Its frame rate is not a benchmark.

```
[11:33:29] [main/INFO]: Loading 124 mods:
```

## Metrics

| metric | value |
| --- | --- |
| heap_after_gc_mb | 309.89 |
| startup_s | 32.75 |
| world_ready_s | 38.79 |

## Crashes

none

## Harness

```
[11:33:51] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] tick 1: overlay net.minecraft.client.gui.screens.LoadingOverlay / screen net.minecraft.client.gui.screens.LevelLoadingScreen
[11:33:52] [IO-Worker-4/INFO]: [STDOUT]: [SLM-HARNESS] saved slm_1_startup_1
[11:33:52] [IO-Worker-2/INFO]: [STDOUT]: [SLM-HARNESS] saved slm_1_startup_2
[11:33:52] [IO-Worker-3/INFO]: [STDOUT]: [SLM-HARNESS] saved slm_1_startup_3
[11:34:00] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] tick 196: screen net.minecraft.client.gui.screens.LevelLoadingScreen
[11:34:00] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] metric startup_s 32.75
[11:34:01] [IO-Worker-4/INFO]: [STDOUT]: [SLM-HARNESS] saved slm_2_world_1_LevelLoadingScreen
[11:34:01] [IO-Worker-6/INFO]: [STDOUT]: [SLM-HARNESS] saved slm_2_world_2_LevelLoadingScreen
[11:34:01] [IO-Worker-4/INFO]: [STDOUT]: [SLM-HARNESS] saved slm_2_world_3_LevelLoadingScreen
[11:34:01] [IO-Worker-4/INFO]: [STDOUT]: [SLM-HARNESS] saved slm_2_world_4_LevelLoadingScreen
[11:34:04] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] tick 260: screen net.minecraft.client.gui.screens.LevelLoadingScreen / in world
[11:34:06] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] tick 299: screen none / in world
[11:34:06] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] metric world_ready_s 38.79
[11:34:14] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] fps 6 (software rendering in CI, not a benchmark)
[11:34:15] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] metric heap_after_gc_mb 309.89
[11:34:15] [IO-Worker-4/INFO]: [STDOUT]: [SLM-HARNESS] saved slm_3_ingame
[11:34:16] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] tick 480: screen net.minecraft.client.gui.screens.GenericMessageScreen / in world
[11:34:17] [IO-Worker-6/INFO]: [STDOUT]: [SLM-HARNESS] saved slm_4_saving
[11:34:17] [Render thread/INFO]: [STDOUT]: [SLM-HARNESS] finished
```

## Errors and warnings worth reading (29)

```
[11:33:31] [main/WARN]: Error loading class: dev/emi/emi/screen/StackBatcher (java.lang.ClassNotFoundException: dev/emi/emi/screen/StackBatcher)
[11:33:31] [main/WARN]: Could not find any graphics adapters! Probably the device is not on a bus we can probe, or there are no devices supporting 3D acceleration.
[11:33:40] [Download-2/ERROR]: Failed to fetch user properties
com.mojang.authlib.exceptions.InvalidCredentialsException: Status: 401
	at knot//com.mojang.authlib.exceptions.MinecraftClientHttpException.toAuthenticationException(MinecraftClientHttpException.java:70)
Caused by: MinecraftClientHttpException[type=HTTP_ERROR, status=401, response=ErrorResponse[path=/player/attributes, error=null, errorMessage=null, details=null]]
	at knot//com.mojang.authlib.minecraft.client.MinecraftClient.buildHttpException(MinecraftClient.java:170)
[11:33:43] [Render thread/ERROR]: Failed to open pack /home/runner/work/streamline-master/streamline-master/.dev/26.2/assets/objects/a6/a69c478840bda10432420c9cd57469320cf33a3b
java.nio.file.NoSuchFileException: /home/runner/work/streamline-master/streamline-master/.dev/26.2/assets/objects/a6/a69c478840bda10432420c9cd57469320cf33a3b
	at java.base/sun.nio.fs.UnixException.translateToIOException(UnixException.java:92)
	at java.base/sun.nio.fs.UnixException.rethrowAsIOException(UnixException.java:106)
	at java.base/sun.nio.fs.UnixException.rethrowAsIOException(UnixException.java:111)
[11:33:43] [Render thread/ERROR]: Failed to open pack /home/runner/work/streamline-master/streamline-master/.dev/26.2/assets/objects/bd/bde50ccdd1e00729f4d187c8ff25ebed357a761a
java.nio.file.NoSuchFileException: /home/runner/work/streamline-master/streamline-master/.dev/26.2/assets/objects/bd/bde50ccdd1e00729f4d187c8ff25ebed357a761a
	at java.base/sun.nio.fs.UnixException.translateToIOException(UnixException.java:92)
	at java.base/sun.nio.fs.UnixException.rethrowAsIOException(UnixException.java:106)
	at java.base/sun.nio.fs.UnixException.rethrowAsIOException(UnixException.java:111)
[11:33:44] [Download-1/INFO]: Could not authorize you against Realms server: java.lang.RuntimeException: Failed to parse into SignedJWT: 0
[11:33:44] [Download-1/ERROR]: Failed to fetch Realms feature flags
com.mojang.realmsclient.exception.RealmsServiceException: Realms authentication error with message 'java.lang.RuntimeException: Failed to parse into SignedJWT: 0'
[11:33:44] [Render thread/WARN]: Failed to initialize Linux Narrator. Make sure you have libflite installed!
[11:33:44] [Download-1/INFO]: Could not authorize you against Realms server: java.lang.RuntimeException: Failed to parse into SignedJWT: 0
[11:33:44] [Download-1/ERROR]: Couldn't connect to realms
com.mojang.realmsclient.exception.RealmsServiceException: Realms authentication error with message 'java.lang.RuntimeException: Failed to parse into SignedJWT: 0'
[ALSOFT] (EE) Could not query RTKit: No such file or directory (2)
[11:33:51] [Worker-ResourceReload-1/INFO]: Force-loading class net.minecraft.server.ChainedJsonException
[11:34:04] [Download-1/ERROR]: Failed to retrieve profile key pair
MinecraftClientHttpException[type=HTTP_ERROR, status=401, response=ErrorResponse[path=/player/certificates, error=null, errorMessage=null, details=null]]
	at knot//com.mojang.authlib.minecraft.client.MinecraftClient.buildHttpException(MinecraftClient.java:170)
```

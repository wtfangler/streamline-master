# Client run: 1.6.3+26.3

**FAIL** — exit -6 after 43 s

Software rendering under Xvfb (Mesa llvmpipe): this proves the pack starts and loads a world,
and shows the screens. Its frame rate is not a benchmark.

```
[12:38:05] [main/INFO]: Loading 137 mods:
```

## Metrics

| metric | value |
| --- | --- |

## Crashes

none

## Harness

```
```

## Errors and warnings worth reading (11)

```
[12:38:08] [main/WARN]: Error loading class: dev/emi/emi/screen/StackBatcher (java.lang.ClassNotFoundException: dev/emi/emi/screen/StackBatcher)
[12:38:08] [main/WARN]: Could not find any graphics adapters! Probably the device is not on a bus we can probe, or there are no devices supporting 3D acceleration.
[12:38:18] [Download-2/ERROR]: Failed to fetch user properties
com.mojang.authlib.exceptions.InvalidCredentialsException: Status: 401
	at knot//com.mojang.authlib.exceptions.MinecraftClientHttpException.toAuthenticationException(MinecraftClientHttpException.java:70)
Caused by: MinecraftClientHttpException[type=HTTP_ERROR, status=401, response=ErrorResponse[path=/player/attributes, error=null, errorMessage=null, details=null]]
	at knot//com.mojang.authlib.minecraft.client.MinecraftClient.buildHttpException(MinecraftClient.java:170)
[ALSOFT] (EE) Could not query RTKit: No such file or directory (2)
[12:38:20] [Render thread/ERROR]: Failed to create backend OpenGL
com.mojang.renderpearl.api.device.BackendCreationException: Failed to create window for OpenGL context: 
FATAL ERROR in native method: [LWJGL] Thread[#43,Render thread,5,main]: No context is current or a function that is not available in the current context was called. The JVM will abort execution.
```

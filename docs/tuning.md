# Tuning

Profil sprzętowy, pod który ustawione są domyślne: HP EliteBook x360, i5-8350U
(4 rdzenie / 8 wątków, 15 W), Intel UHD 620, ekran 1080p.

## Argumenty JVM

Największy pojedynczy lever w całym projekcie, a `.mrpack` go nie przenosi — trzeba
ustawić go w instancji Prism Launchera: Edit Instance → Settings → Java.

Java 21 lub nowsza jest wymagana dla 1.20.5+.

16 GB RAM w laptopie:

```
-Xms1G -Xmx4G -XX:+UnlockExperimentalVMOptions -XX:+UseG1GC -XX:MaxGCPauseMillis=50 -XX:+ParallelRefProcEnabled -XX:G1NewSizePercent=20 -XX:G1MaxNewSizePercent=40 -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=20 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:MaxTenuringThreshold=1 -XX:+PerfDisableSharedMem -XX:-OmitStackTraceInFastThrow
```

8 GB RAM: to samo, ale `-Xmx3G`.

Czego nie robić: nie dawaj `-Xmx8G` ani więcej. Na czterech rdzeniach większa sterta
to dłuższe pauzy GC, czyli dokładnie te przycięcia, które próbujesz wyeliminować.
Nie używaj ZGC ani Shenandoah — obie potrzebują rdzeni, których tu nie ma.

## Sterownik graficzny

Wydajność OpenGL na Intel UHD 620 różni się między wersjami sterownika bardziej niż
między paczkami modów. Zanim zmierzysz cokolwiek, zainstaluj najnowszy sterownik
bezpośrednio od Intela, nie ten z Windows Update ani z HP.

## Ustawienia okna

- Pełny ekran, nie borderless. Chloride ma borderless włączalny — na Intelu zostaw
  wyłączony poza sytuacjami, gdy potrzebujesz szybkiego alt-tab.
- Jeżeli po wszystkim nadal jest za wolno, zejdź z rozdzielczości okna do 1280×720.
  Fill rate jest tu wąskim gardłem i to działa mocniej niż jakikolwiek mod.

## Chloride

Dwie rzeczy do włączenia ręcznie w menu wideo (zakładki Chloride), bo paczka nie wysyła
configu tego moda — nazwa i schemat pliku nie są udokumentowane, a wysłanie zgadywanego
pliku grozi resetem ustawień:

- **Entity Distance Culling** — encje i block entities poza zadanym dystansem przestają
  być renderowane i tickowane. Największy pojedynczy zysk w wioskach i przy farmach.
- **Text Shadows** — wyłączenie cieni fontu. Widoczne tylko wtedy, gdy się o tym wie,
  a przy pełnym HUD i chacie potrafi dać kilka klatek.

Zostaw wyłączone: **Fast Models** (dubluje Better Block Entities) i **Leaves Culling**
(dubluje MoreCulling).

## Powrót do ustawień z 1.5

Domyślne `options.txt` w 2.0 jest jeden do jednego z FO, żeby porównanie miało sens.
Wersja 1.5 szła na cięższych ustawieniach — jeżeli po pomiarze chcesz je z powrotem,
oto one, w kolejności od najdroższej:

| Klucz | 2.0 | 1.5 | Koszt amortyzuje |
|---|---|---|---|
| `renderDistance` | 8 | 12 | MoreCulling, Entity Culling, Chloride, C2ME |
| `renderClouds` / `cloudRange` | "fast" / 32 | "true" / 128 | MoreCulling `cloudCulling` |
| `particles` | 1 | 0 | Particle Core |
| `mipmapLevels` | 2 | 4 | nic — to czysty koszt na iGPU |
| `maxAnisotropyBit` | 0 | 2 | nic — to czysty koszt na iGPU |
| `entityDistanceScaling` | 0.75 | 1.0 | Chloride Entity Distance Culling |
| `entityShadows` | false | true | nic |
| `biomeBlendRadius` | 1 | 2 | nic — koszt przy budowie chunka |

Rób je pojedynczo i mierz po każdej. Trzy ostatnie pozycje nie mają czym się
amortyzować i to od nich zacząłbym rezygnować.

## Opcjonalne obniżenie kosztu

| Zmiana | Co tracisz |
|---|---|
| `maxFps:60` | limit klatek; na 15 W CPU stabilizuje temperaturę i podnosi 1% low |
| `simulationDistance:4` | jeszcze mniejszy promień tickowania niż domyślne 5 |
| `mipmapLevels:0` | ostrzejsze, ale migoczące tekstury w oddali |
| Exordium `maxFps:30` | HUD i ekwipunek odświeżane 30 razy na sekundę zamiast 60 |

`simulationDistance` odciąża wątek serwera zintegrowanego — czyli to, co czuć w grze
ze znajomymi przez Essential, gdzie to Twój laptop jest hostem. Paczka wysyła 5,
czyli mniej niż FO (8); niżej schodź tylko wtedy, gdy nie masz farm w pobliżu.

## Resourcepacki

Paczka wysyła dwa i oba włącza w `options.txt`: **Fast Better Grass** i
**qrafty's Capitalized Font**.

Font to bitmapowy pack 16x, 236 kB — podmienia istniejące tekstury glifów, nie dodaje
nowych. Atlas czcionki ma te same wymiary co w vanilli, liczba draw calli się nie zmienia,
kosztu na klatkę nie ma. Cały narzut to jednorazowe wczytanie przy reloadzie zasobów.

Jedno miejsce, gdzie może się odbić: ImmediatelyFast ma `experimental_sign_text_buffering`
ustawione na `true`, a dokumentacja moda pisze, że ta opcja potrafi sprawiać problemy
z niestandardowymi czcionkami. Jeżeli tekst na tabliczkach zacznie się rozjeżdżać albo
pokazywać nie te znaki, to jest ten przełącznik — `false` w `config/immediatelyfast.json`.
Zostaje na `true`, bo pack jest w tej samej rozdzielczości co vanilla i ryzyko jest niskie,
a opcja realnie oszczędza przy dużej liczbie tabliczek.

`font_atlas_resizing` jest już włączone i to jest właściwe ustawienie pod własne czcionki.
`font_atlas_size: 1024` wystarcza dla 16x; podnoś dopiero przy packu w wyższej rozdzielczości.

Żeby wyłączyć font: usuń wpis `qraftys-capitalized-font` z `manifest.json` i placeholder
`{{resourcepack:qraftys-capitalized-font}}` z `overrides-<mc>/options.txt.tmpl`.

## Mody interfejsu

Smooth Gui, Smooth Scrolling i Smooth Swapping są w manifeście jako `optional`.
Wszystkie trzy działają wyłącznie w ekranach GUI i w HUD-ie — w świecie nie kosztują nic.
Największy z nich ma 96 kB.

Jedyne, co realnie może kosztować, to Smooth Swapping przy shift-klikaniu w podwójnej
skrzyni: każdy animowany przedmiot to osobny render modelu, a to na iGPU nie jest tanie.
`animation_speed: 100` skraca to okno. Gdyby przeszkadzało, `toggle_mod: false`.

Smooth Scrolling ma `RP Compatibility Mode` dla ekranu kreatywnego ustawione na `false`.
Ta opcja istnieje dokładnie pod przerobione tekstury GUI — jeżeli przewijanie zakładek
w kreatywie zacznie się przycinać albo wychodzić poza ramkę, to jest ten przełącznik.

## Recolourful Containers a ImmediatelyFast

Ten resourcepack jest oznaczony na Modrincie kategorią **core-shaders** — modyfikuje
shadery rdzeniowe, żeby przebarwiać GUI. ImmediatelyFast ma na to zabezpieczenie:
`experimental_disable_resource_pack_conflict_handling` decyduje, czy mod ma skanować
resourcepacki pod kątem takich modyfikacji i wyłączać kolidujące optymalizacje.

W Twojej paczce ta opcja była na `true`, czyli skanowanie **wyłączone**. Ustawione
z powrotem na `false`. Kosztuje to część optymalizacji ImmediatelyFast wtedy, kiedy pack
jest włączony — i to jest właściwa cena za GUI, które się renderuje poprawnie.
Jeżeli zdejmiesz Recolourful Containers, możesz wrócić do `true`.

## ModernFix kontra ModernFix-mVUS

W manifeście jest `modernfix-mvus`, nie `modernfix`. To dwa osobne projekty na Modrincie:
oficjalny ModernFix (`nmDcB62a`) kończy buildy fabricowe na 26.1.2, a fork mVUS
(`TjSm1wrD`) ma 26.2 i nowsze. Twoja paczka 1.0.0 i tak używała forka — jar nazywa się
`modernfix-...jar`, więc po nazwie pliku tego nie widać, dopiero po ID projektu.

## Mody rozważone i odrzucone

- **Distant Horizons** — na iGPU przy render distance 8–10 kosztuje więcej, niż daje.
- **Nvidium** — tylko NVIDIA.
- **AsyncParticles** — pokrywa się z Particle Core, renderowanie cząstek po GPU jest
  ryzykowne na sterownikach Intela.
- **ThreadTweak** i **Exordium** — w paczce, ale tylko na 1.21.11; na 26.x nie mają
  buildów. Oznaczone w manifeście jako `optional`, więc build na 26.x je pomija zamiast
  się wywalić.

## C2ME

Tylko na 26.x. Na 1.21.11 każdy build C2ME (release, beta, alpha) wymaga w module
`c2me-opts-natives-math` Javy 22 lub nowszej, a instancja 1.21.11 w aplikacji Modrinth
dostaje Javę 21 — Fabric Loader przerywa start. W manifeście `c2me-fabric` ma
`skipTargets: ["1.21.11"]`. Kto na 1.21.11 ustawi ręcznie runtime Java 22+, może dorzucić
mod z osobna.

Config `c2me.toml` leży w `overrides-26.2/` i `overrides-26.1.2/` (nie w `overrides/`),
z jedną zmianą względem 1.5: `gcFreeChunkSerializer` wraca na `false`. Dokumentacja moda
opisuje tę opcję jako eksperymentalną zmianę sposobu zapisu chunków, wymagającą regularnych
backupów świata. W paczce, którą pobierają obcy ludzie, to nie jest ustawienie, które można
zostawić włączone.

`maxConcurrentChunkLoads = 2` zostaje bez zmian — na czterech rdzeniach throttling
równoległych ładowań realnie zmniejsza przycięcia przy eksploracji.

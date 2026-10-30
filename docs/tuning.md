# Tuning

Profil sprzętowy, pod który ustawione są domyślne: HP EliteBook x360, i5-8350U
(4 rdzenie / 8 wątków, 15 W), Intel UHD 620, ekran 1080p.

## Argumenty JVM

Największy pojedynczy lever w całym projekcie, a `.mrpack` go nie przenosi — trzeba
ustawić go w instancji Prism Launchera: Edit Instance → Settings → Java.

Robi to za Ciebie `tune.cmd` (albo `python tune.py <folder instancji> --gpu`): dobiera
`-Xmx` do RAM-u maszyny według tabeli niżej, wpisuje argumenty G1 do `instance.cfg`
(z kopią `instance.cfg.bak`) i na Windowsie ustawia Javę tej instancji na kartę
„Wysoka wydajność” — ten sam wpis, który robi Ustawienia → Ekran → Grafika. Na laptopie
z dwiema kartami to jest różnica między iGPU a dedykowaną, większa niż cokolwiek w paczce;
na laptopie z jedną kartą (jak UHD 620) nic nie zmienia. Przed uruchomieniem zamknij
Prism — przy wyjściu nadpisuje `instance.cfg`. Aplikacji Modrinth skrypt nie edytuje
(trzyma ustawienia w bazie danych), tylko wypisuje wartości do wklejenia.

Argumenty w `tune.py` są tymi samymi co poniżej, bez `-Xms`/`-Xmx` — Prism podaje
je sam z pól pamięci, a podwójne wpisanie zostawia kolejności argumentów, który wygra.

Java: **25** dla Minecrafta 26.x, **21** dla 1.21.11. Aplikacja Modrinth i Prism dobierają ją same.

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

- Paczka startuje w pełnym ekranie bez trybu wyłącznego (`exclusiveFullscreen:false`,
  domyślne ustawienie gry) i na tym ustawieniu robione były pomiary z CHANGELOG. Tryb
  wyłączny może na Intelu oszczędzić przejście przez kompozytor okien, ale nie był mierzony —
  włącz go w ustawieniach wideo i sprawdź `bench_setup.py`, zanim go zostawisz.
- Chloride (26.2 i starsze) ma swój przełącznik borderless — na Intelu zostaw go
  wyłączonego, chyba że potrzebujesz szybkiego alt-tab.
- Jeżeli po wszystkim nadal jest za wolno, zejdź z rozdzielczości okna do 1280×720.
  Fill rate jest tu wąskim gardłem i to działa mocniej niż jakikolwiek mod.

## Minecraft 26.3

Na 26.3 nie ma Chloride (brak buildu na tę wersję), więc sekcja niżej i przełącznik
borderless z „Ustawień okna” go nie dotyczą. Jego role przejmują inne mody:

- **Entity View Distance** zamiast Entity Distance Culling z Chloride — encje poza
  dystansem nie są renderowane. Paczka nie wysyła configu, działa na domyślnych.
- **Particle Core** (wrócił w 1.6.3) — culling cząstek i tańsze ich renderowanie,
  na domyślnych ustawieniach, tak jak na 26.2.
- **Licznik FPS** jest tylko jeden, z Sodium Extra.

Słabszy sprzęt niż UHD 620: `python tune.py <instancja> --preset potato` obniża
`options.txt` według tabeli „Opcjonalne obniżenie kosztu” niżej (plus zasięg 6, chmury
i cząstki na minimum), z kopią `options.txt.bak`. Działa też dla aplikacji Modrinth.
Ten zestaw nie był mierzony jako całość — zmierz go `bench.py`, zanim uznasz, że pomaga.

## Chloride (26.2, 26.1.2, 1.21.11)

Dwie rzeczy do włączenia ręcznie w menu wideo (zakładki Chloride), bo paczka nie wysyła
configu tego moda — nazwa i schemat pliku nie są udokumentowane, a wysłanie zgadywanego
pliku grozi resetem ustawień:

- **Entity Distance Culling** — encje i block entities poza zadanym dystansem przestają
  być renderowane i tickowane. Największy pojedynczy zysk w wioskach i przy farmach.
- **Text Shadows** — wyłączenie cieni fontu. Widoczne tylko wtedy, gdy się o tym wie,
  a przy pełnym HUD i chacie potrafi dać kilka klatek.

Zostaw wyłączone: **Fast Models** (dubluje Better Block Entities) i **Leaves Culling**
(dubluje MoreCulling).

## Powrót do cięższych ustawień z 1.5

Obecne `options.txt` jest lżejsze niż w wydaniach 1.3 / 1.4 / 1.5 z 28.08.2026 (audyt
w `audit.md`). Jeżeli po pomiarze chcesz któreś z tamtych ustawień z powrotem, oto one,
w kolejności od najdroższego:

| Klucz | teraz | 1.5 | Koszt amortyzuje |
|---|---|---|---|
| `renderDistance` | 8 | 12 | MoreCulling, Entity Culling, Chloride / Entity View Distance |
| `renderClouds` / `cloudRange` | "fast" / 32 | "true" / 128 | MoreCulling `cloudCulling` |
| `particles` | 1 | 0 | Particle Core |
| `mipmapLevels` | 2 | 4 | nic — to czysty koszt na iGPU |
| `maxAnisotropyBit` | 1 | 2 | nic — to czysty koszt na iGPU (1 to minimum gry) |
| `entityDistanceScaling` | 0.75 | 1.0 | Chloride Entity Distance Culling / Entity View Distance |
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
| Exordium `maxFps:30` (26.1.2, 1.21.11) | HUD i ekwipunek odświeżane 30 razy na sekundę zamiast 60 |

`simulationDistance` odciąża wątek serwera zintegrowanego — czyli to, co czuć w grze
ze znajomymi przez Essential, gdzie to Twój laptop jest hostem. Paczka wysyła 5,
czyli mniej niż FO (8); niżej schodź tylko wtedy, gdy nie masz farm w pobliżu.

## Resourcepacki

Paczka wysyła trzy i wszystkie włącza w `options.txt`: **Fast Better Grass**,
**qrafty's Capitalized Font** i **Recolourful Containers Dark** (ten ostatni ma osobną
sekcję niżej, bo dotyka shaderów rdzeniowych).

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
- **ThreadTweak** (tylko 1.21.11) i **Exordium** (26.1.2 i 1.21.11) — w paczce tam, gdzie
  mają buildy; nowsze wersje gry ich nie mają. Oznaczone w manifeście jako `optional`,
  więc build bez nich je pomija zamiast się wywalić.

## C2ME, Very Many Players, ScalableLux

Od 1.6.2 / 1.5.2 / 1.4.2 / 1.3.2 nie ma ich w żadnej paczce. Na 26.3 build z nimi był na
laptopie z UHD 620 o ok. 10% wolniejszy i miał głębsze spadki (szczegóły w CHANGELOG);
na 26.2 kontrolowane A/B dało sprzeczne wyniki, więc tam odpadły dla spójności i dlatego,
że C2ME i VMP są wciąż w wersjach przedpremierowych. W manifeście zostają z `skipTargets`
na wszystkich wersjach — powrót to jedna linijka, ale tylko z pomiarem, który go uzasadni.

Na 1.21.11 C2ME i tak nie dałoby się użyć: moduł `c2me-opts-natives-math` wymaga Javy 22+,
a 1.21.11 działa na Javie 21.

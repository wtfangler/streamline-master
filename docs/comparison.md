# Streamline Master 2.0 — co się zmieniło

Dwa punkty odniesienia: własne wydania 1.3 / 1.4 / 1.5 z 28.08.2026 (audyt w `audit.md`)
oraz Fabulously Optimized 14.0.0-beta.4 (26.2) i 12.2.2 (1.21.11).

## Ustawienia

`options.txt` przestaje być zrzutem prywatnych ustawień. Wysyłane są wyłącznie klucze,
które paczka ma prawo ustawiać: grafika, okno, telemetria, ekrany powitalne. Zero
keybindów, zero głośności, zero czułości myszy, zero FOV i języka. Aktualizacja paczki
nie kasuje już nikomu sterowania.

Wartości graficzne są ustawione jeden do jednego z FO, żeby porównanie miało sens:

| Klucz | SLM 1.5 | SLM 2.0 | FO |
|---|---|---|---|
| `cutoutLeaves` | false | true | true |
| `renderDistance` | 12 | 8 | 8 |
| `mipmapLevels` | 4 | 2 | 2 |
| `maxAnisotropyBit` | 2 | 0 | 0 |
| `biomeBlendRadius` | 2 | 1 | 1 |
| `entityDistanceScaling` | 1.0 | 0.75 | 0.75 |
| `entityShadows` | true | false | false |
| `renderClouds` | "true" | "fast" | "fast" |
| `cloudRange` | 128 | 32 | 32 |
| `particles` | 0 | 1 | 1 |
| `simulationDistance` | 5 | 5 | 8 |

Render distance 8 zamiast 12 to jedyna pozycja, na której obraz jest gorszy niż w 1.5.
Jest tak celowo: dopóki obie paczki nie stoją na tym samym dystansie, pomiar nie mierzy
modów. Po zrobieniu benchmarku podniesienie z powrotem to jedna linijka — `tuning.md`.

## Naprawione configi

| Plik | Było | Jest |
|---|---|---|
| `sodium-options.json` | `use_entity_culling: false` | `true` |
| `moreculling.toml` | `leavesCullingMode = "DEPTH"` | `"CHECK"` |
| `moreculling.toml` | `useCustomItemFrameRenderer = true` | `false` |
| `moreculling.toml` | `itemFrameLODRange = 16` | `128` |
| `moreculling.toml` | `itemFrame3FaceCullingRange = 2.0` | `4.0` |
| `moreculling.toml` | `signTextCulling = true` | `false` |
| `entityculling.json` | `sleepDelay: 153` | wartość domyślna moda |
| `c2me.toml` | `gcFreeChunkSerializer = true` | `false` |
| `threadtweak.json` | `main: 15` | `main: 6`, priorytety przeliczone pod 4C/8T |
| `modernfix-mixins.properties` | `thread_priorities=false` wszędzie | `false` tylko tam, gdzie jest ThreadTweak |
| `modmenu.json` | `count_libraries` i `count_children` na `true` | oba `false` |

Licznik modów w menu głównym pokazywał 130+, bo Mod Menu doliczał biblioteki i moduły
potomne — samo Fabric API to około stu osobnych modułów. Po zmianie liczy tylko mody,
które faktycznie wybrałeś.

Usunięte z overrides: `sodium-fingerprint.json`, `iris-excluded.json`,
`fabric_loader_dependencies.json`, `NoChatReports/*`, `fabric/indigo-renderer.properties`.
Wszystkie pozostałe pliki configu są wysyłane bez komentarzy.

## Mody

Dochodzi 13:

| Mod | Rola |
|---|---|
| Sodium Extra | mgła, cząstki, detale nieba, pogoda, wysokość chmur |
| Chloride | culling encji i block entities po dystansie, fast models, cienie fontu, mgła |
| Particle Core | culling cząstek, tańsze transformacje wierzchołków i lightmapa |
| Better Block Entities | wsadowe renderowanie block entities |
| Sodium Shadowy Path Blocks | oświetlenie ścieżek |
| Continuity | `glass_pane_culling_fix` |
| Packet Fixer | pakiety, NBT, timeouty |
| Fast IP Ping | reverse DNS przy łączeniu po IP |
| Ixeris | buforowane wejście, wątkowe pollowanie zdarzeń |
| FastQuit | powrót do menu w trakcie zapisu świata |
| Remove Reloading Screen | przeładowanie zasobów w tle |
| Main Menu Credits | nazwa i wersja paczki w prawym dolnym rogu |
| Fzzy Config | zależność Particle Core |

Dochodzi też resourcepack **qrafty's Capitalized Font** obok Fast Better Grass.

Wypada 2: `NoChatReports` i `placeholder-api`.

Zostaje wszystko, co już działało: Sodium, Reese's, Iris, Lithium, FerriteCore, ModernFix-mVUS,
BadOptimizations, ScalableLux, C2ME, VMP, Let Me Despawn, Krypton, Entity Culling,
More Culling, ImmediatelyFast, Dynamic FPS, Debugify, Language Reload, Zoomify,
Fast Better Grass, ThreadTweak i Exordium na 1.21.11.

## Stosunek do FO

| | FO 26.2 | SLM 2.0 |
|---|---|---|
| mody | 44 + 3 resourcepacki | 39 |
| ustawienia graficzne | jak wyżej | identyczne |
| culling encji po dystansie | brak | Chloride |
| culling cząstek | brak | Particle Core |
| silnik światła | vanilla | ScalableLux |
| pipeline chunków | vanilla | C2ME |
| wątek serwera zintegrowanego | vanilla | VMP + Let Me Despawn |
| sieć | vanilla | Krypton + Packet Fixer |
| mody bez wpływu na wydajność | 26 | 6 |

FO nie ma ScalableLux, C2ME, VMP, Let Me Despawn, Krypton, BadOptimizations, Chloride,
Particle Core, Packet Fixer ani Fast IP Ping. Ma za to EMF, ETF, Animatica, Polytone,
Skyboxify, OptiGUI, Puzzle, Controlify, Cape Provider, e4mc, Fabrishot i kilka mniejszych
— nic z tego nie zmienia liczby klatek na czystych zasobach vanilla.

## Czego to nie mówi

Nic tu nie zostało zmierzone. Sandbox, w którym paczka powstała, nie ma dostępu ani do
CDN Modrintha, ani do gry. Liczby mają wyjść z `benchmark.md` — i pierwszy pomiar, jaki
warto zrobić, to nie SLM kontra FO, tylko SLM 1.5 kontra SLM 2.0 na tych samych
ustawieniach. To pokaże, ile z różnicy brało się z configów, a ile z listy modów.

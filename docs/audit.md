# Audyt Streamline Master 1.3 / 1.4 / 1.5

Podstawa: trzy pliki `.mrpack` wydane 28.08.2026 (1.21.11, 26.1.2, 26.2).

## Wniosek nadrzędny

Lista modów w 1.5 jest dobra — miejscami lepsza od Fabulously Optimized. Porównanie
na Twoim laptopie przegrywało nie przez mody, tylko przez `options.txt` i kilka
ustawień w configach.

Paczka szła na render distance 12, mipmapach 4, anizotropii, cieniach encji, chmurach
fancy z zasięgiem 128 i wszystkich cząstkach. FO w tym samym czasie szło na render
distance 8 i wszystkim obniżonym. Przy takiej różnicy remis w FPS oznacza, że Twój
stos modów już był szybszy — po prostu nikt tego nie zmierzył przy równych ustawieniach.

## options.txt

Wysyłany plik to zrzut Twoich prywatnych ustawień, nie domyślne paczki. Zawiera
komplet keybindów, głośności, czułość myszy, FOV, język, ustawienia czatu i widoczność
części modelu gracza. Instalacja albo aktualizacja paczki nadpisuje to wszystko u każdego,
kto ją pobierze — łącznie ze sterowaniem.

Porównanie ustawień graficznych z FO:

| Klucz | SLM 1.5 | FO | Efekt |
|---|---|---|---|
| `cutoutLeaves` | false | true | pełne bloki liści zamiast prześwitów |
| `renderDistance` | 12 | 8 | ~2,25× więcej chunków w kadrze |
| `mipmapLevels` | 4 | 2 | więcej próbkowania tekstur |
| `maxAnisotropyBit` | 2 | 0 | filtrowanie anizotropowe włączone |
| `biomeBlendRadius` | 2 | 1 | mieszanie 5×5 zamiast 3×3 przy budowie chunka |
| `entityDistanceScaling` | 1.0 | 0.75 | encje rysowane na pełnym dystansie |
| `entityShadows` | true | false | dodatkowy przebieg cieni |
| `renderClouds` | "true" | "fast" | chmury wolumetryczne |
| `cloudRange` | 128 | 32 | 4× dalej rysowane chmury |
| `particles` | 0 (All) | 1 (Decreased) | pełna liczba cząstek |
| `simulationDistance` | 5 | 8 | tu SLM był tańszy |

`cutoutLeaves:false` to jest ta różnica, którą zobaczyłeś w liściach. Sam w sobie nie
kupuje FPS-ów, bo MoreCulling i tak wycina niewidoczne ściany.

## Błędy w configach

**`sodium-options.json` — `use_entity_culling: false`.** Wyłączony culling encji po stronie
Sodium, we wszystkich trzech wersjach. Zerowy zysk, czysta strata.

**`moreculling.toml` — `leavesCullingMode = "DEPTH"`.** Tryb DEPTH ma sens tylko przy
nieprzezroczystych liściach. Razem z `cutoutLeaves:false` daje spójną, ale najgorzej
wyglądającą kombinację. Do tego `useCustomItemFrameRenderer = true`, `itemFrameLODRange = 16`,
`itemFrame3FaceCullingRange = 2.0` i `signTextCulling = true` — cztery ustawienia, które
obniżają jakość obrazu bliżej gracza, niż ktokolwiek zauważy jako „optymalizację".

**`entityculling.json` — `sleepDelay: 153`.** Wątek cullingu przelicza widoczność około
6,5 raza na sekundę. Encje pojawiają się i znikają z opóźnieniem.

**`c2me.toml` — `gcFreeChunkSerializer = true`.** Dokumentacja moda opisuje to jako funkcję
eksperymentalną, która zmienia sposób zapisu chunków i wymaga regularnych backupów świata.
W publikowanej paczce to nie jest ustawienie domyślne, które można zostawić.

**`threadtweak.json` — `main: 15`.** Piętnaście wątków roboczych na procesorze z ośmioma.
Przy takim przeciążeniu scheduler traci więcej, niż zyskuje.

## Pliki, których paczka nie powinna wysyłać

| Plik | Problem |
|---|---|
| `sodium-fingerprint.json` | odcisk Twojego GPU i sterownika, rozsyłany do wszystkich pobierających |
| `iris-excluded.json` | zawartość to `{"excluded":["put:valuesHere"]}` |
| `fabric_loader_dependencies.json` | nadpisuje zależności moda `noisium`, którego w paczce nie ma |
| `threadtweak.json` na 26.x | ThreadTweak nie ma buildu na 26.1.2 ani 26.2 |
| `NoChatReports/*` | cztery pliki configu moda bez wpływu na wydajność |

## Mody bez roli wydajnościowej

`NoChatReports` i `placeholder-api`. Drugi to biblioteka serwerowa, w paczce klienckiej
nic nie obsługuje.

## Czego brakowało

| Mod | Co wnosi |
|---|---|
| Sodium Extra | kontrola mgły, cząstek, detali nieba i pogody — paczka nie miała żadnego z tych regulatorów |
| Chloride | culling encji i block entities po dystansie, fast models, wyłączenie cieni fontu |
| Particle Core | culling cząstek, tańsze transformacje wierzchołków |
| Better Block Entities | wsadowe renderowanie skrzyń i innych block entities |
| Sodium Shadowy Path Blocks | naprawa oświetlenia ścieżek bez kosztu |
| Continuity | pakiet `glass_pane_culling_fix` — mniej ścian szyb do narysowania |
| Packet Fixer, Fast IP Ping | sieć |
| Ixeris, FastQuit, RRLS | wejście, zamykanie świata, przeładowanie zasobów |

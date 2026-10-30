# Protokół pomiarowy

Cel: liczba, którą da się powtórzyć i obronić. Bez tego „lepsze od FO" jest opinią.

## Najprościej: mod benchmarku (Minecraft 26.3)

`bench/` zawiera mod, który robi cały przebieg sam i identycznie w każdej paczce:
otwiera (przy pierwszym uruchomieniu tworzy) świat „SLM Benchmark” ze stałego ziarna,
ustawia gracza w trybie obserwatora na stałej wysokości nad spawnem, a potem:
20 s rozgrzewki, 30 s sceny statycznej i 60 s przelotu po linii prostej z prędkością
10 bloków/s (budowanie chunków — scena, która decyduje o przycięciach). Czasy każdej
klatki zapisuje do `slm-bench/*.csv` i sam zamyka grę. Nie działa, dopóki w folderze gry
nie ma `slm-bench.txt`, więc w normalnej grze nic nie robi.

Na Windowsie najprościej dwuklikiem w `bench.cmd`: pokaże Twoje instancje, zapyta o dwie
nazwy, zainstaluje, poczeka, aż uruchomisz obie, i porówna wyniki. Ręcznie:

```
python bench_setup.py list
python bench_setup.py install "Streamline Master" --label SLM
python bench_setup.py install "Fabulously" --label FO
```

Instancję podajesz nazwą z `list` (wystarczy jej jednoznaczny fragment) albo pełną
ścieżką folderu w cudzysłowie. Obie muszą być na Minecrafcie 26.3.

Uruchom każdą instancję raz (ok. 2 minut, gra zamyka się sama), potem:

```
python bench_setup.py compare "Streamline Master" "Fabulously"
python bench_setup.py remove "Streamline Master"
```

`compare` bierze najnowsze nagranie każdej sceny z obu instancji i liczy je `bench.py`
(avg FPS, 1% i 0,1% low, przycięcia na minutę, werdykt z progami niżej). Warunki brzegowe
z tej strony obowiązują tak samo — mod usuwa zmienność trasy i świata, nie temperatury.

## Zasada (pomiar ręczny)

Dwie instancje w Prism Launcherze, ta sama wersja MC, ten sam świat, ten sam sprzęt,
ta sama sesja systemu. Zmienna jest jedna: paczka.

- `BENCH-SLM` — Streamline Master w bieżącej wersji, tak jak jest wydany
- `BENCH-FO` — Fabulously Optimized na tę samą wersję MC
- opcjonalnie `BENCH-PREV` — poprzednia wersja SLM, jeśli pytasz, ile dała ostatnia zmiana

Wszystkie instancje dostają identyczne argumenty JVM (`tune.py`) i identyczne
`options.txt` — skopiuj plik z instancji SLM do pozostałych. Bez tego mierzysz różnicę
ustawień, a nie różnicę paczek — dokładnie tak, jak wyszło przy pierwszym porównaniu
(`audit.md`).

## Warunki brzegowe

- Laptop na zasilaczu, plan zasilania „Najwyższa wydajność". Na baterii iGPU schodzi
  z zegarami i wynik jest bezwartościowy.
- Zamknięta przeglądarka, Discord, wszystko poza launcherem.
- Tryb pełnoekranowy, nie borderless. Na Intel HD/UHD borderless przechodzi przez
  kompozytor okien i kosztuje. W Chloride wyłącz „Borderless Fullscreen" na czas pomiaru.
- VSync wyłączony (`enableVsync:false` jest w overrides).
- Przed każdym przebiegiem: restart gry i 3 minuty przerwy między instancjami,
  żeby CPU zszedł z temperatury. i5-8350U to 15 W — throttling zjada więcej niż
  różnica między paczkami.

## Świat testowy

Jeden świat, skopiowany do obu instancji. Ustaw i zapisz:

```
/gamerule doDaylightCycle false
/gamerule doWeatherCycle false
/time set 6000
/weather clear
```

Zapisz współrzędne i kąty z F3 (`XYZ` oraz `Facing`). Do każdej sceny wracaj
teleportem na dokładnie te same wartości:

```
/tp @s <x> <y> <z> <yaw> <pitch>
```

## Sceny

| # | Scena | Co mierzy |
|---|---|---|
| 1 | Statyczna, powierzchnia, widok na las i wodę | fill rate, culling liści, przezroczystość |
| 2 | Statyczna, wnętrze wioski / bazy ze skrzyniami | block entities, fast models, EMF/ETF |
| 3 | Bieg 60 s w linii prostej w jedną stronę | budowanie chunków, 1% low, stutter |
| 4 | Statyczna, `/weather rain` | cząstki, weather radius |
| 5 | Statyczna, farma mobów / duże stado | tick encji, entity culling, LMD |

Scena 3 jest najważniejsza. Średni FPS w statyce mówi mało — to 1% low w ruchu
decyduje o tym, czy gra „stoi".

## Metryki

Na Windowsie: nakładka wydajności w Xbox Game Bar (Win+G) albo PresentMon / CapFrameX.
Obie dają średnią i 1% low bez ingerencji w grę i działają tak samo w obu instancjach.
Liczniki FPS w grze (Sodium Extra, Chloride) są tylko w SLM — nie używaj ich do porównania.

Do zapisu:

| Metryka | Skąd |
|---|---|
| avg FPS | nakładka, 60 s pomiaru |
| 1% low FPS | nakładka |
| RAM po 5 min w świecie | F3, wiersz „Allocated" i użycie |
| czas do menu głównego | stoper, od kliknięcia Launch |
| czas ładowania świata | stoper, od kliknięcia świata do zniknięcia ekranu ładowania |

Logi CSV z PresentMon albo CapFrameX liczy `bench.py` — zawsze tą samą metodą,
z progami z sekcji „Kiedy uznać wynik za przewagę”:

```
python bench.py slm-2.csv slm-3.csv --vs fo-2.csv fo-3.csv
```

Dla każdej strony bierze medianę z przebiegów i podaje avg FPS (klatki / czas, nie
średnią z chwilowych FPS), 1% low i 0.1% low (1000 / średnia z najwolniejszego 1% i 0,1%
klatek) oraz przycięcia na minutę (klatki dłuższe niż 2,5× mediana). Na końcu werdykt:
przewaga, remis albo wynik mieszany. Porównuj tylko logi z tego samego narzędzia —
każde liczy „1% low” trochę inaczej.

## Przebieg

3 przebiegi na scenę na paczkę. Odrzuć pierwszy (ładowanie chunków, kompilacja shaderów
sterownika). Z pozostałych dwóch weź medianę.

Przed każdym pomiarem odczekaj, aż w F3 licznik oczekujących chunków (`C:`) przestanie
rosnąć — inaczej mierzysz budowanie terenu, nie klatki.

## Profilowanie

Zanim uznasz, że coś jest wolne, sprawdź co konkretnie. Do instancji benchmarkowych
(nie do wydawanej paczki) wrzuć **spark** — jest na wszystkie trzy wersje, Fabric,
działa po stronie klienta.

```
/spark profiler start --timeout 60
/spark profiler stop
```

Wynik to drzewo wywołań z procentami czasu klatki. `/spark tps` i `/spark healthreport`
pokazują to samo dla wątku serwera zintegrowanego, czyli tego, który obciąża Cię
przy hostowaniu przez Essential.

To jedyny sposób, żeby rozmowa o „napisaniu własnego moda optymalizacyjnego" miała
podstawy. Bez profilu z Twojej maszyny każda taka decyzja jest zgadywaniem, którą
z już zoptymalizowanych ścieżek dubluje się po raz drugi.

## Arkusz wyników

`docs/benchmark-template.csv` — wypełnij i policz różnicę procentową.
Kolumna `notes` jest na obserwacje jakościowe: pop-in, mikroprzycięcia, artefakty.

## Kiedy uznać wynik za przewagę

Różnica poniżej 5% na średnim FPS mieści się w szumie pomiaru na laptopie z 15 W CPU.
Za realną przewagę uznaj:

- ≥10% na średnim FPS w scenie 1 lub 2, albo
- ≥15% na 1% low w scenie 3, albo
- wyraźnie mniejsze zużycie RAM przy tym samym FPS

Jeżeli wynik wyjdzie na remis — wtedy przewagą jest to, co widać poza wykresem:
krótszy start, mniej pamięci, mniej modów do utrzymania. To też jest wynik i tak
należy go opisać, zamiast dopisywać do opisu paczki liczby, których nikt nie zmierzył.

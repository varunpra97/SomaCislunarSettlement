<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logo/soma-logo-dark.png">
    <img src="assets/logo/soma-logo-light.png" alt="Soma logo: a ring looping the Moon backwards while the Moon circles Earth" width="320">
  </picture>
</p>

# Soma: Cislunar Ring Settlement

<p align="center"><img src="poster/soma-poster-animated.gif" alt="Animated Soma poster: every tile plays its build step"></p>

<p align="center"><b><a href="https://varunpra97.github.io/SomaCislunarSettlement/">Project page</a></b> · <a href="videos/soma-construction-film.mp4">Construction film (5 min 57 s)</a> · <a href="paper/soma-cislunar-rings.pdf">Paper (PDF)</a> · <a href="poster/soma-poster-60x36in.pdf">Poster (60 × 36 in PDF)</a></p>

A speculative design study for space settlements: a cislunar ring for about 550,000 people, six of them stacked on one shared spine, built from Starship-sized hull units, lunar material and self-assembling bay factories, and parked in a stable orbit around the Moon. The study also sketches two Sun-orbiting rings (between Earth and Mars, and in the asteroid belt).

The logo is the orbit itself: the ring loops the Moon backwards every 4.7 days while the Moon carries it around Earth.

All figures are order-of-magnitude estimates for a concept, not engineering results.

## <img src="assets/logo/soma-mark-dark.png" height="28" align="top"> The film: how Soma is built

Every construction animation in build order, from the spine to the finished six-ring stack, ending with a zoom out to its orbit around the Moon (5 min 57 s). Click the preview below to open the MP4 file.

[![How Soma is built](docs/soma-construction-film.gif)](videos/soma-construction-film.mp4)


## <img src="assets/logo/soma-mark-dark.png" height="28" align="top"> Construction, step by step

### 1 · The spine and centre pods (64 s)
Cargo Starships unload and then dock nose to tail along the spin axis: 280 hulls make a 14 km core with one pressurised corridor, and the ships at each end keep their engines to steer it. Robot arms build a 400 m centre pod (magnetic bearings, motor ring, spoke sockets) for each ring. Later, five concentric drums wrapped over the Starship core make the spine strong enough to carry the Sun-tracking loads.

[![The centre pod and the spine](docs/centre-pod-and-spine.gif)](videos/centre-pod-and-spine.mp4)

### 2 · The bay factory (66 s)
The hub Starship arrives, the work ring grows segment by segment, the gripper ring and beams go on, fit-out, then the inchworm cycle that moves the factory 18 m per bay.

[![The bay factory](docs/bay-factory.gif)](videos/bay-factory.mp4)

### 3 · Building the tube (57 s)
Robotic arms unload a Starship, close the ring frame, hang the hull panels, weld and leak-test one bay, then advance. The interactive version is in [`animation/ring-assembly.html`](animation/ring-assembly.html).

[![Ring assembly sequence](docs/ring-assembly.gif)](videos/ring-assembly.mp4)

### 4 · Spokes and the middle ring (48 s)
Six crawlers lay basalt-fibre spokes 17.35 km out in balanced pairs; small bay factories then close a 40 m middle ring at half radius (0.5 g).

[![Spokes and middle ring](docs/spokes-and-middle-ring.gif)](videos/spokes-and-middle-ring.mp4)

### 5 · Solar wings and radiators (50 s)
Wing robots unroll 90 m blankets of lunar-made cells along each spoke (17 km², ~6 GW); fin carriers on the shield fit one 150 × 75 m radiator per cell (~650 in all).

[![Solar wings and radiators](docs/solar-and-radiators.gif)](videos/solar-and-radiators.mp4)

### 6 · The ring stack (64 s)
Twin rings spin up against each other, the pair steers the stack to face the Sun like a giant gyroscope, two more pairs follow, and the build cost per resident falls with each new ring.

[![Building a ring stack](docs/ring-stack.gif)](videos/ring-stack.mp4)

## <img src="assets/logo/soma-mark-dark.png" height="28" align="top"> The orbit (58 s)

A lunar distant retrograde orbit ~30,000 km from the Moon. In a simplified Earth–Moon–Sun model it stayed bound for 20 years with no corrections, even with a 2 m/s kick each time a ring was added; larger loops (40,000–70,000 km) drifted off within a few years.

[![A stable orbit](docs/stable-orbit.gif)](videos/stable-orbit.mp4)

## <img src="assets/logo/soma-mark-dark.png" height="28" align="top"> Living there

### A day on the ring (91 s)
Dawn over a valley of terrace homes, a Roadster driving up a block's climb lane to its terrace, the commute, a spoke elevator to low gravity, the farm cells, the waterfront, the night market, life support at night, and the ring from outside.

[![A day on the ring](docs/day-on-the-ring.gif)](videos/day-on-the-ring.mp4)

## <img src="assets/logo/soma-mark-dark.png" height="28" align="top"> Poster

A 60 × 36 in poster of the whole project: the settlements named for the bodies they orbit, the finished stack on its loop around the Moon, lunar industry, one ring and how it is made, the 11 cell types (step terraces wherever people live), land, water and transit, the nine-step build, and the cost per resident.

- [Print PDF, 60 × 36 in](poster/soma-poster-60x36in.pdf) · [still image, 4096 px](poster/soma-poster-x.jpg)
- Animated GIF, 8-second loop: [1920 px](poster/soma-poster-animated.gif) · [3840 px](poster/soma-poster-animated-3840.gif)

## <img src="assets/logo/soma-mark-dark.png" height="28" align="top"> Paper

[**Soma: CisLunar Rings**](paper/soma-cislunar-rings.pdf) (15 pages): the design, build sequence, materials and cost for each of the 11 cell types, the lunar base and its specs, Starship launch counts, orbit and cost. The numbers come from [`paper/model/opsmodel.py`](paper/model/opsmodel.py). The LaTeX source is in [`paper/`](paper) and opens in Overleaf (New Project → Upload Project, with `main.tex` and `figures/` zipped).

## <img src="assets/logo/soma-mark-dark.png" height="28" align="top"> Report

[**Soma: Cost, Deployment and Operations**](docs/soma-report.pdf) (PDF, 36 pages): proof-of-concept milestones, cost, deployment, building the spokes, wings and radiators, ring stacks and the price per resident for each new ring, the orbit, bootstrapping, power, heat, air, water, food and waste, and how the systems work together.

## <img src="assets/logo/soma-mark-dark.png" height="28" align="top"> Design boards

| | |
|---|---|
| **The Chart of Settled Orbits**: the solar system with Helios Ring I (≈1.25 AU), Helios Ring II in the asteroid belt fed by Jupiter, and the cislunar rings. ![](designs/png/01-chart-of-settled-orbits.png) | **Cislunar Ring · Design Study**: 109 km ring, 150 m tube, static regolith shield, ~300 Mt bill of materials and where it comes from. ![](designs/png/02-cislunar-ring-design.png) |
| **Starship Hull Units**: 84-panel cross-section, 16 panels per Starship, unit catalogue and robotic assembly of one bay. ![](designs/png/03-starship-hull-units.png) | **The Bay Factory**: two 180 m rail rings and telescoping beams, 7 Starship flights to deploy, self-assembly and the inchworm cycle. ![](designs/png/04-bay-factory.png) |
| **Settlement Cells**: 45 levels per cell, 11 cell types including leisure (great outdoors, waterfront, food and night, parks and sports), a 20-cell district, and the cell mix. ![](designs/png/05-settlement-cells.png) | **Life Support**: air, water, food and waste loops, lunar make-up, light, heat and power, and safety. ![](designs/png/06-life-support.png) |
| **Landscape and Water**: hollow filter mountains and the district water loop. ![](designs/png/07-landscape-and-water.png) | **Power and Energy**: spoke solar wings, batteries, loads and air movement. ![](designs/png/08-power-and-energy.png) |

Full-size PNGs are in [`designs/png`](designs/png); standalone HTML versions are in [`designs/html`](designs/html).

## <img src="assets/logo/soma-mark-dark.png" height="28" align="top"> Key numbers

| | |
|---|---|
| Ring | 109 km around, 17.35 km radius, 1 g at 0.23 rpm |
| Tube | 150 m across, 45 levels of 3.33 m, 606 cells of 180 m |
| Population | ≈550,000 per ring with stacked homes; ≈3.3 million in a six-ring stack |
| Atmosphere | 57 kPa, 34% O₂ (NASA exploration atmosphere) |
| Mass | ~300 Mt per ring, mostly lunar regolith |
| Spine | 280 Starships docked nose to tail (14 km core), later wrapped in 5 concentric drums out to r 100 m (~1.4 Mt) |
| Middle ring | r 8.7 km, 0.5 g, Ø 40 m, ~0.5 Mt |
| Stack | 6 rings (3 counter-rotating pairs) on a 14 km spine, 2 km apart |
| Orbit | Lunar distant retrograde orbit, ~30,000 km from the Moon, 4.7-day loop |
| Cost per ring | ≈$89–356B standalone, with 100 rings sharing the lunar industry |
| Cost per resident | Ring 1: $168–661k → ring 100: $87–502k |

## <img src="assets/logo/soma-mark-dark.png" height="28" align="top"> Logo

The logo files are in [`assets/logo`](assets/logo): full logo and mark alone, dark and light, as PNG and SVG.

| Dark | Light |
|---|---|
| <img src="assets/logo/soma-logo-dark.png" width="260"> | <img src="assets/logo/soma-logo-light.png" width="260"> |

## <img src="assets/logo/soma-mark-dark.png" height="28" align="top"> Repository layout

```
assets/logo/       Soma logo and mark (PNG + SVG, dark and light)
poster/            60 × 36 in poster (PDF, JPG) and the animated GIF
paper/             LaTeX brief (main.tex, figures) and its PDF
index.html         the project page served by GitHub Pages
videos/            MP4 videos, including the full construction film
docs/              GIF previews used in this README, and the report PDF
designs/png/       board exports (2400 × 1600)
designs/html/      standalone board pages + SVG assets
animation/         interactive ring-assembly animation (HTML)
scripts/           Python (pycairo) scripts that render the videos, drawings and logo
scripts/stack/     spokes, solar/radiators, centre pod/spine, stack and orbit videos; cost and orbit models
scripts/film/      logo, title cards and the zoom-out finale
scripts/poster/    poster layout, drawn panels, animated tiles and GIF build
```

To re-render: `pip install pycairo numpy scipy`, have `ffmpeg` on the path, then run e.g. `python scripts/stack/stackvid.py all` or `python scripts/film/finale.py`. Each script writes one MP4 per scene and joins them with ffmpeg's concat demuxer.

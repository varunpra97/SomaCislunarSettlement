# Soma: Cislunar Ring Settlement

A speculative design study for space settlements: two Sun-orbiting rings (between Earth and Mars, and in the asteroid belt) and a cislunar ring for about 550,000 people, built from Starship-sized hull units, lunar material and a self-assembling bay factory.

All figures are order-of-magnitude estimates for a concept, not engineering results.

## Report

[**Soma: Cost, Deployment and Operations**](docs/soma-report.pdf) (PDF, 31 pages): proof-of-concept milestones, cost, deployment, bootstrapping, power, heat and radiators, air, water, food and waste, and how the systems work together.

## Videos

Click a preview to open the full MP4.

### A day on the ring (91 s)
What living there feels like: dawn over a valley of terrace homes, every home on a top floor, a Roadster driving straight up a block's climb lane to its terrace, the commute, a spoke elevator to low gravity, the farm cells, the waterfront, the night market, life support at night, and the ring from outside.

[![A day on the ring](docs/day-on-the-ring.gif)](videos/day-on-the-ring.mp4)

### The bay factory: deployment and operation (66 s)
The hub Starship arrives, the work ring grows segment by segment, the gripper ring and beams go on, fit-out, then the inchworm cycle that moves the factory 18 m per bay.

[![The bay factory](docs/bay-factory.gif)](videos/bay-factory.mp4)

### Ring assembly sequence (57 s)
Robotic arms unload a Starship, close the ring frame, hang the hull panels, weld and leak-test one bay, then advance. The interactive version is in [`animation/ring-assembly.html`](animation/ring-assembly.html) (open it in a browser).

[![Ring assembly sequence](docs/ring-assembly.gif)](videos/ring-assembly.mp4)

## Design boards

| | |
|---|---|
| **The Chart of Settled Orbits**: the solar system with Helios Ring I (≈1.25 AU), Helios Ring II in the asteroid belt fed by Jupiter, and six cislunar rings. ![](designs/png/01-chart-of-settled-orbits.png) | **Cislunar Ring · Design Study**: 109 km ring, 150 m tube, static regolith shield, ~300 Mt bill of materials and where it comes from. ![](designs/png/02-cislunar-ring-design.png) |
| **Starship Hull Units**: 84-panel cross-section, 16 panels per Starship, unit catalogue and robotic assembly of one bay. ![](designs/png/03-starship-hull-units.png) | **The Bay Factory**: two 180 m rail rings and telescoping beams, 7 Starship flights to deploy, self-assembly and the inchworm cycle. ![](designs/png/04-bay-factory.png) |
| **Settlement Cells**: 45 levels per cell, 11 cell types including leisure (great outdoors, waterfront, food and night, parks and sports), a 20-cell district, and the cell mix. ![](designs/png/05-settlement-cells.png) | **Life Support**: air, water, food and waste loops, lunar make-up, light, heat and power, and safety. ![](designs/png/06-life-support.png) |
| **Landscape and Water**: hollow filter mountains and the district water loop. ![](designs/png/07-landscape-and-water.png) | **Power and Energy**: spoke solar wings, batteries, loads and air movement. ![](designs/png/08-power-and-energy.png) |

Full-size PNGs are in [`designs/png`](designs/png); standalone HTML versions are in [`designs/html`](designs/html).

## Key numbers

| | |
|---|---|
| Ring | 109 km around, 17.35 km radius, 1 g at 0.23 rpm |
| Tube | 150 m across, 45 levels of 3.33 m, 606 cells of 180 m |
| Population | ≈550,000 with stacked homes; terrace homes (every home a top floor) hold ~850 people per cell instead of ~3,600 |
| Atmosphere | 57 kPa, 34% O₂ (NASA exploration atmosphere) |
| Mass | ~300 Mt for the first design, mostly lunar regolith; denser cells add ~80 Mt of basalt-fibre hoop bands |
| Hull | ≈509,000 panels; ~36,000 Starship flights if all from Earth, so later rings use lunar aluminium |
| Bay factory | ≈330 t, 7 Starship flights each, 6 per ring |
| Cost | Roughly $80–300B per ring if 100 rings share the lunar industry |

## Repository layout

```
videos/            MP4 videos
docs/              GIF previews used in this README
designs/png/       board exports (2400 × 1600)
designs/html/      standalone board pages + SVG assets
animation/         interactive ring-assembly animation (HTML)
scripts/           Python (pycairo) scripts that render the videos and cell drawings
```

To re-render the videos: `pip install pycairo`, have `ffmpeg` on the path, then run `python scripts/vid.py all` (bay factory) or `python scripts/life2.py all` (a day on the ring) and join the scene files with ffmpeg's concat demuxer.

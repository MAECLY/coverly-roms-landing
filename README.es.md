# Landing de Coverly ROMs

[![Estrellas](https://img.shields.io/github/stars/MAECLY/coverly-roms-landing?style=flat-square&label=estrellas)](https://github.com/MAECLY/coverly-roms-landing/stargazers) [![Visitas](https://hits.sh/github.com/MAECLY/coverly-roms-landing.svg?label=visitas&style=flat-square)](https://hits.sh/github.com/MAECLY/coverly-roms-landing/) [![Último commit](https://img.shields.io/github/last-commit/MAECLY/coverly-roms-landing?style=flat-square&label=último%20commit)](https://github.com/MAECLY/coverly-roms-landing/commits/main)

[English](README.md)

La web de [Coverly ROMs](https://github.com/MAECLY/coverly-roms), publicada
en **https://coverly-roms.maecly.com**: una web estática y bilingüe
(español en `/`, inglés en `/en/`), sin framework, sin dependencias y sin
rastreadores. La app, sus releases y sus incidencias están en
[MAECLY/coverly-roms](https://github.com/MAECLY/coverly-roms).

## Qué hay

- **La portada** ([es](https://coverly-roms.maecly.com/), [en](https://coverly-roms.maecly.com/en/)):
  primero las portadas (el hero, los cuatro pasos en un solo escritorio y
  «Tu tarjeta vuelve como estaba», con cómo se elige cada portada), y
  después lo que ha crecido alrededor: ordenar comprimidos y discos,
  consolas actuales sin claves, duplicados y las seis vistas, los formatos y
  los 131 sistemas por familia, la línea de comandos en su propia sección,
  la comparativa con Skraper, Skyscraper, ARRM y Mini Scraper, lo siguiente,
  las descargas y las preguntas.
- **[Funciones](https://coverly-roms.maecly.com/features/)** (`/features/`,
  `/en/features/`): todas las funciones en siete grupos, cada una con la
  versión en que llegó y un dibujo hecho con las piezas de la propia web.
- **[Hoja de ruta](https://coverly-roms.maecly.com/roadmap/)** (`/roadmap/`,
  `/en/roadmap/`): cada versión con su fecha, y lo que viene con su estado.

Todas las animaciones son dibujadas (nada de carruseles de capturas), se
reproducen una vez o con un botón, se paran fuera de pantalla y con el
ratón encima, y con movimiento reducido son un fotograma fijo.

## En local

Hace falta `python3` y `node` (24 o posterior); no hay nada que instalar.

```bash
make site                                                       # http://localhost:8080
make site SITE_PORT=8111                                        # otro puerto
make site RELEASE=scripts/site/fixtures/release.json            # release de prueba con los nombres hasta v0.2.0
make site RELEASE=scripts/site/fixtures/release-new.json        # nombres nuevos, con Intel y ARM64
make site RELEASE=scripts/site/fixtures/release-new-no-arm.json # nombres nuevos, sin Windows ARM64
make check                                                      # todas las comprobaciones, como en CI
make roadmap                                                    # sincroniza site/data/roadmap.json con ../coverly-roms
make help                                                       # todos los objetivos
```

`make check` también pasa los tests de `roadmap.py` y, con la app clonada
al lado (`../coverly-roms`, o `APP=`/`COVERLY_APP=`), falla si la hoja de
ruta o las cifras se desfasan de la app.

## Hoja de ruta y cifras

- `site/data/roadmap.json` es el único archivo detrás de `/roadmap/` y de
  «Lo siguiente» en la portada. `scripts/site/roadmap.py` escribe los
  bloques en las páginas (`<!-- roadmap:…:begin -->`), los comprueba y
  compara el archivo con `TODO.md`, `CHANGELOG.md` y `docs/TRACKER.md` de la
  app. `make roadmap` rellena lo que es de máquina (avance, versiones,
  fechas, huellas); el texto, el estado y lo que se publica se escriben a
  mano. Cuando la app publica una versión, `make roadmap` pasa «Próxima
  versión» a su número, también en `/features/`. En Vercel solo avisa.
- `site/data/facts.json` guarda las cifras que imprimen las páginas (131
  sistemas, 8 formatos, 62 créditos, sistemas por familia). Cada número
  marcado con `data-fact` tiene que coincidir, y frases como «más de 50
  sistemas» no pasan.

## Despliegue

Vercel despliega `main` con su integración de Git (`vercel.json` →
`scripts/site/vercel_build.sh`, que rellena la última release en
`target/site`). Al publicar una release, el workflow `landing-redeploy.yml`
de la app llama al deploy hook de Vercel; mientras tanto, `release.js`
actualiza la versión y las descargas en el navegador.

## Nombres de los archivos de cada release

La landing acepta los dos esquemas de nombres de la app: los nuevos
(`Coverly-ROMs_<v>_mac_arm.dmg`, `coverly_<v>_windows_arm.exe`, …), desde la
release siguiente a v0.2.0, y los que usaron las releases hasta v0.2.0
(`Coverly.ROMs_<v>_universal.dmg`, …). `apply_release.py` prueba primero el
nombre nuevo y después el antiguo, y rechaza una release que traiga los
dos nombres para la misma descarga.
Los enlaces para Mac con Intel y Windows ARM64 solo aparecen si la release
trae esos archivos. `release.js` nunca mezcla los dos esquemas en el
navegador; el deploy hook reconstruye la página.

**Orden de merge:** cualquier cambio en los nombres esperados se mergea aquí
antes de que la app publique una release que los use. Si no, el build de
Vercel falla y sigue sirviendo el despliegue anterior.

Los tokens de marca (`design/tokens.json`) son una copia de los de la app:
`make sync-tokens` los trae de `main` y regenera `site/assets/tokens.css`.

Más detalle en [docs/landing.md](docs/landing.md) (en inglés). Licencia
[AGPL-3.0](LICENSE).

## Créditos

Diseño y desarrollo de Miguel Esparza ([MAECLY](https://www.maecly.com)).
Tipografías: Archivo y Atkinson Hyperlegible Next y Mono (SIL OFL 1.1). Las
portadas de la web son formas generadas, no arte de juegos. Los créditos de
la app (fuentes de portadas, bases de datos, bibliotecas) están en su
pestaña Ajustes → Agradecimientos y en su
[THIRD-PARTY-NOTICES.md](https://github.com/MAECLY/coverly-roms/blob/main/THIRD-PARTY-NOTICES.md).

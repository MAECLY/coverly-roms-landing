# Landing de Coverly ROMs

[![Estrellas](https://img.shields.io/github/stars/MAECLY/coverly-roms-landing?style=flat-square&label=estrellas)](https://github.com/MAECLY/coverly-roms-landing/stargazers) [![Visitas](https://hits.sh/github.com/MAECLY/coverly-roms-landing.svg?label=visitas&style=flat-square)](https://hits.sh/github.com/MAECLY/coverly-roms-landing/) [![Último commit](https://img.shields.io/github/last-commit/MAECLY/coverly-roms-landing?style=flat-square&label=último%20commit)](https://github.com/MAECLY/coverly-roms-landing/commits/main)

[English](README.md)

La web de [Coverly ROMs](https://github.com/MAECLY/coverly-roms), publicada
en **https://coverly-roms.maecly.com**: una página estática y bilingüe
(español en `/`, inglés en `/en/`), sin framework, sin dependencias y sin
rastreadores. La app, sus releases y sus incidencias están en
[MAECLY/coverly-roms](https://github.com/MAECLY/coverly-roms).

## En local

Hace falta `python3` y `node` (24 o posterior); no hay nada que instalar.

```bash
make site                                                       # http://localhost:8080
make site SITE_PORT=8111                                        # otro puerto
make site RELEASE=scripts/site/fixtures/release.json            # release de prueba con los nombres hasta v0.2.0
make site RELEASE=scripts/site/fixtures/release-new.json        # nombres nuevos, con Intel y ARM64
make site RELEASE=scripts/site/fixtures/release-new-no-arm.json # nombres nuevos, sin Windows ARM64
make check                                                      # todas las comprobaciones, como en CI
make help                                                       # todos los objetivos
```

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

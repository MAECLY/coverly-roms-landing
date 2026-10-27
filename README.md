# Coverly ROMs landing

[![Stars](https://img.shields.io/github/stars/MAECLY/coverly-roms-landing?style=flat-square)](https://github.com/MAECLY/coverly-roms-landing/stargazers) [![Views](https://hits.sh/github.com/MAECLY/coverly-roms-landing.svg?label=views&style=flat-square)](https://hits.sh/github.com/MAECLY/coverly-roms-landing/) [![Last commit](https://img.shields.io/github/last-commit/MAECLY/coverly-roms-landing?style=flat-square)](https://github.com/MAECLY/coverly-roms-landing/commits/main)

[Español](README.es.md)

The website of [Coverly ROMs](https://github.com/MAECLY/coverly-roms), live at
**https://coverly-roms.maecly.com**: a static, bilingual page (Spanish at `/`,
English at `/en/`) with no framework, no dependencies and no trackers. The app
itself, its releases and its issues live in
[MAECLY/coverly-roms](https://github.com/MAECLY/coverly-roms).

## Run it locally

You need `python3` and `node` (24 or newer); there is nothing to install.

```bash
make site                                                       # http://localhost:8080, before the first release
make site SITE_PORT=8111                                        # another port
make site RELEASE=scripts/site/fixtures/release.json            # a (fake) release with the names used up to v0.2.0
make site RELEASE=scripts/site/fixtures/release-new.json        # the release names, with the Intel and ARM64 files
make site RELEASE=scripts/site/fixtures/release-new-no-arm.json # the release names, without Windows ARM64
make check                                                      # every gate, as CI runs it
make help                                                       # all targets
```

`make check` runs the token and cover-sprite staleness checks, the
`release.js` tests and `scripts/site/check_site.py` (links, ES/EN parity, head
tags and CSP, budgets, contrast, motion, art, release markers) on four builds:
the three fixtures above and the no-release state.

## How it deploys

- **Vercel Git integration.** Every push to `main` deploys production; pull
  requests get previews. `vercel.json` runs `scripts/site/vercel_build.sh`,
  which checks the site, asks the GitHub API for the latest release of
  `MAECLY/coverly-roms` and fills the `{{release.*}}` markers into
  `target/site`, the folder Vercel serves.
- **Deploy hook on each release.** Publishing a release changes nothing here,
  so the app repository's `landing-redeploy.yml` calls this project's Vercel
  deploy hook and `main` is rebuilt with the new downloads.
- **At runtime,** `site/assets/release.js` reads the latest release in the
  browser and updates the version and the download links if the page was
  built before it.

## Release file names

The landing reads both naming schemes of the app's release files:

- **Release names**, from the release after v0.2.0 on:
  `Coverly-ROMs_<v>_mac_arm.dmg`, `Coverly-ROMs_<v>_mac_intel.dmg`,
  `Coverly-ROMs_<v>_windows_x64-setup.exe`, `Coverly-ROMs_<v>_linux_x64.AppImage`,
  `coverly_<v>_windows_arm.exe`, and so on.
- **The names releases up to v0.2.0 used**: `Coverly.ROMs_<v>_universal.dmg`,
  `Coverly.ROMs_<v>_x64-setup.exe`, `Coverly.ROMs_<v>_amd64.AppImage`, ...

`apply_release.py` tries the release name of each download first and the old
name second, and refuses a release that has both names for the same
download. The Intel Mac and Windows
ARM64 links appear only when the release has those files (`asset`/`noasset`
blocks), so a v0.2.0 build renders the same cards as before. `release.js`
never mixes the two schemes in the browser: it upgrades a page only to a
release with the same names, and the deploy hook rebuilds the page for the
rest.

**Merge order:** merge any change to the expected names here before the app
publishes a release that uses them. Otherwise the Vercel build fails on the
unknown files and keeps serving the previous deployment.

## Brand tokens

`design/tokens.json` is a copy of the app's, which is the source of truth.
`make tokens` regenerates `site/assets/tokens.css` from it; `make sync-tokens`
first fetches the app's copy from `main`. The `Sync tokens` workflow does
that weekly and opens a pull request when something changed.

More in [docs/landing.md](docs/landing.md); open work in [TODO.md](TODO.md).

## License

[AGPL-3.0](LICENSE), like the app. Fonts are under the SIL Open Font License
1.1; see [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md).

# Third-party notices

The Coverly ROMs landing (https://coverly-roms.maecly.com) is licensed under
the GNU Affero General Public License v3.0 (see `LICENSE`), like the app in
[MAECLY/coverly-roms](https://github.com/MAECLY/coverly-roms), whose
`THIRD-PARTY-NOTICES.md` covers the application. The page uses no
third-party code; the screenshots show the app's mock backend with labelled
placeholder art, not real box art.

## Fonts

The website self-hosts three typefaces (`site/assets/fonts/`), each licensed
under the SIL Open Font License 1.1:

- **Archivo**, Copyright 2020 The Archivo Project Authors
  (https://github.com/Omnibus-Type/Archivo). Licence: `OFL-Archivo.txt`.
- **Atkinson Hyperlegible Next**, Copyright 2020-2024 The Atkinson
  Hyperlegible Next Project Authors
  (https://github.com/googlefonts/atkinson-hyperlegible-next). Licence:
  `OFL-AtkinsonHyperlegibleNext.txt`.
- **Atkinson Hyperlegible Mono**, Copyright 2020-2024 The Atkinson
  Hyperlegible Mono Project Authors
  (https://github.com/googlefonts/atkinson-hyperlegible-next-mono). Licence:
  `OFL-AtkinsonHyperlegibleMono.txt`.

The shipped `.woff2` files are modified versions of the variable fonts from
the google/fonts repository: their axes are limited (Archivo wdth 75-112 and
wght 600-800, Atkinson Hyperlegible Next wght 400-700, Atkinson Hyperlegible
Mono wght 400-600), they are subset to Latin, Latin-1 Supplement and Latin
Extended-A, hinting is removed, and they are converted to WOFF2. They keep
their original family names, which the OFL allows because none of these
fonts declares a Reserved Font Name. Each licence file sits next to the font
files.

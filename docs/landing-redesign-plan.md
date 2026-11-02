# Plan del rediseño de la landing (noviembre de 2026)

Rama `feat/landing-redesign`. Brief de Miguel del 2026-11-01. Inventario del
2026-11-02: landing `d3057a0`, app `735cbe9` (PR #36).

Este documento tiene dos pasadas. La primera es el plan (§1–§10). La segunda
es la crítica de ese plan contra el brief y contra los vicios de una página
genérica (§11). Las correcciones de la crítica ya están aplicadas en las
secciones de arriba, y §11 explica qué se cambió y por qué.

## 0. Lo que no se negocia

- **El nombre se queda: Coverly ROMs.**
- **Las portadas siguen siendo lo principal.** El hero, la primera sección y
  la sección más larga de la home hablan de portadas. Todo lo demás se
  presenta como lo que ha crecido alrededor de ellas.
  - Medida de control: en 1440×900, el hero, `#como` y `#seguro` ocupan al
    menos el 40 % de la altura de la home. Lo compruebo en el navegador.
- **Lenguaje visual propio: «La estantería viva».** Se usa la gramática del
  hueco tal como está en `docs/landing.md`: discontinuo = aún no, sólido =
  hecho, lomo Buckram = lo hizo Coverly, pestaña Manila = aún se puede
  deshacer.
  - Paleta: tokens de `tokens.css`, papel `#f2f3ef`, petróleo `#0e5e6f`,
    Manila `#e6c171`, banda greyboard oscura y terminal `#121514`.
  - Tipografías: Archivo variable a ancho 75 para los títulos, Atkinson
    Hyperlegible Next para el texto y Atkinson Hyperlegible Mono solo para la
    terminal y los nombres de archivo.
  - No entra ningún color ni tipografía nuevos.
- **Las animaciones son ilustradas.** Se construyen con las piezas de la
  página: `kit.svg` (`sm`, `sf`, `spine`, `tab`, `stag`, `folder`, `ftab`,
  `p-box`, `ck`, `lean`…), las portadas generadas de `covers.svg` y la ventana
  de `views.js`. Nunca un carrusel de capturas.
  - Todas se paran fuera de pantalla, al pasar el ratón o con el foco, en
    una pestaña oculta y con `cr-halt`.
  - Con movimiento reducido son un fotograma final estático.
  - Cada una tiene botón para saltar o repetir.
  - El HTML ya es la página terminada.
- **Paridad es/en** en todas las páginas (`site/` y `site/en/`).
- **Enlaces prohibidos:** ROMs, claves y emuladores.
- «Xbox» solo aparece como nombre de sistema (Xbox, Xbox 360, Xbox One, Xbox
  Series).
- **Solo cuento lo que está en `main` de la app.**
  - El arreglo `.wua` (`fix/prefer-wua-over-folder`, sin commits ni PR) no
    sale en la landing hasta que se mergee.
  - ScreenScraper está construido pero oculto sin credenciales de
    desarrollador (bitácora M6). Sigue en «Dónde van por delante» y en «Lo
    que aún no hace».

## 1. Orden de la home

```
 Topbar   wordmark · Cómo funciona · Consolas · Terminal · Comparar · Funciones · Hoja de ruta · [Descargar] · EN
 ───────────────────────────────────────────────────────────────────────────
 Hero     «Cada ROM, con su portada.»  + la estantería The Lean-To (sin cambios)        PORTADAS
 #como    4 pasos en UN escritorio (antes: 4 pantallas fijadas)  ── banda oscura        PORTADAS
 #seguro  demo Simular/Aplicar/Deshacer + «Y elige bien cada portada» + cascada de fuentes   PORTADAS (la más larga)
 #ordenar «Más que portadas.»  comprimidos/discos (ilustrado) · consolas actuales sin claves · duplicados · seis vistas
 #formatos «Escribe donde tu consola busca.»  8 perfiles + 131 sistemas por familia (sin terminal)
 #terminal NUEVA «Todo, también desde la terminal.»  índice de órdenes + terminal con 4 escenas
 #comparar «Las otras opciones, comparadas.»  12 filas (antes 7)
 #siguiente NUEVA «Lo siguiente: tu biblioteca.»  3 huecos discontinuos sacados de roadmap.json
 #descargar (sin cambios de estructura; «Lo que aún no hace» al día)
 #preguntas 10 preguntas (cambian 2 y entra 1)
 Cierre    estantería final (sin cambios)
 Footer    + Funciones · Hoja de ruta · Novedades (CHANGELOG)
```

Todo el texto va alineado a la izquierda, como hoy. La única excepción
centrada sigue siendo la estantería del cierre.

### 1.1 Hero: no cambia lo que se ve

- **H1 igual:** «Cada ROM, con su portada.» / «Every ROM gets its cover.»
  La palabra clave sigue sobre su subrayado de hueco: es la firma de la
  marca, no un adorno.
- **Subtítulo:** el actual, más una segunda frase más pequeña en un `<p>`
  aparte, después de los botones.
  - es: «Y ya que está, ordena tus descargas en 131 sistemas y aparta los
    juegos que tienes repetidos.»
  - en: «And while it's there, it sorts your downloads into 131 systems and
    sets aside the games you have twice.»
- **Datos rápidos (`<ul>`):** se añade «131 sistemas» / «131 systems» entre
  «Sin telemetría» y «Windows, macOS y Linux».
- **Meta description** (155 caracteres como máximo, «gratis / sin cuenta»
  al principio, resuelve el punto 2 del TODO de la landing):
  - es: «Gratis y sin cuenta: Coverly ROMs añade las portadas que faltan en
    tu consola portátil, ordena 131 sistemas y aparta duplicados. Con
    deshacer.» (146)
  - en: «Free, no account: Coverly ROMs adds the missing covers on your
    handheld, sorts 131 systems and sets duplicates aside. With undo.» (133)
- **`<title>`:** se mantiene («Las portadas que faltan en tus ROMs»).

### 1.2 `#como`: de cuatro pantallas a una

**Hoy:** un escritorio fijado al hacer scroll. Pasa por cuatro capturas y
ocupa unas cuatro alturas de pantalla.

**Nuevo:** un solo escritorio de la altura de una pantalla.

- A la izquierda, una lista ordenada de 4 pasos. Aquí la numeración sí
  tiene sentido, porque es una secuencia.
- A la derecha, la captura del paso activo, con su cámara y sus
  anotaciones. Se reutilizan los clips de los pasos 3 y 4 y las elipses de
  los pasos 1 y 2.
- **Cambio de paso:**
  - Cada paso es un botón.
  - El paso activo llena su lomo Buckram en 4 s y pasa al siguiente,
    igual que los botones de `views.js`.
  - El cambio entre capturas es la cortina `clip-path` de hoy, nunca un
    fundido.
  - Se pausa con el ratón encima, con el foco, fuera de pantalla y con
    `cr-halt`.
  - Con movimiento reducido se queda en el paso 1, y los botones cambian
    al instante.
  - Sin JS se ven los 4 pasos uno debajo de otro, cada uno con su captura
    a `@1x`. Es lo mismo que hoy en móvil, así que no se pierde contenido.
- **En móvil** (menos de 1024 px), cada paso lleva su captura debajo, sin
  pinning.
- **Se elimina** el pinning con `animation-timeline` de esta sección. Ahorra
  CSS y unos 3 viewports de scroll.
- **Se reutiliza código:** `views.js` pasa a ser `deck.js`, un controlador
  genérico de «botones + paneles + lomo que se llena» que se configura con
  atributos `data-deck`. Lo usan la ventana de las seis vistas, `#como`, la
  terminal de `#terminal` y las ilustraciones de `/features`. La tabla de
  posiciones de las seis vistas sigue en `gen_views.py`, que ahora la
  escribe en un `data-` del HTML.

Copy (título igual: «Cuatro pasos. Los dos primeros no escriben nada.» /
«Four steps. The first two write nothing.»):

| # | es | en |
|---|---|---|
| 1 | **Abre la tarjeta.** Coverly reconoce tu firmware y cuenta lo que le falta a cada sistema: portada, captura o pantalla de título. | **Open the card.** Coverly recognises your firmware and counts what each system is missing: cover, screenshot or title screen. |
| 2 | **Simula.** Identifica cada ROM por su huella y te enseña el plan entero. Todavía no escribe nada. | **Dry run.** It identifies each ROM by its fingerprint and shows you the whole plan. Nothing is written yet. |
| 3 | **Decide las dudosas.** Las seguras van solas; las dudosas esperan en una cola que recorres con el teclado, y cada una dice por qué. | **Decide the doubtful ones.** Confident matches go through; doubtful ones wait in a queue you walk with the keyboard, and each says why. |
| 4 | **Aplica, o deshaz.** Las imágenes se escriben de una en una. Deshacer devuelve la tarjeta a como estaba. | **Apply, or undo.** Images are written one at a time. Undo puts the card back as it was. |

Las anotaciones dibujadas se quedan como están: «lo que falta, contado»,
«y dice por qué», «deshacer, siempre».

### 1.3 `#seguro`: la sección estrella crece

**Título igual:** «Tu tarjeta vuelve como estaba, con más portadas.» /
«Your card comes back as it was, plus covers.»

La demo Simular/Aplicar/Deshacer y las cinco promesas no cambian. Se le
añade una segunda mitad con todo lo que hace bien las portadas, que es justo
donde Coverly gana a las alternativas.

```
 ┌──────────────── demo SD ↔ datos de la app (igual) ───────────────┐
 │ Simular  Aplicar  Deshacer                                        │
 └───────────────────────────────────────────────────────────────────┘
  5 promesas (igual)
 ───────────── H3 «Y elige bien cada portada.» ─────────────
  ┌ cascada de fuentes (ilustración) ┐   Por su huella …
  │  [ ┄ ]  ← libretro ┄ (falla)      │   En tu región …
  │         ← SteamGridDB ┄ (falla)   │   Aunque nadie la tenga …
  │  [ ▮ ]  ← el propio juego ✓       │   Con el nombre que busca RetroArch …
  └───────────────────────────────────┘   A mano, juego a juego …
                                         Mientras rellena …
  captura del informe de auditoría (igual)
```

**Ilustración nueva, «la cascada de fuentes»** (`svg.art` en línea,
alrededor de 2,5 KB):

- Un hueco discontinuo (`#sm`) con una portada generada a medio fundir.
- Tres lomos de fuente se acercan por turnos:
  - libretro-thumbnails y SteamGridDB se quedan en discontinuo, porque no
    tienen nada para ese juego de PS4;
  - el tercero, «el propio juego», registra su icono: el hueco pasa a
    sólido, se dibuja su lomo Buckram y cae su pestaña Manila.
- Dura 2,4 s y se reproduce una vez al entrar en pantalla, con ↻ Repetir.
- Los nombres de las fuentes van en HTML (`<ol>` debajo), porque la puerta
  `art` no admite `<text>`.
- Con movimiento reducido se ve el fotograma final.

Copy de la lista (cada punto: nombre en negrita y una frase):

| es | en |
|---|---|
| **Por su huella.** Reconoce cada ROM por CRC32, MD5 o SHA1, no solo por el nombre, y entiende los nombres cortos de arcade. | **By fingerprint.** It recognises each ROM by CRC32, MD5 or SHA1, not only by name, and understands arcade short names. |
| **En tu región.** Prefiere la portada de la región de la ROM, o sigue el orden de fuentes que elijas. | **In your region.** It prefers the cover from the ROM's region, or follows the source order you choose. |
| **Aunque nadie la tenga.** Si ninguna fuente tiene portada, usa el icono que lleva el propio juego: PS3, PS Vita, Wii U, 3DS, Xbox 360, PS4, PS5 y Xbox One. | **Even when nobody has it.** If no source has a cover, it uses the icon the game carries: PS3, PS Vita, Wii U, 3DS, Xbox 360, PS4, PS5 and Xbox One. |
| **Con el nombre que busca RetroArch.** Los títulos con «&» o «:» se guardan como RetroArch los busca, y entonces los encuentra. | **With the name RetroArch looks for.** Titles with “&” or “:” are saved the way RetroArch looks for them, so it finds them. |
| **A mano, juego a juego.** Desde la ficha cambias, quitas o buscas otra imagen, o pones una tuya. | **By hand, game by game.** From the game's panel you change, remove or search for another image, or use your own. |
| **Sabes cuánto falta.** Mientras rellena, ves portadas por minuto y el tiempo que queda. | **You know how long.** While it fills, you see covers per minute and the time left. |

Antes de publicar, compruebo en la app (`sources::embedded` y facts v8) la
lista exacta de sistemas con portada incrustada, y si NRO homebrew entra en
la frase.

### 1.4 `#ordenar`: «Más que portadas.», al día

**Entradilla:**

- es: «Alrededor de las portadas, Coverly ROMs ha aprendido a ordenar la
  biblioteca. Todo se simula primero y se puede deshacer.»
- en: «Around the covers, Coverly ROMs has learned to tidy the library.
  Everything is a dry run first and can be undone.»

Siguen siendo filas `.feat` alternas, ahora cuatro, con un cierre corto.

1. **Ordena por sistema, también lo comprimido.** / **Sorts by system,
   archives too.**
   - es: «Reconoce zip, 7z, RAR y otros por lo que llevan dentro. Extrae
     los juegos de disco comprobando el CRC de cada pista, mueve como uno
     solo los juegos que son una carpeta (PS3, Vita, Wii U, PS4…) y agrupa
     los multidisco sueltos con su `.m3u`.»
   - en: «It recognises zip, 7z, RAR and more by what's inside. It
     extracts disc games checking each track's CRC, moves folder games
     (PS3, Vita, Wii U, PS4…) as one item and groups loose multi-disc games
     with their `.m3u`.»
   - **Ilustración nueva, «el comprimido que se abre»**, en lugar de la
     captura de Organizar. Reproduce la ilustración de progreso de la
     propia app (#30):
     - una caja (`#p-box`) se abre;
     - salen 4 pistas en fila como huecos discontinuos;
     - cada una pasa a sólido y recibe su ✓ (`#ck`) al «comprobar su CRC».
     - El contador es HTML vivo con `aria-hidden` y el texto de la app:
       «Juego 2 de 4 · Pista 5 de 16» / «Game 2 of 4 · Track 5 of 16».
     - Es una escena de `deck.js` de 3 s que se repite al pulsar.
2. **Consolas actuales, sin claves.** / **Current consoles, no keys.** Fila
   nueva, sin imagen. La landing no lleva los iconos de RetroArch Assets, y
   no los traigo solo para esto: añadirían peso y otra licencia que
   acreditar. Ver §11.16.
   - es: «Switch, 3DS, PS4, PS5 y Xbox One se reconocen por lo que va en
     claro. Coverly nunca lee ni pide claves, y deja tus archivos de
     licencia donde están. Los nombres de Switch salen del propio archivo
     o, si lo activas, de un catálogo público.»
   - en: «Switch, 3DS, PS4, PS5 and Xbox One are recognised from what's
     stored in the clear. Coverly never reads or asks for keys, and leaves
     your licence files where they are. Switch names come from the file
     itself or, if you turn it on, from a public catalogue.»
3. **Aparta las copias repetidas sin borrar nada.** Igual que hoy, con una
   frase más:
   - es: «También las de un mismo title ID y versión, o la misma carpeta.»
   - en: «Also those with the same title ID and version, or the same
     folder.»
   - La captura se queda: es estática, y eso está permitido.
4. **Seis vistas, y un icono para cada sistema.** Igual, con la ventana de
   `views.js` (ahora movida por `deck.js`).

**Cierre** (un párrafo y un enlace):

- es: «Y además: pregunta antes de mover un juego de más de 10 GB, se
  actualiza con versiones firmadas, y en Ajustes, Agradecimientos lista
  las 62 fuentes y bibliotecas que usa, con su licencia. **Ver todas las
  funciones**» (enlace a `/features/`).
- en: «Also: it asks before moving a game over 10 GB, it updates with
  signed versions, and in Settings, Credits lists the 62 sources and
  libraries it uses, with their licences. **See every feature**»
  (enlace a `/en/features/`).

### 1.5 `#formatos`: perfiles y sistemas, sin la terminal

**Título igual.**

**Entradilla:**

- es: «Ocho formatos de firmware y frontend, detectados al abrir la
  carpeta, y 131 sistemas con la carpeta que usa cada uno.»
- en: «Eight firmware and frontend layouts, detected when you open the
  folder, and 131 systems with the folder each one uses.»

**Contenido:**

- La tabla de 8 perfiles × portada/captura/título y la fila de galería que
  se revela se quedan igual.
- **Nuevo:** sustituye a la terminal una tira de familias de sistemas, un
  `<ul>` en línea. Cada familia lleva un número y un mini hueco sólido
  dibujado en CSS:
  - es: «Cartucho · Portátiles · Disco · Arcade · Ordenadores · Consolas
    actuales · Fantasía · Ports y motores».
  - Los números salen de `coverly systems --json` en la app (o del
    `systems.rs` de la app) y quedan en `site/data/facts.json`. Ver §6.

### 1.6 `#terminal` (nueva): la CLI en su propia sección

Va en la banda oscura (`--cr-code-bg`), que hoy solo usa `#como`. Así
`#como` y `#terminal` hacen de sujetalibros de la parte central.

```
 «Todo, también desde la terminal.»
 entradilla
 ┌──────────── órdenes (dl) ────────────┐ ┌──────── terminal ────────┐
 │ audit     cuenta lo que falta         │ │ [Portadas][Ordenar]      │
 │ fill      rellena el arte             │ │ [Duplicados][Deshacer]   │
 │ organize  ordena por sistema          │ │ $ coverly …  (tecleado)  │
 │ dedupe    aparta duplicados           │ │ salida                   │
 │ undo      deshace                     │ │                          │
 │ catalog   catálogo de Switch          │ └──────────────────────────┘
 │ profiles · systems · update           │   nota: binario suelto, x64 y ARM64
 └───────────────────────────────────────┘
```

**Título:** «Todo, también desde la terminal.» / «All of it, from the
terminal too.»

**Entradilla:**

- es: «La orden `coverly` hace lo mismo que la app y se puede programar.
  Rellenar, ordenar y apartar duplicados son una simulación hasta que
  añades `--apply`, y cada informe sale en JSON si lo pides.»
- en: «The `coverly` command does what the app does and can be scripted.
  Filling, sorting and setting duplicates aside are a dry run until you add
  `--apply`, and every report comes out as JSON if you ask.»
- Comprobado en `main.rs`: «dry run unless --apply» en `fill`, `organize` y
  `dedupe`.

**Lista de órdenes** (`<dl>`, el nombre en mono):

| orden | es | en |
|---|---|---|
| `audit` | Cuenta lo que falta. Solo lee. | Counts what's missing. Read-only. |
| `fill` | Rellena portadas, capturas y pantallas de título. | Fills covers, screenshots and title screens. |
| `organize` | Ordena por sistema, con comprimidos y discos. | Sorts by system, with archives and discs. |
| `dedupe` | Aparta las copias repetidas. | Sets repeated copies aside. |
| `undo` | Deshace el último trabajo, o también los posteriores. | Undoes the last job, or the later ones too. |
| `catalog switch` | Descarga, revisa o borra el catálogo de nombres de Switch. | Downloads, checks or removes the Switch name catalogue. |
| `profiles`, `systems` | Lista los formatos y los 131 sistemas. | Lists the layouts and the 131 systems. |
| `update` | Busca e instala versiones firmadas. | Checks for and installs signed versions. |

**Terminal:** es el bloque de terminal de hoy, movido aquí y repartido en 4
escenas de `deck.js`. La escritura de `motion.js` se reutiliza escena por
escena. Los números cuadran con los del hero (4553 sin portada).

1. **Portadas:** `coverly audit /Volumes/SD --missing-only` → «4553 sin
   portada»; `coverly fill /Volumes/SD` → «plan: 4553 · 0 escritos»;
   `coverly fill /Volumes/SD --apply --auto-only` → «✓ 4401 aplicadas».
2. **Ordenar:** `coverly organize ~/Descargas --target /Volumes/SD` →
   «plan: 212 a 31 sistemas · 0 movidos»; `… --apply --skip-large` →
   «extract item 2/4 files 5/16» (la línea real de la CLI) y «✓ 209
   ordenados · 3 grandes saltados».
3. **Duplicados:** `coverly dedupe /Volumes/SD` → «38 copias en 17 grupos ·
   0 apartadas»; `… --apply` → «✓ 38 a _Duplicados/».
4. **Deshacer:** `coverly undo` → «↶ 4401 restauradas».

Las salidas de las escenas 2 y 3 se copian de la salida real de la CLI
contra los fixtures de la app antes de publicar. No me invento el formato.

**Nota final** (párrafo pequeño):

- es: «Binario suelto para macOS, Windows y Linux, en x64 y ARM64.
  **Descargar la línea de comandos**» (enlace a `#descargar`).
- en: «A single binary for macOS, Windows and Linux, x64 and ARM64.
  **Download the command line**».

### 1.7 `#comparar`: 12 filas

Las columnas no cambian: Coverly ROMs, Skraper, Skyscraper, ARRM y Mini
Scraper. Se mantienen las 7 filas de siempre; «Windows» pasa a decir «x64 y
ARM64» y «Simulación y deshacer» se amplía. Entran 5 filas nuevas,
elegidas porque en ellas Coverly gana o es el único.

| Fila es / en | Coverly ROMs | Qué hay que verificar en las otras |
|---|---|---|
| Windows / Windows | x64 y ARM64 | ¿ARM64 nativo en alguna? |
| Simulación y deshacer **en portadas, ordenar y duplicados** / Dry run and undo **for covers, sorting and duplicates** | Sí | Hoy las 4 salen «—» |
| Identifica por huella / Identifies by fingerprint | CRC32, MD5, SHA1 | Skraper sí (hash dentro de zip/7z/rar/gz/xz/tar, `skraper.md`); Skyscraper, ARRM y Mini Scraper por comprobar |
| Revisa las dudosas, con el motivo / Reviews doubtful matches, with the reason | Sí | Documentación de las cuatro |
| Portada aunque no esté en las bases (icono del propio juego) / A cover even when the databases lack one (the game's own icon) | PS3, Vita, Wii U, 3DS, 360, PS4, PS5, Xbox One | Las cuatro |
| Ordena por sistema, con comprimidos y discos / Sorts by system, with archives and discs | Sí | **ARRM se llama «Roms manager»**: verificar a fondo |
| Aparta duplicados sin borrar / Sets duplicates aside without deleting | Sí | Las cuatro |
| Consolas actuales, sin claves / Current consoles, no keys | Sí | Las cuatro |

**Reglas:**

- **Nunca «No» sin una fuente.** Si la documentación no lo dice, la celda
  lleva «—», que ya se explica en la leyenda.
- **Fuentes revisadas en noviembre de 2026.** La leyenda pasa a «recogidos
  en noviembre de 2026».
- **Se quita una fila nueva si no aguanta la verificación**, por ejemplo si
  ARRM también ordena por sistema. Mejor 10 filas ciertas que 12 dudosas.
- En la columna Coverly se reutiliza la cortina de resaltado y los ✓
  dibujados.

**Entradilla** (provisional; la cierro cuando estén las celdas):

- es: «Para las portadas, es la única que simula y deshace, en los tres
  sistemas y sin cuenta. Y además ordena y aparta duplicados, con el mismo
  deshacer.»
- en: «For covers, it's the only one that does a dry run and undo, on all
  three systems and without an account. And it also sorts and sets
  duplicates aside, with the same undo.»

**«Dónde van por delante», al día:**

- es: «Skraper, Skyscraper y ARRM usan ScreenScraper y traen vídeos,
  mezclas de imágenes, logos y metadatos; Coverly ROMs todavía no usa
  ScreenScraper. Mini Scraper y ROMCover también funcionan sin cuenta en
  Mac y traen el formato de Anbernic. Y Coverly ROMs aún no se ha probado
  en consolas reales.»
- en: «Skraper, Skyscraper and ARRM use ScreenScraper and bring videos,
  image mixes, logos and metadata; Coverly ROMs doesn't use ScreenScraper
  yet. Mini Scraper and ROMCover also work without an account on Mac and
  ship the Anbernic layout. And Coverly ROMs hasn't been tested on real
  handhelds yet.»
- ROMCover entra solo en este párrafo, con su fuente. No entra como columna.

**Fuentes:** las cuatro de hoy, más la de ROMCover.

**Ancho en móvil:** la tabla ya tiene scroll propio dentro de su figura
(sin scroll horizontal de la página). Con 12 filas, la primera columna
queda fija (`position: sticky`).

### 1.8 `#siguiente` (nueva): el paso hacia la biblioteca

Es una sección corta en papel claro.

**Título:** «Lo siguiente: tu biblioteca.» / «Next: your own library.»

**Entradilla:**

- es: «Coverly va camino de ser la biblioteca de tus juegos, no solo de tu
  tarjeta. Esto es lo que está en marcha.»
- en: «Coverly is on its way to being the library of your games, not just
  your card. This is what's in progress.»

**Contenido:**

- Tres huecos discontinuos en fila, los de la hoja de ruta: actualizaciones
  y DLC dentro de su juego, la biblioteca propia y las fuentes por title ID.
- Cada uno lleva su título, una frase, su estado y su recuento de tareas
  como mini huecos.
- Todo sale de `site/data/roadmap.json` (§5), con los mismos bloques
  generados que `/roadmap`.
- Enlace: «Ver la hoja de ruta» / «See the roadmap».

### 1.9 `#descargar`, `#preguntas` y cierre

**«Lo que aún no hace»:**

- Se quita «más de 50 sistemas».
- Se quita «Reconocer discos de PS2 o 3DO dentro de comprimidos», **solo
  si** la app los reconoce dentro de un zip/7z. El CHANGELOG solo dice que
  «se organizan». Lo compruebo con los fixtures de `coverly-core` antes de
  quitar la línea; si no los reconoce, se queda.
- «ScreenScraper: previsto» se queda.
- Entra «Poner las actualizaciones y DLC dentro de la carpeta de su juego
  (en camino)».

**FAQ (10):**

- «¿Con qué consolas funciona?» menciona los 131 sistemas.
- «¿Envía datos a algún sitio?» añade el catálogo de Switch: opcional,
  apagado por defecto.
- Pregunta nueva:
  - es: «¿Necesito claves para Switch o PS4?» → «No. Coverly ROMs nunca
    lee ni pide claves. Reconoce lo que puede con lo que va en claro, y lo
    que no puede leer queda como «Cifrado».»
  - en: «Do I need keys for Switch or PS4?» → «No. Coverly ROMs never
    reads or asks for keys. It recognises what it can from what's stored in
    the clear, and anything it can't read stays as “Encrypted”.»
- Todo esto se refleja en el JSON-LD `FAQPage`.

**Cierre:** sin cambios.

## 2. `/features` y `/en/features/`

**Rutas:** `site/features/index.html` y `site/en/features/index.html`.

- La URL es la misma en los dos idiomas, como pide el brief. Descarté
  `/funciones/` porque complica `hreflang`, el selector de idioma y las
  puertas sin aportar nada.
- **Título de la pestaña:** «Funciones · Coverly ROMs» / «Features ·
  Coverly ROMs».
- **H1:** «Todo lo que hace Coverly ROMs.» / «Everything Coverly ROMs
  does.»
- **Entradilla:**
  - es: «Empezó rellenando portadas y sigue siendo lo que mejor hace.
    Alrededor ha crecido todo lo demás. Aquí está agrupado, con la versión
    en que llegó cada cosa.»
  - en: «It started by filling in covers, and that's still what it does
    best. Everything else grew around it. Here it is, grouped, with the
    version each thing arrived in.»

**Composición: la estantería por grupos, no un mosaico de tarjetas.**

```
 ┌ índice (sticky ≥1024) ┐  ┌──────────────────────────────────────────────┐
 │ ▮ Portadas            │  │ H2 Portadas y arte          [ilustración]    │
 │ ▯ Consolas y formatos │  │ ───────────────────────────────────────────  │
 │ ▯ Ordenar             │  │ Auditoría          Lista sistema por …  v0.1 │
 │ ▯ Duplicados          │  │ Identificación     Reconoce cada ROM …  v0.1 │
 │ ▯ Biblioteca y vistas │  │ Portada incrustada Usa el icono que …  próx. │
 │ ▯ Terminal            │  │ …                                            │
 │ ▯ Ajustes y confianza │  └──────────────────────────────────────────────┘
 └───────────────────────┘   (siguiente grupo, la misma estructura)
```

**Índice lateral:**

- Es una pila de lomos: cada grupo es un lomo de libro.
- El del grupo que estás leyendo se rellena de Buckram con
  `IntersectionObserver`; los demás quedan en contorno.
- En móvil pasa a ser una fila de anclas con scroll propio.

**Cada grupo:**

- Un `<h2>`, una frase de entrada y una ilustración.
- Una lista de definiciones con tres columnas: nombre (`dt`), frase
  (`dd`) y etiqueta de versión.
- **La etiqueta de versión** es la del `#descargar` (`#stag`, Manila, a
  ancho 75):
  - «v0.1.0», «v0.2.0» o «Próxima versión» / «Next version»;
  - cuando la app publique, `roadmap.py --update` (§5) cambia «Próxima
    versión» por el número.
  - Las etiquetas no son decoración: dicen la versión en que llegó cada
    cosa.

**Contenido:** las tablas A–G del inventario, con su copy es/en ya escrito
en una frase. Se copian tal cual en el HTML, ajustando el tono a la
landing. Cada grupo lleva su frase de entrada:

| Grupo es / en | Frase de entrada es | en |
|---|---|---|
| Portadas y arte / Covers and art | Lo que hizo nacer a Coverly, y donde más se nota. | Why Coverly exists, and where it shows most. |
| Consolas y formatos / Handhelds and layouts | Ocho formatos y 131 sistemas, cada uno con su carpeta. | Eight layouts and 131 systems, each with its folder. |
| Ordenar por sistema / Sort by system | De una carpeta de descargas a una biblioteca en orden. | From a downloads folder to a tidy library. |
| Duplicados / Duplicates | Por contenido, nunca por nombre, y sin borrar. | By content, never by name, and nothing deleted. |
| Biblioteca y vistas / Library and views | Seis formas de mirar lo que tienes. | Six ways to look at what you have. |
| Terminal / Command line | Todo lo anterior, programable. | All of the above, scriptable. |
| Ajustes y confianza / Settings and trust | Sin cuenta, sin telemetría, con versiones firmadas y créditos a la vista. | No account, no telemetry, signed versions and credits in plain sight. |

**Ilustraciones** (una por grupo, cada una con piezas que ya existen):

| Grupo | Ilustración | Reutiliza | Movimiento |
|---|---|---|---|
| Portadas | La cascada de fuentes | `#seguro` de la home (el mismo `<symbol>` en `kit.svg`) | Una vez al entrar, ↻ |
| Consolas | La fila de galería que se revela por perfil | `#formatos` | Al entrar, CSS |
| Ordenar | El comprimido que se abre, con las pistas ✓ | `#ordenar` de la home | `deck.js`, ↻ |
| Duplicados | **Nueva:** 3 portadas iguales; la que se queda recibe su lomo Buckram, las otras dos se deslizan a una carpeta `_Duplicados/` (`#folder`, `#ftab`) y cae la pestaña Manila de deshacer | `kit.svg` + `covers.svg` | Una vez al entrar, ↻ |
| Biblioteca | La ventana de las seis vistas | `views.js` → `deck.js` | Como hoy |
| Terminal | Una terminal estática con `coverly --help` resumido (texto HTML, no SVG) | Estilo `.term` | Ninguno |
| Ajustes y confianza | **Nueva, estática:** un paquete (`#p-box`) con un sello ✓ de firma y un hueco discontinuo vacío donde «iría la telemetría» (el mismo mini hueco vacío del contador del footer) | `kit.svg` | Ninguno |

**Regla de movimiento de la página:** solo se mueve la ilustración que está
en pantalla, una cada vez, y se reproduce una sola vez. Todas se paran
fuera de pantalla y con el ratón encima, y con movimiento reducido son el
fotograma final.

**JSON-LD:** `SoftwareApplication` con `featureList` (una línea por
función, el mismo texto que los `dt`) y `BreadcrumbList`.

**Al final de la página:** CTA «Descargar Coverly ROMs» (enlace a
`/#descargar`) y enlace a la hoja de ruta.

## 3. `/roadmap` y `/en/roadmap/`

**Rutas:** `site/roadmap/index.html` y `site/en/roadmap/index.html`.

- **Título de la pestaña:** «Hoja de ruta · Coverly ROMs» / «Roadmap ·
  Coverly ROMs».
- **H1:** «Lo que ya está y lo que viene.» / «What's done and what's
  next.»
- **Entradilla:**
  - es: «Cada versión, con su fecha y lo que trajo. Debajo, lo que viene,
    en el orden en que se hará y con su estado.»
  - en: «Each version, with its date and what it brought. Below, what's
    next, in the order it will be built and with its status.»

**Componente: la estantería de versiones.** Es una línea de tiempo de
verdad, así que el orden visual es el cronológico.

```
 Entregado
 ════════ v0.1.0 ══ 17 oct 2026 ══════════════════════════════════
  ▮▮▮▮▮▮▮▮  Auditoría · Relleno con deshacer · Explorador · …     (huecos sólidos, lomo Buckram)
 ════════ v0.2.0 ══ 25 oct 2026 ══════════════════════════════════
  ▮▮▮▮▮     Seis vistas · Comprimidos y discos · Duplicados
 ════════ Próxima versión ══ ya en el código, sin publicar ══════
  ▮▮▮▮▮▮▮▮▮ 131 sistemas · Consolas actuales sin claves · …       (sólidos, sin etiqueta)

 Lo que viene
  ┌┄┄┄┐ Actualizaciones y DLC dentro de su juego     En investigación   ▮▯▯▯▯▯▯▯ 0 de 15
  ┌┄┄┄┐ Tu biblioteca                                 Planificado · espera a la anterior
  ┌┄┄┄┐ Fuentes de nombres y arte por title ID        En investigación   ▮▯▯… 1 de 27
  …
```

- **Versiones:**
  - cada versión es una balda (`<section>` con `<h3>`);
  - la etiqueta de acceso Manila (`#stag`) lleva la versión, y la fecha va
    en un `<time>` a su lado, no en una cadena unida con puntos;
  - los cambios son una `<ul>` de huecos sólidos con lomo Buckram, porque
    los hizo Coverly.
- **«Próxima versión»:** huecos sólidos sin etiqueta de acceso, porque está
  hecho pero aún no tiene número. Cuando se publique la versión, el script
  le pone su etiqueta.
- **Lo que viene:**
  - una `<ol>`, porque el orden de prioridad es real;
  - cada bloque es un hueco discontinuo con título, una frase, su estado
    con palabras y su avance;
  - el avance es una fila de mini huecos, los mismos 24 de la barra de
    progreso de la cabecera, escalados a hechas/total;
  - si el total pasa de 24, se agrupan y debajo va el número exacto:
    «1 de 27» / «1 of 27»;
  - las dependencias van en una frase («Espera a: actualizaciones y DLC»),
    no en flechas.
  - No se muestran los números internos del TODO (2.1, 3.1…): para quien
    lee no significan nada, y viven solo en `data-id` y en el JSON.
- **Estados** (vocabulario cerrado, es/en):

  | `status` | es | en | Hueco |
  |---|---|---|---|
  | `verifying` | Hecho, falta probarlo | Done, being tested | sólido, con pestaña Manila |
  | `almost` | Casi listo | Almost there | sólido con un hueco discontinuo |
  | `research` | En investigación | Being researched | discontinuo que marcha una vez |
  | `planned` | Planificado | Planned | discontinuo |
  | `blocked` | Espera a otro bloque | Waiting on another block | discontinuo atenuado |
  | `parked` | Aparcado | Parked | discontinuo con trama |

- **Lo que no entra en la página pública:** «Modo usa tus propias claves»
  (aparcado hasta una revisión legal). Lo dejo fuera a propósito para no
  sugerir nada sobre claves. Tampoco entra lo que depende de Miguel
  (credenciales, copia de la clave): en el JSON llevan `"public": false`.
- **Movimiento:** ninguno automático. Es una página de lectura y no tiene
  JS propio (cero bytes nuevos de script).
- **JSON-LD:** `WebPage` + `ItemList` de las versiones.

## 4. Animaciones: inventario y contrato

| Pieza | Dónde | Nueva o reutilizada | Disparo | Saltar | Reducido |
|---|---|---|---|---|---|
| The Lean-To | Hero | Igual | Al cargar | ↻ Repetir | Final |
| Escritorio de 4 pasos | `#como` | Reutilizada (capturas, clips, cortina) con `deck.js` | En pantalla, 4 s por paso | Botones de paso | Paso 1 |
| Cascada de fuentes | `#seguro`, `/features` | **Nueva** (`kit.svg`) | 40 % en pantalla, una vez | ↻ | Final |
| El comprimido que se abre | `#ordenar`, `/features` | **Nueva** (`kit.svg`, copia la ilustración de la app #30) | En pantalla, `deck.js` | ↻ | Final, 4/4 ✓ |
| Seis vistas | `#ordenar`, `/features` | Igual (`deck.js`) | Como hoy | Botones | Portadas |
| Terminal con 4 escenas | `#terminal` | Reutiliza la escritura de `motion.js` + `deck.js` | En pantalla | Botones de escena | Escena 1 escrita |
| Duplicados que se apartan | `/features` | **Nueva** (`kit.svg`, `covers.svg`) | Una vez al entrar | ↻ | Final |

**Reglas que comprueba la puerta `motion` (se amplía a las 6 páginas):**

- solo se animan `transform`, `opacity`, `clip-path` y `stroke-dashoffset`;
- `[data-off]` fuera de pantalla;
- pausa en `:hover` y `:focus-within`;
- `cr-halt` en `deck.js`;
- ni `<video>` ni `autoplay`.

**Un solo momento fuerte por página:**

- **Home:** el hero. El resto son tiempos tranquilos que se disparan al
  llegar o al pulsar.
- **`/features`:** ninguno al cargar. Cada grupo se reproduce al llegar a
  él.
- **`/roadmap`:** ninguno.

## 5. Datos de la hoja de ruta: `site/data/roadmap.json` y su guardia

Un solo archivo alimenta `/roadmap`, `/en/roadmap/` y `#siguiente` en las
dos homes. **El HTML lleva los bloques ya generados** (la regla de «el HTML
es la página terminada»), entre marcadores `<!-- roadmap:begin -->` …
`<!-- roadmap:end -->`. El navegador no descarga el JSON: el archivo vive
en `site/data/` para que el repo lo versione, y `vercel.json` no lo sirve
(o lo sirve sin enlazar; se decide al implementar).

### 5.1 Formato

```json
{
  "schema": 1,
  "source": {
    "app_repo": "MAECLY/coverly-roms",
    "app_commit": "735cbe9",
    "todo_sha256": "…",
    "changelog_sha256": "…",
    "tracker_sha256": "…",
    "synced": "2026-11-02"
  },
  "released": [
    {
      "version": "0.2.0",
      "date": "2026-10-25",
      "items": [
        { "es": "Seis vistas e iconos de sistema", "en": "Six views and system icons" },
        { "es": "Ordenar con comprimidos y juegos de disco, con extracción verificada", "en": "Sorting with archives and disc games, with verified extraction" },
        { "es": "Duplicados, a _Duplicados/ o a la Papelera, y coverly dedupe", "en": "Duplicates, to _Duplicados/ or the Trash, and coverly dedupe" }
      ]
    }
  ],
  "unreleased": {
    "prs": [28, 29, 30, 31, 32, 33, 34, 35, 36],
    "items": [
      { "es": "131 sistemas, de 54", "en": "131 systems, up from 54", "prs": [32, 33, 34] },
      { "es": "Consolas actuales sin claves y nombres de Switch", "en": "Current consoles without keys, and Switch names", "prs": [34, 36] }
    ]
  },
  "next": [
    {
      "id": "2.1",
      "public": true,
      "status": "research",
      "progress": { "done": 0, "total": 15 },
      "after": [],
      "title": { "es": "Actualizaciones y DLC dentro de su juego", "en": "Updates and DLC inside their game" },
      "summary": { "es": "…", "en": "…" }
    }
  ]
}
```

**Quién escribe cada campo:**

- **Los escribe la máquina** con `roadmap.py --update APP`: `source.*`,
  `released[].version` y `date` (del CHANGELOG), `next[].progress` (las
  casillas `- [x]` / `- [ ]` de cada `## N.` del TODO, contando sus `###`
  hasta el siguiente `##`), y que exista cada `id`.
- **Los escribe una persona** (copy de la landing): `items`, `title`,
  `summary`, `status` y `public`.
- `--update` nunca pisa lo que escribe una persona. Si en el TODO aparece
  un bloque nuevo, lo añade con `"public": false` y `"status": "planned"`,
  y con el copy vacío, que la puerta de abajo rechaza hasta que alguien lo
  escriba.

### 5.2 `scripts/site/roadmap.py`

| Modo | Qué hace | Dónde corre |
|---|---|---|
| `--check` | Valida el esquema: estados del vocabulario, fechas ISO, versiones SemVer en orden, paridad es/en de cada texto, `after` que apunta a `id`s que existen, `progress.done ≤ total`. **Vuelve a generar los bloques `roadmap:` de las 6 páginas** (4 de roadmap y 2 homes) y falla si el HTML no coincide. | `make check`, `check_site.py` (puerta `roadmap`), Vercel |
| `--check --app PATH` | Además compara con la app: los `id` contra los `## N.` del TODO, el progreso contra las casillas, las versiones y fechas contra `## [x.y.z] - fecha` del CHANGELOG, que todo PR de la bitácora del TRACKER posterior a la última versión esté en `unreleased.prs`, y los `*_sha256` contra los archivos. Si algo no cuadra, falla y dice qué campo actualizar. | `make check` cuando existe `../coverly-roms` (o `COVERLY_APP=`); `make roadmap-check` |
| `--update PATH` | Rellena los campos de la máquina y regenera los bloques del HTML. Si el CHANGELOG ya tiene la versión nueva, mueve `unreleased` a `released` y cambia «Próxima versión» por el número en `/features`. | `make roadmap APP=../coverly-roms` |
| `--remote` | Igual que `--check --app`, pero lee `TODO.md`, `CHANGELOG.md` y `docs/TRACKER.md` de `main` desde `api.github.com/repos/MAECLY/coverly-roms/contents/…`, el host que el build ya usa. | `vercel_build.sh`, **solo para avisar**: imprime `::warning::` y nunca rompe el deploy |

Así no se puede desfasar sin que nadie se entere:

- en local, `make check` falla;
- en cada deploy, el log de Vercel avisa;
- y `landing-redeploy.yml` ya redespliega con cada release de la app.

**Tests:** `scripts/site/roadmap.test.py` (o `.mjs`, como los que ya hay)
con fixtures mínimas de TODO, CHANGELOG y TRACKER en
`scripts/site/fixtures/app/`: casillas anidadas, un `###` dentro de un
`##`, una versión nueva en el CHANGELOG y un PR que falta.

### 5.3 `site/data/facts.json` (pequeño)

`{"systems": 131, "profiles": 8, "credits": 62, "families": {…}}`.

- `check_site.py` comprueba que cada número que aparece en las páginas
  (marcados con `data-fact="systems"`) coincide con este archivo.
- Con `--app`, comprueba también que `systems` coincide con el registro de
  sistemas de la app.
- Así se evita que vuelva a pasar lo de «más de 50» cuando ya eran 131.

## 6. Navegación, footer, sitemap, llms.txt y OG

- **Topbar** (6 enlaces y el CTA):
  - es: «Cómo funciona · Consolas · Terminal · Comparar · Funciones · Hoja
    de ruta»;
  - en: «How it works · Handhelds · Terminal · Compare · Features ·
    Roadmap».
  - «Seguridad» y «Preguntas» pasan al menú móvil y al footer.
  - En `/features` y `/roadmap`, los enlaces de sección apuntan a `/#…`, y
    el de la página actual lleva `aria-current="page"` y su lomo Buckram
    lleno.
  - El enlace de idioma va a la misma página en el otro idioma.
- **Footer:** se añaden «Funciones», «Hoja de ruta» y «Novedades» (el
  CHANGELOG en GitHub). Esto cierra en parte el punto 8 del TODO.
- **`sitemap.xml`:** 6 URLs, cada una con su `xhtml:link` es/en/x-default.
  `lastmod` sale de la fecha del último commit de `site/`, también sin
  release (punto 4 del TODO).
- **`llms.txt` / `agents.txt`:**
  - «What it does today» al día: 131 sistemas, Organizar con
    comprimidos, discos y juegos-carpeta, consolas actuales sin claves,
    duplicados por title ID, la CLI con todas sus órdenes, Agradecimientos
    y descargas por chip.
  - Se quita «More than 50».
  - Secciones nuevas `## Docs` con enlaces `[título](url)` a las 6 páginas,
    el repo, las versiones y la licencia (punto 3 del TODO).
- **JSON-LD de la home:** la `description` empieza por las portadas y
  después nombra lo demás. `operatingSystem` añade «Windows 11 ARM64» y
  «macOS (Intel)».
- **OG:**
  - `og.mjs` aprende una lista de tarjetas: las 2 de hoy y 4 nuevas
    (`og-features.png`, `og-features-en.png`, `og-roadmap.png`,
    `og-roadmap-en.png`).
  - Usan el mismo diseño (icono Lean-To, wordmark, regla de estantería)
    con el H1 de cada página.
  - Presupuesto: 4 × ~45 KB.
- **`404.html`:** enlaces a Funciones y Hoja de ruta.

## 7. Presupuestos y puertas

| Qué | Hoy | Nuevo | Por qué |
|---|---|---|---|
| Home (es/en), crudo/gzip | 74 000 / 17 500 | 78 000 / 18 600 | Se ahorra en `#como` (unos −3 KB de cámaras y raíl fijado). Se suman `#terminal` (+3,5 KB), la cascada (+2,5 KB), el comprimido (+2 KB), 5 filas de comparativa (+2 KB), `#siguiente` (+1,5 KB) y la FAQ (+0,4 KB). |
| `/features` (cada idioma) | — | 70 000 / 16 500 | 7 grupos con unas 45 funciones, 5 ilustraciones en línea y la ventana de las seis vistas |
| `/roadmap` (cada idioma) | — | 34 000 / 8 500 | Solo HTML y mini huecos en CSS |
| Hojas de estilo | 86 000 / 19 400 | `site.css` 90 000 / 20 400 + `pages.css` 10 000 / 2 600 (solo en `/features` y `/roadmap`) | La home no carga el CSS de las páginas nuevas |
| Scripts (todos) | 29 000 / 9 100 | 31 500 / 9 900 | `views.js` (3 000) pasa a `deck.js` (≤ 3 600); un `toc.js` de 900 para el índice de `/features`; `motion.js` sube a ≤ 10 000 por las escenas de la terminal |
| Arte (`assets/art/*.svg`) | 24 000 / 7 000 | 27 000 / 8 000 | Los símbolos de la cascada y de duplicados se comparten en `kit.svg` |
| Palabras visibles | 1 850 por idioma | home 1 950; `/features` 2 600; `/roadmap` 1 200 | La home gana unas 100: `#como` pierde unas 180 y se suman `#terminal`, `#seguro` y `#siguiente` |
| OG | — | 6 PNG ≤ 60 KB cada uno | |

**`check_site.py`:**

- `PAGES` pasa a 6 entradas, cada una con su tipo de presupuesto.
- `REQUIRED` recoge las 4 páginas nuevas, `deck.js`, `toc.js`,
  `pages.css`, `data/roadmap.json`, `data/facts.json` y los 4 OG.
- La puerta `parity` compara es/en de cada par.
- `head` comprueba la CSP exacta en las 6 páginas.
- `links` incluye las rutas nuevas con barra final.
- Puertas nuevas:
  - `roadmap`: `roadmap.py --check`;
  - `facts`: los `data-fact`;
  - `stale_copy`: rechaza «más de 50» / «more than 50» y cualquier
    `\b5[0-9] sistemas`.
- Los presupuestos se miden sobre la salida construida, como hoy, en las
  4 variantes.

**`Makefile`:** se añaden `roadmap` y `roadmap-check`, y `check` llama a
`roadmap.py --check` (más `--app` si existe la app). La previsualización se
sirve con `make site SITE_PORT=8091`.

## 8. Plan de trabajo (commits pequeños, cada uno con su push)

1. `docs: add landing redesign plan` (este archivo).
2. `refactor(site): generalise views.js into deck.js`. Es el mismo
   comportamiento, con tests de las seis vistas y de los gates de
   movimiento en verde.
3. `feat(site): roadmap data file and roadmap.py with drift checks`. Lleva
   el JSON, el script, los tests y fixtures, y los objetivos del
   `Makefile`.
4. `feat(site): facts.json and stale-copy gate`.
5. `feat(site): compact the four steps into one desk`.
6. `feat(site): cover choices and the source cascade in #seguro`.
7. `feat(site): refresh More than covers with archives and current consoles`.
8. `feat(site): split the command line into its own section`.
9. `feat(site): add rows to the comparison`. Va después de verificar las
   fuentes; cada celda tiene su fuente en el commit.
10. `feat(site): next-up teaser fed by roadmap.json`.
11. `feat(site): features pages (es/en)`.
12. `feat(site): roadmap pages (es/en)`.
13. `feat(site): nav, footer, sitemap, llms.txt, agents.txt and JSON-LD`.
14. `feat(site): OG cards for the new pages`.
15. `chore(site): budgets and gates for six pages`, más
    `docs(landing): document the redesign`, que actualiza `landing.md`, la
    tabla de movimiento y los presupuestos.

**Verificación antes del PR:**

- `make check` en verde, con la app presente.
- Chrome DevTools sobre `make site SITE_PORT=8091` con la release de
  ejemplo:
  - 1440×900 y 390×844, claro y oscuro, movimiento reducido sí y no, los
    dos idiomas, las 6 páginas;
  - `document.getAnimations().length === 0` con movimiento reducido;
  - sin JS;
  - con teclado;
  - 0 errores de consola;
  - Lighthouse móvil ≥ 90;
  - CLS 0;
  - la medida del 40 % de portadas (§0).
- Capturas en el PR.

## 9. Lo que hay que verificar antes de escribir según qué copy

- **ARRM ordena por sistema o no** (se llama «Roms manager»). Y si alguna
  alternativa identifica por hash, aparta duplicados o reconoce consolas
  actuales. Hay que ir a la documentación de cada una, con fecha de
  noviembre de 2026.
- **Discos de PS2 y 3DO dentro de zip/7z.** Lo compruebo con los fixtures
  de la app.
- **La lista exacta de sistemas con portada incrustada**, y si NRO homebrew
  cuenta como «juego».
- **La salida real** de `coverly organize` y `coverly dedupe` para las
  escenas de la terminal.
- **Los recuentos por familia de sistemas.**
- **El texto de ayuda de `undo`** en `main.rs` dice «fill or organise». La
  landing dirá «el último trabajo», que es cierto en los dos casos. Lo
  anoto para la app, que no toco.

## 10. Fuera de este rediseño

- Leer `credits/credits.json` de la app en la landing (TODO 7). Es una
  buena tarea, pero la dejo aparte: aquí solo se enlaza a la pestaña
  Agradecimientos.
- Grabaciones reales de la app.
- `security.txt`, `humans.txt` y Search Console.

## 11. Crítica del plan y qué cambié

He revisado la primera versión contra el brief y contra los defectos de
una página genérica. Esto es lo que encontré y lo que cambié:

1. **`/features` era un mosaico de tarjetas** (7 grupos × 6 tarjetas
   redondeadas con icono). Es el kit SaaS de manual, y además le daba el
   mismo peso a «Imágenes limpias» que a «Portada incrustada».
   → **Cambio:** estantería por grupos, con índice de lomos, listas de
   definiciones y etiquetas de versión. Las etiquetas son el accesorio de
   acceso que ya usa `#descargar`, así que la estructura dice algo: cuándo
   llegó cada cosa.
2. **Numeraciones de adorno.** Había puesto «01–07» a los grupos de
   `/features` y los ids del TODO (2.1, 3.1) en `/roadmap`.
   → **Cambio:** solo se numeran los 4 pasos, que son una secuencia de
   verdad. La lista de lo que viene es una `<ol>` sin números visibles
   (el orden ya se ve), y los ids se quedan en los datos.
3. **La hoja de ruta como barras de progreso de colores y diagrama de
   Gantt.** Es genérico y además prometía fechas que nadie ha dado.
   → **Cambio:** filas de mini huecos con la gramática de la marca, estado
   con palabras y sin fechas futuras. Las fechas solo aparecen en lo
   entregado.
4. **Cadenas con puntos medios** («v0.2.0 · 25 oct 2026 · 3 cambios»).
   → **Cambio:** etiqueta de versión y `<time>` separados. Solo se queda
   «Juego 2 de 4 · Pista 5 de 16», porque es el texto literal de la app.
5. **Etiquetas en versalitas encima de cada H2** («FUNCIONES»,
   «NOVEDADES»).
   → **Cambio:** fuera. Los títulos de sección ya llevan su regla de
   estantería con el remate Buckram. No se añade ningún antetítulo.
6. **Flecha «→» en los enlaces** («Ver todas las funciones →»).
   → **Cambio:** fuera en todo lo nuevo. El enlace dice lo que hace. Ya
   hay una «→» en la home dentro de la anotación del paso 3; esa
   representa teclas pulsadas y se queda.
7. **Mono para etiquetas pequeñas** (estados, versiones).
   → **Cambio:** la mono solo para órdenes, nombres de archivo y la
   terminal. Las etiquetas van en Archivo a ancho 75, como la etiqueta de
   acceso que ya existe.
8. **Demasiado movimiento en `/features`.** Siete ilustraciones en bucle
   al mismo tiempo.
   → **Cambio:** una cada vez, solo la que está en pantalla, una sola vez,
   con ↻. La de Terminal y la de Ajustes son estáticas.
9. **Las portadas perdían peso.** En la primera versión, `#ordenar` subía
   por encima de `#seguro` y el hero decía «ordena, aparta, portadas». El
   brief dice que las portadas son la estrella.
   → **Cambio:** el H1 no se toca, la frase nueva va después de los
   botones y en pequeño, `#seguro` gana su segunda mitad («Y elige bien
   cada portada») y es la sección más larga, y la comparativa empieza su
   entradilla por las portadas. Además hay una medida de control (§0).
10. **La comparativa iba a decir «No» sin pruebas** (ordena por sistema:
    ARRM «No»).
    → **Cambio:** «—» si no está documentado, verificar ARRM a fondo y
    quitar la fila si no se sostiene. La honestidad de esa tabla es parte
    de la marca (ya tiene «Dónde van por delante»).
11. **El copy de relleno** («potente», «todo en uno», «la herramienta
    definitiva»).
    → **Cambio:** cada frase dice lo que hace, en voz activa y desde quien
    usa la app («Cuenta lo que falta. Solo lee.»). En inglés, igual de
    directo.
12. **La terminal en la home se quedaba como un adorno** con los mismos 4
    comandos de antes.
    → **Cambio:** la sección dice qué ordenes hay (`<dl>`, texto real e
    indexable) y la terminal enseña 4 escenas reales, incluida la
    confirmación de juegos grandes, que es nueva.
13. **Mantener `/features` y la home a mano dejaría que los números se
    desfasaran** («más de 50» ya pasó).
    → **Cambio:** `facts.json` + `data-fact` + la puerta `stale_copy`. La
    hoja de ruta, con su guardia contra la app.
14. **Riesgo de añadir sin quitar** (consejo de Chanel).
    → **Cambio:** se quitan el pinning de 4 pantallas de `#como`, la
    captura de Organizar (la sustituye la ilustración), la terminal de
    `#formatos` y 2 enlaces del topbar.
15. **Lo que sí hay que defender aunque parezca uno de los vicios
    genéricos.**
    - El subrayado de hueco bajo «portada» en el H1 acentúa una sola
      palabra. Se queda porque es la firma de la marca y cuenta la
      historia del producto: el hueco que se rellena.
    - La banda oscura con terminal (`#121514`) es el token `--cr-code-bg`
      de la marca, no un negro teñido elegido por moda.
16. **Iconos de sistema en la fila «Consolas actuales».** Los había
    propuesto, pero la landing no los tiene: traerlos de RetroArch Assets
    añade peso y otra licencia CC BY que acreditar, solo por decorar.
    → **Cambio:** fila de texto, sin imagen.

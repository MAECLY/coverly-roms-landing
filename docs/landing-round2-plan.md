# Plan de la ronda 2 de la landing (noviembre de 2026)

Peticiones de Miguel sobre el PR #8 (2026-11-02), que se resuelven en la
misma rama `feat/landing-redesign`:

1. Mostrar en la home todos los sistemas que soportamos, con su icono,
   después de comprobar si las marcas lo permiten. Se piden dos cosas: un
   carrusel y otra forma de recorrer la lista completa.
2. En «Aparta las copias repetidas sin borrar nada», cambiar la captura por
   una animación.
3. En `/features`, más animación en cada función o una escena fija (sticky)
   que avance con el scroll.
4. En `/roadmap`, un roadmap muy visual y fácil de leer por encima del
   texto, hecho después de ver cómo lo resuelve la industria.
5. Las 4 decisiones pendientes, que Miguel nos ha delegado: aplicamos las
   recomendadas (§5).

Este plan amplía `docs/landing-redesign-plan.md`. Todo lo de su §0 sigue en
pie, con una excepción: la §0 decía que en `/roadmap` no había ningún
momento animado, y ahora hay uno. También deja sin efecto la crítica 16 de
ese plan («iconos de sistema: fila de texto, sin imagen»), porque ahora
Miguel los pide de forma explícita. Lo que sigue igual:

- la gramática del hueco: discontinuo = aún no; sólido = hecho; lomo Buckram
  = lo hizo Coverly; pestaña Manila = se puede deshacer;
- ni colores ni tipografías nuevos;
- las animaciones son ilustradas y se hacen con piezas de la página;
- se paran al pasar el ratón, con el foco, fuera de pantalla, con la pestaña
  oculta y con `cr-halt`;
- con movimiento reducido se queda el fotograma final;
- todas tienen un botón para saltarlas o repetirlas;
- paridad es/en;
- nada de enlaces a ROMs, claves ni emuladores;
- `make check` en verde con la app delante.

---

## 1. Los sistemas en la home

### 1.1 Conclusión legal: se pueden mostrar siluetas, no logos

No es asesoría legal. Es la práctica habitual y la investigación con
fuentes está en el anexo A. En resumen:

- **Nombrar un sistema para decir que somos compatibles es uso nominativo.**
  - En EE. UU. lo cubre el test de *New Kids on the Block* (9.º Circuito,
    1992), aplicado en *Playboy v. Welles* (2002). Sus tres condiciones:
    1. el producto no se puede identificar sin nombrarlo;
    2. se usa solo lo necesario;
    3. no se insinúa patrocinio.
  - En la UE lo cubre el uso referencial: art. 14(1)(c) del Reglamento
    2017/1001 y art. 14 de la Directiva 2015/2436 (en España, la Ley de
    Marcas). Exige «prácticas leales».
  - Con el nombre en texto basta. Un **logo** gráfico ya cuesta defenderlo
    como «lo necesario» y se acerca a sugerir respaldo.
- **Los fabricantes lo dejan claro.**
  - Microsoft: «Don't use Microsoft's logos, icons, or designs». Sus marcas
    de palabra sí se pueden usar en texto.
  - Nintendo rechaza las peticiones de uso.
  - Sony protege el Family Mark y las formas de los botones de PlayStation,
    y ha actuado contra dbrand.
- **Lo que mostramos no son logos.** Son las siluetas monocromas de hardware
  del tema XMB Monochrome de RetroArch Assets (CC BY 4.0, © libretro
  contributors), las mismas que la app ya lleva.
  - Su `src/assets/system-icons/README.md` audita las 89 una a una: sin
    logos, sin wordmarks, sin los símbolos de los botones de PlayStation,
    sin el anillo de Xbox y sin el remolino de Dreamcast.
  - Los iconos que eran logos o arte de juegos (CP System, MAME, DOS,
    ScummVM, DOOM, Quake…) no se incluyeron, y tampoco los que no se leen
    pequeños (Vectrex, CDTV, CPC, Channel F, Intellivision). Esos sistemas
    llevan la abreviatura de la app.
- **CC BY 4.0 no da derechos de marca** (sección 2(b)(2)). Por eso ponemos
  a la vez el crédito de la licencia y un aviso de no afiliación.
- **Batocera y Delta**, que hacen algo parecido, nombran los sistemas sin
  logos. LaunchBox reparte «clear logos» oficiales sin licencia: no lo
  copiamos.

**Reglas que se aplican:**

1. Solo las 89 siluetas de la app, sin cambios en el dibujo. Los otros 42
   sistemas llevan la abreviatura de la app (`systemFallbacks.ts`).
   Nunca se añade un icono que la app no tenga.
2. Cada icono va siempre con el nombre del sistema escrito, tal como lo
   escribe la app: sin ™, sin cambiar el nombre y sin «compatible oficial».
3. «Xbox» solo aparece como nombre de sistema, igual que en el plan de la
   primera ronda.
4. Al pie del bloque, en los dos idiomas, van dos textos:
   - **Aviso:**
     - «Coverly no está afiliado ni respaldado por Nintendo, Sony,
       Microsoft, Sega ni ningún otro fabricante. Los nombres de los
       sistemas son marcas de sus dueños y aquí solo dicen con qué
       funciona.»
     - *«Coverly is not affiliated with or endorsed by Nintendo, Sony,
       Microsoft, Sega or any other maker. System names are trademarks of
       their owners, used here only to say what it works with.»*
   - **Crédito:**
     - «Iconos de sistemas adaptados de RetroArch Assets (tema XMB
       Monochrome), © libretro contributors, CC BY 4.0. Cambios:
       recoloreados, optimizados y recortados.»
     - Enlaces: la licencia y el commit `d9f9690` del repositorio de
       assets. Es un enlace a GitHub de libretro/retroarch-assets, que solo
       tiene arte de menús: no es un sitio de emuladores ni de ROMs.
   - El mismo crédito se añade a `llms.txt` y a la sección de créditos del
     pie, si la hay.

### 1.2 Dónde va: en `#formatos`, como una estantería y no como un muro de logos

El bloque sustituye a la lista `.fams` («131 sistemas, por familia») al
final de `#formatos` («Escribe donde tu consola busca»). Esa sección ya
habla de las carpetas que usa cada sistema y ya enseña los recuentos por
familia.

No va justo debajo del hero. Una franja de logos bajo el hero es el «trusted
by» de cualquier SaaS. Además, quitaría peso a las portadas, que tienen que
seguir ocupando ~29 % de la home (§5).

```
#formatos ─────────────────────────────────────────────────────────
 Escribe donde tu consola busca.
 [tabla de formatos]            [galería de perfiles]
 ── 131 sistemas, con su carpeta ──────────────────────── [Pausar] ─
 ◀ ▢ GBA  ▢ SNES  ▢ PS2  [CPS1] ▢ Mega Drive  ▢ Lynx  ▢ 3DS  …    (fila 1 →)
 ══════════════════════════════════════════════ regla de estantería
  … ▢ Saturn  [DOS]  ▢ Amiga  ▢ PC Engine  ▢ Wii  ▢ Neo Geo ▶     (fila 2 ←)
 ══════════════════════════════════════════════
 ▸ Ver los 131 sistemas      (details)
   [ Buscar sistema…      ]  Todos 131 · Consolas 50 · Portátiles 20 · …
   Consolas · 50
     Nintendo 17   ▢ Nintendo Entertainment System  ▢ Super Nintendo …
     Sega 11       ▢ Master System  ▢ Mega Drive …
   …
 Aviso de no afiliación · Crédito CC BY
```

### 1.3 Carrusel: dos baldas que se mueven en sentido contrario

- **Qué se ve.**
  - Dos filas, cada una sobre su regla de estantería con el remate Buckram.
    Es la misma regla de los títulos.
  - Cada sistema es una placa con su silueta en `--cr-text-secondary` y su
    nombre corto debajo, en Archivo a ancho 75.
  - Los sistemas sin silueta llevan una **placa con la abreviatura**. Es el
    mismo recurso que la app (el «Slot mount»), así que no se nota que
    falta un dibujo.
- **Reparto.**
  - Fila 1: consolas y portátiles (70).
  - Fila 2: ordenadores, arcade y motores (61).
  - El orden es el de `systems.toml`, que ya agrupa por fabricante.
- **Movimiento.**
  - CSS `@keyframes` sobre `transform: translateX()` de la pista. Se anima
    solo `transform`, que está en `MOVES`.
  - Una vuelta tarda unos 90 s (≈ 30 px/s). Es lento a propósito: es
    ambiente, no un reclamo.
  - La fila 2 usa `animation-direction: reverse`.
  - JS clona la pista una vez para que el bucle no tenga costura. El clon
    lleva `aria-hidden` e `inert`.
- **Pausa.** Se para al pasar el ratón por el carrusel, cuando algo dentro
  tiene el foco, fuera de pantalla (`[data-off]` del observador común), con
  la pestaña oculta y con `cr-halt`.
- **Botón «Pausar» / «Reanudar».** Es obligatorio por WCAG 2.2.2, porque el
  contenido se mueve más de 5 s.
  - Es un botón con `aria-pressed`, a la derecha de la cabecera del bloque.
  - Se recuerda en `sessionStorage`, dentro de un `try` por si falla.
- **Accesibilidad.**
  - El carrusel entero es decorativo: `aria-hidden="true"` sobre las dos
    pistas.
  - La lista accesible e indexable es el buscador de §1.4, que siempre
    está en el HTML. Así el lector de pantalla no oye 131 nombres en
    movimiento.
- **Movimiento reducido.** No hay animación. Las dos filas se quedan quietas
  y se pueden desplazar a mano (`overflow-x: auto`, `scroll-snap`). El
  botón de pausa no aparece.
- **Sin JS.** No hay carrusel, porque las placas se crean desde la lista.
  La lista completa se sigue viendo.

### 1.4 La lista completa: un `<details>` con buscador, agrupada por familia y fabricante

- **Estructura.**
  - `<details class="sys-all"><summary>Ver los 131 sistemas</summary>`.
    Viene cerrado, así que no cuenta en la altura de la home.
  - Dentro, un `<input type="search">` con su `<label>` y los botones de
    familia como **filtro**: «Todos 131», «Consolas 50», «Portátiles 20»,
    «Ordenadores 27», «Arcade 15», «Motores, ports y consolas de fantasía
    19».
  - Los filtros son botones con `aria-pressed`, no pestañas: filtran una
    misma lista.
  - Los recuentos salen de `data-fact`, igual que hoy.
- **Grupos.** Cada familia es un `<section>` con su `<h4>` y su recuento.
  - En consolas, portátiles y ordenadores hay subgrupos por fabricante
    (Nintendo 17, Sega 11, Atari 8…).
  - Arcade y motores van en orden alfabético, porque en ellos el
    «fabricante» es una placa, un motor o un juego.
- **Cada sistema** es un `<li>` con su placa y su nombre:
  - `<li data-k="gba advance"><i data-i="gba"></i>Game Boy Advance</li>`
  - `data-k` lleva hasta 3 alias cortos de la app (≤ 8 caracteres), para
    que «gba», «md» o «pce» también encuentren el sistema.
  - Sin silueta: `<i data-a="CPS1"></i>`. El CSS pinta la abreviatura con
    `content: attr(data-a)`, así que funciona también sin JS.
- **Buscador.**
  - Filtra por nombre, alias y fabricante, sin distinguir mayúsculas ni
    acentos (`normalize("NFD")`).
  - Oculta los grupos que se quedan vacíos.
  - Anuncia «12 sistemas» en un `role="status"`.
  - Si no hay resultados, dice qué hacer: «Ningún sistema se llama así.
    Prueba con el nombre de la consola o con su carpeta (gba, snes…).»
  - Con `Escape` se vacía el campo.
- **Nombres en es/en.**
  - Los nombres de sistema son nombres propios. La app los muestra igual en
    los dos idiomas, así que la landing también.
  - Se traducen las familias, los fabricantes genéricos («Otros») y todos
    los textos del bloque.
- **Sin JS.** El `<details>` se abre y muestra la lista agrupada. El
  buscador y los filtros llevan `hidden` hasta que el JS los activa.
- **Era.** La app no guarda años. Inventar una tabla de fechas sería un
  dato sin fuente que nadie comprueba, así que no agrupamos por era.

### 1.5 Iconos: un sprite que se carga solo cuando hace falta

- `scripts/site/systems.py --write` lee de la app:
  - `crates/coverly-core/src/systems/systems.toml` (con `tomllib`);
  - `src/components/system/systemIcons.generated.ts` (ids, `viewBox`,
    `body`);
  - `src/components/system/systemFallbacks.ts` (`FALLBACK_ABBR`).
- Escribe dos archivos:
  - `site/data/systems.json`: `schema`, `source` (commit de la app y
    sha256 de los tres archivos), y por sistema `id`, `name`, `family`,
    `maker`, `keys`, `icon` (bool) y `abbr`;
  - `site/assets/art/systems.svg`: un `<symbol>` por silueta, con
    coordenadas redondeadas a 1 decimal, sin `fill` (lo hereda de
    `currentColor`) y con la cabecera CC BY dentro como comentario XML.
    Medido: 89 símbolos ocupan 129 KB sin comprimir y 35 KB en gzip, frente
    a 148 KB y 44 KB con 3 decimales.
- Regenera los bloques `<!-- systems:begin -->…<!-- systems:end -->` de
  `site/index.html` y `site/en/index.html`.
- **Fabricante.**
  - Sale del prefijo de `libretro` («Nintendo - Game Boy» → «Nintendo»).
  - Una tabla corta en el script corrige los 20 sistemas sin `libretro` y
    los prefijos que no son fabricantes (MAME, DOS, FBNeo, títulos de
    juegos). Esos van a «Otros».
  - La tabla tiene su test.
- **Carga diferida.**
  - El HTML no referencia el sprite. Las placas son `<i data-i>` vacías,
    que se ven como hueco discontinuo: un hueco a la espera de su dibujo.
  - `assets/systems.js`, con su `IntersectionObserver` y
    `rootMargin: 800px`, cambia cada `<i data-i>` por
    `<svg><use href="assets/art/systems.svg#gba"/></svg>`. Lo hace al
    acercarse a `#formatos` y al abrir el `<details>`.
  - El navegador pide el sprite una sola vez y lo guarda en caché. Es del
    mismo origen, así que la CSP no cambia.
  - Con movimiento normal, cada placa pasa de discontinua a sólida al
    llegar su icono. Es la gramática del hueco aplicada a los sistemas.
    Con movimiento reducido, aparece sin más.
- **`assets/systems.js`** (≤ 2 200 B) hace cuatro cosas:
  - el cambio de placas;
  - el clon de las pistas;
  - el botón de pausa;
  - el buscador y los filtros.

  Lo cargan solo las dos homes.

### 1.6 Guardias en `make check`

- **`systems.py --check [--app RUTA]`.** Se llama desde `check` como
  `roadmap.py`.
  - Sin la app, comprueba:
    - que el JSON, el sprite y los bloques HTML de los dos idiomas cuadran
      entre sí;
    - que cada `data-i` tiene su `<symbol>`;
    - que cada `data-a` es la abreviatura del JSON;
    - que `facts.json` (`systems`, `families.*`) coincide con el JSON.
  - Con la app, además:
    - que ids, nombres, familias y orden son iguales a `systems.toml`;
    - que el conjunto de iconos es exactamente el de
      `systemIcons.generated.ts`, y cada `<symbol>` es su `body` redondeado
      (por hash);
    - que las abreviaturas son las de `FALLBACK_ABBR`.
  - Si algo se ha desviado, falla con el comando para arreglarlo:
    `make systems`.
- **`check_site.py --only systems`** (puerta nueva):
  - el aviso y el crédito están en los dos idiomas, con los enlaces a la
    licencia y al commit;
  - no hay `™` ni `®` en el bloque;
  - el sprite solo tiene ids de la app;
  - ningún `<use>` del HTML inicial apunta a `systems.svg`, para que la
    carga diferida no se pierda sin que nadie se entere.
- **`motion`.** La pista del carrusel solo anima `transform` y está dentro
  de `html.motion`. Se comprueban también las pausas `[data-off]`, `:hover`
  y `:focus-within`, y el bloque de movimiento reducido.
- **`Makefile`.** Se añaden `make systems` (regenera desde `APP`) y
  `systems-check`.

---

## 2. Duplicados: la escena que aparta las copias

La captura de `#ordenar` se cambia por una escena ilustrada.

- **Piezas.** Todas existen ya:
  - la ilustración `.dup` de `/features`, con sus piezas de `kit.svg`
    (`sm`, `sf`, `spine`, `folder`, `ftab`, `tab`) y la portada `c-23` de
    `covers.svg`;
  - la geometría de la escena `SetAsideScene` de la app: 5 huecos 3:4
    sobre una regla, a 40 px de paso, y una carpeta con pestaña Manila.

  Es lo mismo que hicimos con el comprimido, que copia la ilustración de la
  app #30.
- **Los textos** salen tal cual de `locales/*/ui.json` de la app:
  - «Se queda: tiene portada; la otra no.» / «Stays: it has a cover; the
    other doesn't.»;
  - «Copia exacta» / «Exact copy»;
  - el nombre de carpeta `_Duplicados`, que la app usa igual en los dos
    idiomas (la home en inglés ya lo escribe así).
- **CSS.** Las reglas `.dup*` pasan de `pages.css` a `site.css`, para que
  la home y `/features` compartan escena. La de `/features` usa los mismos
  tiempos.

### Storyboard (≈ 7 s por vuelta)

| Tiempo | Qué pasa | Cómo se mueve |
|---|---|---|
| 0–1,2 s | Una balda con 5 portadas de un sistema. Tres son la misma (`c-23`). | Fotograma de partida. |
| 1,2–2,4 s | Una línea de lectura recorre la balda. Bajo las tres iguales aparece la misma huella (un `stag` con 4 bloques iguales) y la etiqueta «Copia exacta». | `transform` de la línea; `opacity` de las etiquetas. |
| 2,4–3,6 s | Una de las tres recibe el lomo Buckram (`spine`) y su motivo: «Se queda: tiene portada; la otra no.». | `clip-path` del lomo; `opacity` del texto. |
| 3,6–5,0 s | Las otras dos se levantan y caen en la carpeta `_Duplicados` (240 ms de subida y 400 ms de caída, como la app, con 250 ms entre una y otra). Sus huecos se quedan discontinuos un momento y la balda se cierra. | `transform` (subida y caída); `opacity` del hueco. |
| 5,0–6,2 s | Aparece la pestaña Manila «Deshacer» sobre la carpeta. | `transform: rotate` de la pestaña, la misma que en el hero. |
| 6,2–7,0 s | Deshacer: las dos copias vuelven a su sitio y la vuelta empieza otra vez. | Lo inverso de 3,6–5,0. |

- **Reproducción.**
  - Arranca al entrar en pantalla, con el observador común y `data-clip`.
  - Da **dos vueltas** y se queda en el fotograma de 5,0–6,2: copias
    apartadas y pestaña de deshacer a la vista. Ese fotograma es el que
    cuenta la frase «sin borrar nada».
  - «↻ Repetir» la vuelve a lanzar. Hay pausa con el ratón, el foco, fuera
    de pantalla y con la pestaña oculta.
- **Movimiento reducido.** Se ve directamente el fotograma final.
- **Accesibilidad.** La figura lleva
  `role="img" aria-label="Ilustración: tres copias del mismo juego en una
  balda. Una se queda porque tiene portada; las otras dos van a la carpeta
  _Duplicados y la pestaña Deshacer puede devolverlas."`. Debajo va el pie
  «Ilustración, con el texto de la propia app.», como el del comprimido.
- **Peso.** La escena inline ocupa unos 3 KB en crudo y 0,8 KB en gzip.
  Sale el `<picture>` (unos 1,3 KB de HTML) y la home deja de pedir dos WebP
  de 33–34 KB cada uno.
- **Lo que no se hace.** No hay un temblor de las copias al marcarlas.
  Tiembla lo que va mal, y aquí no va nada mal.

---

## 3. `/features`: escenas fijas que avanzan con el texto

### 3.1 Patrón

Es el mismo patrón que usan Apple, Stripe y Linear (anexo B): una columna
con la ilustración fija y otra con el texto, que pasa por debajo.

- En pantallas de 1024 px o más, cada grupo pasa a dos columnas:
  - **izquierda:** la figura del grupo, `position: sticky` con
    `top: calc(var(--header) + 24px)`;
  - **derecha:** la `<dl class="flist">`.
- Las funciones de cada grupo se agrupan en **3–5 tiempos**. La primera
  `<div>` de cada tiempo lleva `data-beat="n"`. Cuando ese tiempo llega a la
  franja de lectura (entre el 35 % y el 55 % del viewport), la escena pasa a
  su estado `n`.
- **El scroll no se secuestra.** La página se desplaza al ritmo normal: no
  hay `scroll-snap` obligatorio, ni `wheel` interceptado, ni secciones
  fijadas que alarguen la página. La figura simplemente se queda pegada
  mientras su grupo está en pantalla.

### 3.2 Cómo avanza

1. **Donde hay animaciones ligadas al scroll** (`@supports
   (animation-timeline: view())`: Chrome/Edge 115+, Safari 26+, Firefox
   159+):
   - cada `[data-beat]` declara `view-timeline: --bN`;
   - el grupo declara `timeline-scope: --b1, --b2, …`;
   - cada parte de la escena se anima contra el tiempo que le toca
     (`animation-timeline: --b2; animation-range: entry 35% cover 50%`).

   El avance sigue al scroll y lo hace solo el CSS.
2. **Si no hay soporte**, `toc.js`, que ya observa los grupos para el
   índice, observa también los `[data-beat]` con `rootMargin: "-35% 0px
   -45% 0px"` y pone `data-beat` en la figura. Las transiciones CSS hacen
   el cambio. No se escucha el evento `scroll`. `toc.js` pasa de 922 B a
   ≤ 1 900 B.
3. **Teclado.** Cuando el foco entra en un tiempo (`focusin`), la escena va
   a ese tiempo, aunque el scroll no haya llegado.
4. **Movimiento reducido.**
   - La figura sigue fija, porque es composición y no movimiento.
   - Los tiempos cambian por **corte** (sin transición y sin scrub), con el
   mismo observador.
   - `document.getAnimations()` sigue en 0.
5. **Menos de 1024 px.** No hay sticky. La figura va debajo de la cabecera
   del grupo, como hoy, y se reproduce de una vez al entrar (el `data-clip`
   actual), con ↻.
6. **Saltar.** Un enlace «Saltar a la lista» antes de cada figura fija,
   visible con el foco. El índice de lomos ya permite saltar de grupo en
   grupo.
7. **Lectores de pantalla.**
   - Cada figura conserva su `role="img"` con una descripción del grupo
     entero.
   - El estado de cada tiempo **no** se anuncia, porque la lista ya dice lo
     mismo.
   - El texto nunca se oculta.

### 3.3 Escenas y tiempos por grupo

Cada escena se hace con lo que el grupo ya tiene. Lo nuevo son los estados.

| Grupo | Escena (existe) | Tiempos → estado |
|---|---|---|
| Portadas y arte (11) | Cascada `.cascade` | 1 Auditoría, Identificación: huecos discontinuos contados, la huella aparece. 2 Simulación, Cola: la cola de dudosas con 3 candidatas. 3 Región y orden, SteamGridDB, Portada del propio juego: la cascada baja de fuente en fuente. 4 Nombres, Cambiar a mano, Imágenes limpias, Ritmo: la portada se escribe, recibe el lomo y la pestaña Deshacer. |
| Consolas y formatos (6) | Galería `.galfig` | 1 Ocho formatos: los perfiles se encienden uno a uno. 2 Tu propio formato, gamelist.xml: la vista previa del formato propio. 3 131 sistemas, Un icono, Nombres: la balda pasa a placas de sistema (las del carrusel, desde el sprite). |
| Ordenar (9) | Comprimido `.arcfig` | 1 Ordenar, Comprimidos: el zip se abre. 2 Disco, Carpeta, Multidisco: pistas que pasan a sólidas con ✓, y el `.m3u`. 3 10 GB, Actualizaciones, Consolas actuales, Catálogo: aviso de tamaño y candado «Cifrado» sin claves. |
| Duplicados (6) | `.dup` (la de §2) | 1 Por contenido: huella. 2 Reglas: el lomo y el motivo. 3 A _Duplicados, Partidas distintas: las copias se apartan y la que tiene partidas distintas se queda con un candado. 4 Title ID, Ficha: la ficha de la copia. |
| Biblioteca y vistas (5) | Ventana `.vw` | Cada tiempo es una vista (`deck.js` con `go(n)`). Los botones siguen ahí y mandan si los pulsas. |
| Terminal (6) | **Nueva, pequeña:** el bloque de terminal de `#terminal` (`--cr-code-bg`) | Cada orden se escribe cuando llega su tiempo, con la escritura de `motion.js`. En reducido, todo escrito. |
| Ajustes y confianza (6) | `.trustfig` | 1 Sin cuenta: el candado. 2 Versiones firmadas: el sello minisign. 3 Agradecimientos, Ajustes, Una descarga, Idiomas: las pestañas de Ajustes. |

- Solo se anima `transform`, `opacity`, `clip-path` y `stroke-dashoffset`.
- `motion.js` no crece. La escritura de la terminal se reutiliza llamando a
  `cr-type` sobre el elemento.

---

## 4. `/roadmap`: la estantería de la hoja de ruta

### 4.1 Lo que hace la industria (anexo B) y qué tomamos

| Patrón | Quién | Lo bueno | Lo que no nos sirve |
|---|---|---|---|
| Tablero por trimestres + «Exploratory», con fases alpha/beta/GA | GitHub public roadmap | Fases claras | Fechas por trimestre que no tenemos |
| **Now / Next / Later** | ProdPad (Janna Bastow), Linear, Productboard, Canny | Agrupa por confianza, no por fecha. Es el estándar. | Suele ser tres columnas de tarjetas (el kit SaaS) |
| Entregado / Corto / Medio plazo + aviso | Dyad, Bun | Honesto | Solo texto |
| Documentos de foco mensual / changelog | Raycast, Supabase | Ritmo | No es visual |
| Mapa de metro | MetroViz, metro-map-builder | Dependencias | Con 9 puntos abiertos queda escaso, a 360 px no se lee y tiene aire de presentación corporativa |
| Librerías (vis-timeline ≈ 114 KB gz, frappe-gantt, react-chrono, markwhen) | — | — | Peso, estética Gantt, React o un paso de compilación. Chocan con «sin instalación». |

**Decisión.** Una **estantería** que combina el historial entregado con
Ahora / Después / Más adelante, hecha a mano en HTML y SVG y generada desde
`roadmap.json`. Es la gramática de la marca: la hoja de ruta es una balda
que se va llenando de portadas.

### 4.2 Cómo se ve

```
 Entregado                       Hoy │ Ahora           Después              Más adelante
 ┌──┐ ┌──┐  ╱▔▔╲                    │ ▣ ▣ ▣           ▤ ▢ ▤                ▢ ▢ ▢
 │01│ │02│ ╱ próx ╲                  ▼ ARM64 Sistemas  DLC  Title ID Front.   Biblio Sinc Partidas
 └──┘ └──┘                         ┃   3/5   65/69    0/15  1/28   1/18     0/32  0/20  0/17
═══════════════════════════════════╋═════════════════════════════════════════════════════
 17 oct  25 oct  en el código        Agradec. 7/8       ╰──── 2.1 ──→ 3 ──→ 4, 5 ────╯
```

- **La regla.** Una regla horizontal de ancho completo con el remate Buckram
  a la izquierda, la de los títulos. Se lee de izquierda a derecha.
- **Entregado.**
  - Cada versión publicada es una **portada sólida de pie**, con el lomo
    Buckram, la etiqueta de versión (`vtag`) y su fecha `<time>` debajo.
  - La «Próxima versión» es **The Lean-To**, la portada apoyada en diagonal
    del hero, porque está hecha pero aún no está colocada. No lleva fecha.
  - Cada versión enlaza a su bloque de texto (`#v0-2-0`).
- **Hoy.** Un marcador vertical con la pestaña Manila y la palabra «Hoy».
  Es la única marca de tiempo del futuro.
- **Ahora / Después / Más adelante.** Son tres tramos separados por
  sujetalibros. Cada punto abierto es un **hueco 3:4** que se llena desde
  abajo según su progreso (`done/total`):
  - discontinuo si está a 0;
  - en `--cr-slot-filled` lo hecho;
  - con un ✓ al 100 %.
  - Debajo, el título corto y «3 de 5».
  - El hueco entero es un enlace (`<a href="#rm-2-1">`) a su ficha de
    texto.
- **Reparto en tramos.** Sale del `status` del JSON, sin tocarlo a mano:
  - **Ahora:** `verifying`, `almost` → 0, 2, 7;
  - **Después:** `research`, `planned` → 2.1, 3.1, 6;
  - **Más adelante:** `blocked` → 3, 4, 5. `parked` no sale en la balda,
    solo en el texto.

  Dentro de cada tramo, el orden es el del JSON.
- **Dependencias.**
  - Arcos discontinuos por encima de los huecos, de `after` → `id`
    (2.1 → 3; 2.1 y 3 → 4 y 5), con la punta en forma de pestaña.
  - Al pasar el ratón por un hueco o enfocarlo, se resaltan sus arcos y
    los huecos de los que depende. El resto baja a `opacity: .35`.
  - Es una respuesta a lo que haces, no un adorno.
- **Leyenda.** Una línea: «Lleno: hecho. Discontinuo: aún no. La altura es
  la parte hecha. Sin fechas hasta que haya versión.»
- **Móvil (< 720 px).**
  - La balda pasa a **vertical**: la regla es una línea a la izquierda, con
    las versiones arriba y los tramos debajo.
  - Cada hueco es una fila: hueco, título y «3 de 5».
  - Los arcos se cambian por el texto «Espera a: …», que ya existe.

### 4.3 Estructura (una sola, accesible, sin capas duplicadas)

```html
<figure class="rm-shelf" data-clip-box>
  <ol class="rm-line" aria-label="Hoja de ruta">
    <li class="rm-v" data-state="released">…v0.1.0, <time>…</time></li>
    <li class="rm-v" data-state="unreleased">…Próxima versión</li>
    <li class="rm-today">Hoy</li>
    <li class="rm-bay" data-bay="now"><h3>Ahora</h3><ol>
      <li><a href="#rm-0" class="rm-slot" style="--p:.6">…ARM64 <span>3 de 5</span></a></li>…
    </ol></li>
    …
  </ol>
  <svg class="rm-deps" aria-hidden="true" …><!-- arcos, generados --></svg>
  <figcaption>leyenda + ↻</figcaption>
</figure>
```

- **Composición.**
  - En escritorio, `.rm-line` es una rejilla con columnas fijas: versiones,
    hoy y 9 huecos.
  - El SVG de arcos usa la misma rejilla en su `viewBox`, con
    `preserveAspectRatio="none"` y `vector-effect: non-scaling-stroke`.
  - `roadmap.py` calcula las posiciones desde el JSON.
- **CSP.** `style="--p:.6"` choca con `style-src 'self'`. En su lugar,
  `roadmap.py` genera **clases** `.p0`…`.p20` (pasos del 5 %) en
  `pages.css`, o pinta el relleno como un `<rect>` dentro del mini SVG de
  cada hueco. Elegimos el `<rect>`: no hace falta CSS nuevo por cada valor y
  el hueco ya es un SVG.
- **Títulos cortos.** `roadmap.json` gana un campo `short` (es/en, ≤ 22
  caracteres) en cada punto de `next`.
  - `roadmap.py --update` lo conserva.
  - `--check` falla si falta o se pasa de largo.
- **Generación.** El bloque `<!-- roadmap:shelf:begin -->…end` lo genera
  `roadmap.py`, igual que los demás bloques. `make check` comprueba que el
  HTML sale del JSON.
- **El texto sigue debajo.** «Entregado», «Lo que viene» y las fichas no
  cambian. La estantería resume y las fichas detallan.

### 4.4 El momento animado de `/roadmap`

Es uno solo y se reproduce una vez al entrar.

1. La regla se dibuja (`stroke-dashoffset`).
2. Las portadas entregadas caen en su sitio (`transform`).
3. The Lean-To se apoya.
4. Los huecos se llenan hasta su progreso (`transform: scaleY` desde
   abajo).
5. Los arcos se dibujan.

Dura unos 2,4 s. Lleva ↻, se para con el ratón, el foco o fuera de
pantalla, y con movimiento reducido se ve el estado final. Con soporte de
`view()`, el llenado sigue al scroll; sin él, lo dispara `data-clip`.

---

## 5. Las cuatro decisiones delegadas

1. **Las portadas siguen siendo la apertura y la sección más grande.**
   - La medida de control de la §0 del primer plan pasa del 40 % a un
     **mínimo del 28 %**. Hoy está en ~29 %: hero, `#como` y `#seguro` sobre
     la altura total, a 1440×900.
   - El carrusel suma unos 230 px. La escena de duplicados mide lo mismo
     que la captura. El `<details>` cerrado suma unos 56 px.
   - Si al medir sale por debajo del 28 %, se hace más bajo el carrusel
     (placas de 40 a 32 px) antes de tocar las portadas.
2. **Windows ARM64 en la comparativa: «x64 y ARM64 (beta)»** (es y en:
   «x64 and ARM64 (beta)»).
   - Nadie lo ha probado en hardware real, y así lo dice el punto 0 de la
     hoja de ruta.
   - Las tarjetas de descarga no cambian. La FAQ ya avisa de que no se ha
     probado en consolas.
3. **Squash merge al final.** Por ahora no hay nada que hacer. El PR #8
   sigue abierto y no se mergea.
4. **Títulos de los pasos (`#como`).** Ya no hay botones dentro de los
   `<h3>`.
   - El `<h3>` de cada paso es texto: «1 Abre la tarjeta.».
   - En pantallas de 1024 px o más, `deck.js` añade el patrón **Tabs** de
     WAI-ARIA:
     - una `role="tablist"` con 4 `<button role="tab" aria-selected
       aria-controls>`;
     - cada paso es un `role="tabpanel"` con `aria-labelledby` apuntando a
       su `<h3>`;
     - las flechas ← → y las teclas Inicio/Fin con *roving tabindex*.
   - Las pestañas se generan desde el HTML, así que no hay copy duplicado.
   - Por debajo de 1024 px y sin JS no hay tablist, ni roles, ni botones
     desactivados: los cuatro pasos van uno debajo de otro con sus
     encabezados.
   - Al cruzar el *media query*, `deck.js` pone y quita roles y atributos.
   - Las otras dos barajas (vistas y terminal) se quedan como un grupo de
     botones con `aria-pressed`: son selectores de una ilustración, no
     pestañas con paneles.
   - `deck.js` pasa de un tope de 3 600 a 4 100 B.

---

## 6. Presupuestos

Medidos sobre `target/site` en las 4 variantes de la release el
2026-11-02. Se usa el peor caso, `release-new`.

| Qué | Hoy (medido / tope) | Previsto | Tope nuevo | Por qué |
|---|---|---|---|---|
| Home es/en, crudo/gzip | 88 287 / 20 505 de 90 000 / 21 000 | ≈ 97 500 / 23 600 | **100 000 / 24 000** | La lista de 131 sistemas, agrupada y con alias (≈ 8 KB / 2,4 KB), y la escena de duplicados (+3 KB). Sale el `<picture>` (−1,3 KB). |
| Palabras de la home | 2 528 de 2 600 | ≈ 2 920 | **3 000** | 131 nombres y las cabeceras de grupo (≈ 400), el aviso y el crédito (≈ 60). Salen el alt y el pie de la captura (≈ 45). Es lista de consulta dentro de un `<details>` cerrado, no texto para leer seguido. |
| `site.css` + tokens | 95 502 / 21 369 de 96 000 / 21 600 | ≈ 102 400 / 22 900 | **104 000 / 23 200** | El carrusel y la lista (≈ 3,5 KB), la escena `.dup` (pasa de `pages.css` y se amplía, ≈ 2,8 KB) y las pestañas de los pasos (≈ 0,6 KB). |
| `pages.css` | 7 228 / 2 314 de 10 000 / 2 800 | ≈ 13 000 / 3 600 | **14 000 / 3 900** | Sale `.dup` (−1,8 KB). Entran las escenas fijas y sus tiempos (≈ 4 KB) y la estantería de la hoja de ruta (≈ 3,5 KB). |
| Scripts (todos) | 30 919 / 9 556 de 31 500 / 9 900 | ≈ 34 300 / 10 700 | **35 500 / 11 000** | `systems.js` ≤ 2 200 (tope propio `SYSTEMS_JS`), `toc.js` +1 000 por los tiempos y `deck.js` +500 por las pestañas (`DECK_JS` 4 100). |
| `assets/art/systems.svg` | — | 129 000 / 35 000 | **132 000 / 36 000** (tipo nuevo `systems_art`, fuera de `art`) | 89 siluetas a 1 decimal. Solo se pide cerca de `#formatos` (§1.5), nunca en la primera carga. La home deja de pedir el WebP de duplicados (33–34 KB a 1×, 80–83 KB a 2×), así que lo transferido queda parecido. |
| `/features` | 41 700 / 10 847 de 72 000 / 17 000 | ≈ 48 000 / 12 500 | sin cambio | `data-beat`, los estados nuevos y la escena de terminal |
| `/roadmap` | 19 330 / 5 213 de 34 000 / 8 500 | ≈ 27 000 / 7 000 | sin cambio | La estantería y los arcos |
| Palabras `/roadmap` | 833 de 1 200 | ≈ 910 | sin cambio | Títulos cortos y leyenda |

Cada subida va con su comentario en `BUDGET`, como las anteriores.

---

## 7. Plan de trabajo

Commits pequeños, cada uno con su push y con `make check` en verde antes
de subirlo.

1. `docs: add landing round 2 plan` (este archivo).
2. `fix(site): accessible step tabs without buttons in headings` (§5.4).
3. `fix(site): mark Windows ARM64 as beta in the comparison` (§5.2).
4. `feat(site): systems data, icon sprite and drift check from the app`:
   `systems.py`, sus tests, `systems.json`, `systems.svg`, `make systems` y
   el `check`.
5. `feat(site): browsable list of every supported system` (§1.4).
6. `feat(site): systems shelf marquee with pause control` (§1.3).
7. `feat(site): trademark notice and CC BY credit for system icons`
   (§1.1), también en `llms.txt`.
8. `feat(site): animated set-aside scene for duplicates` (§2): home, y
   `/features` con la escena compartida.
9. `feat(features): sticky scenes that follow the reading` (§3), un commit
   por cada 2–3 grupos.
10. `feat(roadmap): short titles and bays in roadmap.json` (§4.3).
11. `feat(roadmap): visual roadmap shelf above the text` (§4).
12. `chore(site): budgets and gates for round 2` (§6) y
    `docs(landing): document round 2` en `landing.md`, con la tabla de
    movimiento y los presupuestos.

**Verificación.** Con `make site SITE_PORT=8091`, que se para por puerto al
acabar, y Chrome DevTools:

- 1440×900 y 390×844, claro y oscuro, movimiento reducido sí y no, es/en;
- sin JS;
- con teclado: las pestañas de los pasos, el buscador, los filtros, la
  pausa del carrusel y los huecos de la hoja de ruta;
- 0 errores de consola;
- `getAnimations().length === 0` con movimiento reducido;
- CLS 0;
- el sprite no se pide en la primera carga (panel de red);
- la medida de las portadas, ≥ 28 %.

Al terminar, se actualiza el artefacto de revisión de Miguel en la misma
URL.

---

## 8. Crítica del plan y qué cambié

He revisado la primera versión contra el brief de Miguel y contra los
defectos típicos de una página genérica.

1. **El carrusel era un muro de logos bajo el hero** (el «trusted by» de
   cualquier SaaS), con logos a color.
   → **Cambio:** siluetas monocromas sobre dos baldas, colocadas en
   `#formatos`, donde ya se habla de sistemas. Las abreviaturas van en
   placas de hueco. Ni logos ni color de marca ajena.
2. **Un carrusel con 131 nombres en movimiento como única forma de ver la
   lista** no se lee y es un problema de WCAG 2.2.2.
   → **Cambio:** el carrusel es decorativo (`aria-hidden`), lleva botón de
   pausa y es lento. La lista real es el buscador agrupado, que también
   funciona sin JS.
3. **Agrupar por «era»** obligaba a inventar años que la app no tiene.
   → **Cambio:** familia y fabricante, que salen de los datos de la app, con
   alias en el buscador.
4. **Meter el sprite inline o cargarlo en la primera visita** costaba 35 KB
   en gzip en todas las cargas.
   → **Cambio:** placas vacías en el HTML y sprite cargado al acercarse, con
   tope propio y una puerta que avisa si alguien lo enlaza en la primera
   carga. Las placas vacías se ven como huecos discontinuos que se llenan,
   así que la espera usa la misma gramática del hueco.
5. **La escena de duplicados empezaba con las copias «temblando».**
   → **Cambio:** fuera. Tiembla lo que va mal y aquí no va nada mal. Se
   marca con una huella y con «Copia exacta», el texto de la app.
6. **La escena de duplicados iba en bucle infinito.** En la home ya está el
   hero como momento fuerte.
   → **Cambio:** dos vueltas y se queda en el fotograma que cuenta «sin
   borrar nada», con ↻.
7. **Escenas fijas en los 7 grupos, al estilo Apple:** muchas horas de
   trabajo y peligro de convertir `/features` en una presentación.
   → **Cambio:** sin secuestrar el scroll, sin secciones fijadas que
   alarguen la página y sin sticky en móvil. Las escenas se hacen con las
   figuras que ya existen; solo la terminal es nueva y es la más simple.
   El avance se resuelve en CSS donde hay soporte y con el observador que
   ya existe donde no.
8. **La hoja de ruta como tres columnas de tarjetas Now/Next/Later** (el
   kit SaaS) o como un Gantt con fechas inventadas.
   → **Cambio:** una sola balda. Lo entregado son portadas, lo próximo es
   The Lean-To y lo abierto son huecos que se llenan. Las fechas solo
   aparecen en lo publicado y los tramos se calculan solos desde `status`.
9. **Etiquetas en versalitas encima de cada tramo** («NOW», «NEXT»).
   → **Cambio:** «Ahora», «Después» y «Más adelante» en tipo de frase,
   dentro de la balda, como `<h3>` del tramo. Dicen algo (la confianza), no
   decoran.
10. **Una capa SVG decorativa y otra lista oculta para lectores de
    pantalla** duplicaban contenido y dejaban enlaces invisibles en el
    orden de tabulación.
    → **Cambio:** una sola estructura `<ol>` enlazable. El SVG solo dibuja
    los arcos (`aria-hidden`) y las dependencias también están en texto.
11. **`style="--p:…"` para el progreso** se habría saltado la CSP
    `style-src 'self'`.
    → **Cambio:** el relleno es un `<rect>` generado dentro del SVG de cada
    hueco.
12. **Subir presupuestos sin compensar.**
    → **Cambio:** cada subida lleva su cuenta. Sale la captura de
    duplicados de la home y `.dup` deja de estar duplicado entre hojas. El
    sprite va con tope propio y fuera de la carga inicial.
13. **Las pestañas en todas las barajas por coherencia.**
    → **Cambio:** solo en los pasos, que tienen panel con título propio.
    Vistas y terminal son selectores de una figura y se quedan con
    `aria-pressed`.
14. **Consejo de Chanel.** Había un brillo de color al pasar el ratón por
    cada placa del carrusel.
    → **Cambio:** fuera. El carrusel se para al pasar el ratón y eso basta.
    Lo memorable de la ronda es la estantería de la hoja de ruta. El resto
    es tranquilo.

---

## Anexo A. Fuentes legales

- Nominative use: https://en.wikipedia.org/wiki/Nominative_use
- *Playboy v. Welles*, 279 F.3d 796 (9th Cir. 2002):
  https://law.justia.com/cases/federal/appellate-courts/F3/279/796/506072
- Directiva (UE) 2015/2436, art. 14:
  https://www.legislation.gov.uk/eudr/2015/2436/article/14
- Reglamento (UE) 2017/1001: https://eur-lex.europa.eu/eli/reg/2017/1001/oj
- Microsoft Trademark and Brand Guidelines:
  https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks
- Nintendo, copyright y marcas:
  https://www.nintendo.com/en-gb/Legal-information/Copyright/Copyright-625949.html
- Sony Interactive, aviso de marcas:
  https://www.playstation.com/en-gb/legal/copyright-and-trademark-notice/
- CC BY 4.0, texto legal, sección 2(b)(2):
  https://creativecommons.org/licenses/by/4.0/legalcode
- RetroArch Assets: https://github.com/libretro/retroarch-assets
- Batocera: https://batocera.org/; Delta: https://faq.deltaemulator.com/
- En la app (solo lectura): `src/assets/system-icons/README.md`,
  `credits/credits.json` (`retroarch-assets`), `TRADEMARKS.md`,
  `THIRD-PARTY-NOTICES.md`.

## Anexo B. Fuentes de roadmap y movimiento

- GitHub public roadmap: https://github.com/github/roadmap
- Now / Next / Later (ProdPad): https://www.prodpad.com/glossary/now-next-later-roadmap/
- Janna Bastow, AMA:
  https://www.producthunt.com/p/general/ama-today-i-invented-the-now-next-later-roadmap-co-founded-mind-the-product-prodpad?page=2
- Dyad: https://www.dyad.sh/docs/roadmap · Bun: https://bun.sh/docs/project/roadmap.md
- Raycast, focus documents:
  https://www.plushcap.com/content/raycast/blog/raycast-monthly-focus-documents-instead-of-roadmaps
- MetroViz: https://github.com/rstockm/Metroviz
- vis-timeline, tamaño: https://depscope.dev/pkg/npm/vis-timeline
- MDN, `animation-timeline`:
  https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/animation-timeline
- Scroll al estilo Apple:
  https://ddingpy.github.io/mynote/posts/building-an-apple-style-scroll-experience-like-the-macbook-neo-page
- WAI-ARIA Tabs: https://www.w3.org/WAI/ARIA/apg/patterns/tabs/
- WCAG 2.2.2 Pause, Stop, Hide:
  https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html

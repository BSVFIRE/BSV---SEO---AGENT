# Higgsfield-prompter for BSV Fire

Higgsfield-koblingen i denne økta kan ikke generere media, så kjør promptene selv og legg filene i `site/assets/`
med filnavnene under. Siden bruker dem automatisk. Ingen tekst, logoer eller firmanavn skal være synlige i bildene.

Felles stil: realistisk dokumentarfoto/film, rolig kamera, norsk vestlandsstemning (regn, dis, fjell), moderne nordiske bygg,
nøytral oransje aksent i arbeidstøy, ingen leselige logoer eller tekst på utstyr, ingen kjente merkenavn.

## Film (MP4, H.264, 1920x1080, 5–8 sek, uten lyd, under ~4 MB)
| Fil | Prompt |
|---|---|
| `video/hero.mp4` + `img/hero-poster.jpg` | Servicetekniker i mørk arbeidsjakke kontrollerer en brannalarmsentral i teknisk rom i et moderne norsk næringsbygg. Rolig sakte kamerabevegelse, dagslys fra vindu, nøytrale paneler uten tekst. |
| `video/servicebil-bergen.mp4` + `img/film-servicebil-poster.jpg` | Hvit elektrisk varebil uten logo kjører på våt vei i Bergen, regn, Fløyen og fjell i dis, bryggen i bakgrunnen. Rolig sporingsbevegelse. |
| `video/sprinkler.mp4` | Nærbilde av tekniker som kontrollerer sprinklerrør og ventil i teknisk rom, rolig kamera. |
| `video/nodlys.mp4` | Mørk rømningsvei i moderne bygg, nødlys tennes ett for ett og lyser opp korridoren, rolig kamera. |

## Bilder (JPG, 1600x2000 for fliser, 1920x1080 for brede; under ~300 kB)
| Fil | Motiv |
|---|---|
| `img/tjeneste-brannalarm.jpg` | Tekniker ved brannalarmsentral (bredt, 16:9) |
| `img/tjeneste-boligalarm.jpg` | Trådløs alarmenhet på vegg i moderne norsk bolig |
| `img/tjeneste-sprinkler.jpg` | Sprinklerhoder i tak i moderne bygg |
| `img/tjeneste-nodlys.jpg` | Nødlys over rømningsvei, mørk korridor |
| `img/tjeneste-roykventilasjon.jpg` | Røykluke / ventilasjon i trapperom |
| `img/tjeneste-brannslokkeutstyr.jpg` | Tekniker kontrollerer slokkeapparat og brannslange |
| `img/tjeneste-dokumentasjon.jpg` | Tekniker med nettbrett fyller ut kontrollrapport i bygg |
| `img/miljo-elbil.jpg` | Elektrisk servicebil, fjell og natur ved Bergen |
| `img/miljo-natur.jpg` | Natur ved Bergen, fjord og fjell i morgenlys |
| `img/og-bsv-fire.jpg` | Delingsbilde 1200x630 JPG: tekniker + mørk bakgrunn, plass til logo (legges på i etterkant) |

## Designfilmer i fourphase-stil (produkt og teknikk, uten mennesker)
Rene, stilige produktfilmer med mørk eller lys bakgrunn, myke lysrefleksjoner, sakte kamerakjøring og oransje lys som aksent.
Bruk gjerne Cinema Studio Video 3.0 eller Seedance 2.5: lag først ett stillbilde som startbilde (image-to-video), så blir stilen jevn.
Generiske produkter uten logo, tekst eller merkenavn. Format 16:9, 5–8 sek, uten lyd.

| Fil | Prompt |
|---|---|
| `video/design-brannalarm.mp4` | Sakte kamerakjøring rundt en moderne hvit røykdetektor i taket, hvit overflate med myke refleksjoner, en liten rød lysdiode blinker, mørkegrå bakgrunn, lys oransje kantlys. Ingen tekst eller logo. |
| `video/design-nodlys.mp4` | Mørk moderne korridor sett nedenfra, nødlys i taket tenner ett etter ett og lyser opp en grønn rømningsveisskilt-vei, myk røyk i lufta, rolig fremoverkjøring. Ingen leselig tekst. |
| `video/design-slokker.mp4` | Rød håndslokker på en minimalistisk vegg i et moderne trapperom, sakte kamerabevegelse inn mot manometeret, mykt sidelys, dyp skarphet. Ingen logo eller tekst. |
| `video/design-sprinkler.mp4` | Makrobilde av sprinklerhode i taket, en dråpe vann dannes og faller i sakte film, mørk bakgrunn med oransje kantlys. |

Legg filene inn som bakgrunnsfilm i seksjonene (samme `<video data-autoplay muted loop playsinline>`-mønster som filmbåndet på forsiden).

## Teknisk film: «Inne i brannsentralen» (zoom inn, forklarende)
Mål: én film som zoomer fra en brannsentral inn i kretskortet og viser hva som skjer: sløyfer, brannklokker, alarm til brannvesen, batteri, trådløse enheter, fjernstyring.
Lag den som 6 korte klipp à 4–6 sek (mer kontroll og bedre kvalitet enn ett langt klipp), og sett dem etter hverandre.
Modell: Cinema Studio Video 3.0 eller Seedance 2.5. Bruk siste bilde i hvert klipp som startbilde i neste, så blir zoomen sammenhengende.
Format 16:9, uten lyd. Tekst i selve videoen blir ofte feil, så **ingen tekst i prompten**. Etikettene legger vi på siden som HTML-tekst over filmen.
Felles stil: mørk grafitt-bakgrunn, presis produktvisualisering, kald hvit nøytral belysning, oransje (#EF661C) lys som viser signalene. Generisk utstyr, ingen logoer eller merkenavn.

| # | Klipp | Prompt | Etikett som legges på siden |
|---|---|---|---|
| 1 | Oversikt | Moderne vegghengt brannalarmsentral i et teknisk rom, nøytral grå kabinett med display uten tekst, rolig kamera som sakte nærmer seg. | Brannsentralen |
| 2 | Inn i kabinettet | Døren åpnes og kameraet glir inn mot et kretskort med tydelige tilkoblingsklemmer, makrodybde, lett refleksjon. | Hjernen i anlegget |
| 3 | Sløyfer | Oransje lys pulserer langs tykke kabler fra kretskortet og ut til små detektorer i taket, i en sløyfe som lukker seg, abstrakt teknisk visualisering. | Detektorsløyfer |
| 4 | Utganger | Fra kretskortet går lyspulser til en brannklokke/sirene på veggen og til en blinkende varsler, og et signal sendes ut mot en ikon-lignende antenne uten tekst. | Brannklokker og alarm til brannvesen |
| 5 | Strømbrudd | Rommet blir mørkt. Et batteri ved siden av kretskortet lyser opp og sentralen fortsetter å fungere, kaldt blått lys blir varmt oransje. | Batteri ved strømbrudd |
| 6 | Trådløst og sky | Kamera trekker ut. Små trådløse enheter i rommet sender ringer av lys, og en stilisert lysstråle går opp til en sky og ned til en mobil som viser et nøytralt grensesnitt uten tekst. | Trådløse enheter og fjernstyring |

Lagre som `video/teknisk-brannsentral-1.mp4` … `-6.mp4` (eller klipp dem sammen til `video/teknisk-brannsentral.mp4`) og legg posterbilde i `img/teknisk-brannsentral-poster.jpg`.
Teknisk fakta å holde seg til i teksten: sløyfer, brannklokker, alarmoverføring til brannvesen, batteri-reserve, trådløse enheter (f.eks. Ajax), fjernstyring/sky. Jeg legger inn de endelige etikettene når filmene er klare.

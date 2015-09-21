#### Text Mining Exercise week 2
Guido Zuidhof, s4160703



My approach uses regular expressions to recognize and replace certain parts of the text. All regular expressions are Python regex. The text is processed as follows:

1. Subsequent newlines are flagged, matched using `'\n\n'`
2. Hyphens at the end of sentences are removed, the two parts of the words get merged. Achieved using `re.sub(r'\n([^A-Z])',r"\1", text)`
3. All newlines that do not have a capital letter as next character get removed: `re.sub(r'\n([^A-Z])',r"\1", unhyphened)`
4. Newlines are inserted where the following pattern is present:
 `dot, space, capital letter, (NOT (whitespace AND dot) OR dot)`.
The operation for this is `re.sub(r'[.][ ]([A-Z])([^?\s.])', r'.\n\1\2', text)`.
5. Newlines are re-inserted where the flags were placed in step 1.

This simple approach is quite succesful, I worked from simple rules to more advanced rules, back to simpler rules. It is not perfect, but it gets very close.

##### Encountered problems
I encountered many problems, the first was the encoding of the file. The windows commandline seemed to be unable to print certain characters, and Python wanted to convert everything to unicode. After a lot of googling I found out I could simply decode and encode the file.

The second was the use of hyphens mid-sentence. The solution was to only match hyphens at the end of sentences and remove these.
The third problem had to do with capitals and dots used throughout the text, especially in names of people (with initials). By setting a minimal length of two for a sentence to be placed on a new line in the regex many of these problem areas seem to have been solved.

Finally, there was the page numbering/foot note problem. It turned out to be trivial to solve, as there were already newlines present in the original text, which I could simply restore.

#### Output
```


Distributie van levensmiddelen
Met dc distributie van levensmiddelen was al tijdens de neutraliteitsperiodecen begin gemaakt.
In de eerste wereldoorlog was die distributie aanvankelijkeen gemeentelijke aangelegenheid geweest - nu was zij van meet a f aanlandelijk opgezet, met dien verstande dat de gemeenten de taak gekregenhadden om voor de uitreiking van de bonnen te zorgen.
Er was een Centraal
Distributiekantoor, het C D K , in Den Haag gekomen, het land was in ruim500 ‘distributiekringen’ ingedecld en de ruim duizend gemeenten haddengemeentelijke distributiediensten georganiseerd; voorts had elke inwonereen z.g. distributiestamkaart ontvangen op grond waarvan men periodiekbonkaarten voor levensmiddelen kreeg; met de bonnen van die bonkaart konmen, uiteraard mede tegen normale betaling, in dc winkels levensmiddelenkopen voorzover dic gerantsoeneerd waren.
Dc winkelier plakte de ont­vangen bonnen op vellen, leverde die vellen bij de distributiedienst in (waar zijgeteld werden) en kreeg dan van dic dienst toewijzingsbonnen (de z.g. coupu­res) waarna hij door de groothandel o f de industrie herbcvoorraad kon worden.
Uit de levensmiddelensector waren in dc neutraliteitsperiode slechts tweeartikelen ‘op de bon’ gekomen: suiker en erwten.
De rantsoenen warenevenwel zo ruim dat niet eens alle bonnen ingewisseld werden.
Waaromdan toch die distributie? ‘De inwerkstelling (was)’ , aldus minister Stecnberglic na de oorlog, ‘niet alleen geschied omdat wij een beetje krap begon­nen te zitten’ (dat gold alleen voor suiker, niet voor erwten), ‘maar ook omde proef te nemen o f het systeem werkte.’1
Welnu, het werkte.
Natuurlijk greep die distributie van het begin van de bezetting a f steedsverder om zich heen en niet alleen op het gebied van de levensmiddelen.
W ij hebben er in dit hoofdstuk al voorbeelden van gegeven: voor deaanschaffing van fietsbanden, fietsen, steenkolen, kleding, schoenen, tabaksartikelen en versnaperingen en tenslotte ook voor huishoudelijke artikelenhadden de consumenten telkens bonnen nodig.
Kreeg men zulk een bon,bijvoorbeeld voor een fietsband o f voor een paar schoenen, dan werd eenvakje op de distributiestamkaart afgekruist; de meeste kruisjes waren aan­vankelijk gevolg van het feit dat men periodiek nieuwe bonkaarten voorlevensmiddelen ontving.
In '41 werd aan de stamkaart een z.g. inlegveltoegevoegd.
Op dat inlegvel werd in een vakje de datum gestempeld waar­op men een bonkaart voor levensmiddelen uitgereikt kreeg en dan werdtegelijk een bonnetje dat aan het inlegvel vastzat, afgeknipt en ingehouden.

i1 Getuige M. P. L.
Steenbcrghe, Enq. , dl.
II c, p. 308.

156

ALLES ‘ OP DE B O n ’
Van tijd tot tijd kreeg men een nieuw inlegvel.
Met dat al raakte toch ook destamkaart van velen in dc loop van '42 aardig vol.
Kruidenierswaren, peulvruchten, kaas en zeep ontving men tegen inle­vering van bonnen van de z.g. algemene bonkaart; daarnaast waren er, watde levensmiddelen betrof, geruime tijd aparte kaarten voor brood, aardap­pelen, melk, bloem, boter, vet cn vlees, later was de algemene bonkaartverdeeld in groepen bonnen voor die artikelen.
De bonnen waren als regelgenummerd en welke bonnen in een bepaalde periode geldig waren, werd elkeweek in de pers bekendgemaakt; voor menigeen was dat ccn voornamereden waarom men op een krant geabonneerd bleef.
Praktisch alles kwam‘op de bon’1 - wat de levensmiddelen betrof, bleven alleen groente, fruit envis lange tijd buiten de distributie.
Eind '40 had in gezinnen met een gemid­deld inkomen van ruim f 2 000 per jaar (gezinnen van geschoolde arbeiders,middelbaar kantoorpersoneel enz.) al 70% van de uitgaven voor voedingbetrekking op gerantsoeneerde artikelen; vóór de invoering van de visdistributie (juli '44) was dat 95^% geworden - de vis heeft daar wellicht nog1 % aan toegevoegd.
Anders gezegd: de distributie werd de grondslag vande gehele levensmiddelenvoorziening.
Dat die distributie voor de burgerij een enorme rompslomp met zichbracht, spreekt vanzelf.
In zekere zin waren de distributiestamkaart (plusinlegvel) en de bonkaarten het belangrijkste wat men in huis had.
Het verliesvan een bonkaart, laat staan van alle distributiebescheiden tezamen, leeksteeds een ramp.
Aanvankelijk kon men dan na aangifte bij de distributiedienst nieuwe bescheiden krijgen, maar in dc zomer van '41 deden zich zoveelgevallen van vermissing voor dat toen bepaald werd dat voor cén-derdc vandc verloren gegane rantsoenen geen compensatie gegeven zou worden. N oggeen drie maanden later, in oktober '4 1, werd die regeling ingrijpendgewijzigd.
Er kwamen toen per week niet minder dan 20 000 opgaven vanvermissingen binnen en men was bij de departementen tot de conclusie

1 De distributie van de volgende, voor alle consumenten belangrijke artikelen (onzeopgave is niet volledig) werd in de volgende maanden afgekondigd:jwm '40: brooden bloem, koffie en thee, textiel en schoenen; juli '40: allerlei grutterswaren, boter,margarine en spijsvetten; augustus ’40: alle soorten zeep; september’40: vlees en vlees­waren ; oktober ’40: kaas; november '40: de overige grutterswaren, eieren, koek, gebak,aardewerk, glazen voorwerpen en electrotechnische artikelen; januari '4 1: lucifers;april 41: melk en aardappelen; juli '4 1: alle soorten jam en purée; november '41:cacao en cacaoproducten; mei ’42: tabaksproducten en versnaperingen; september '42:taptemelk; december '42: appelen en zuidvruchten; mei '43: alle surrogaten; augustus'43: groente en fruit; september '43: alle huishoudelijke gebruiksvoorwerpen; juli’ 44 : alle soorten vis.

157

VERA RM EN D NEDERLANDgekomen dat een groot aantal daarvan gefingeerd was.
Er werd derhalvebesloten, vermiste bonkaarten niet meer te vervangen, ‘bijzondere gevallendaargelaten’1 - dat laatste betekende dat de plaatselijke politie en distributiedienst er volstrekt van overtuigd moesten zijn dat geen boos opzet in hetspel was.
Nadien nam het aantal vermissingen af.
Met dat al werd bijvoor­beeld in Den Haag in '43 nog altijd in bijna XI 000 gevallen aangifte gedaan;in een kwart van die gevallen waren de mensen zelfs hun stamkaart en/ofinlegvel kwijtgeraakt.
Als regel werden de bonnen door de vrouw des huizes beheerd; zij was hetimmers die er de dagelijkse inkopen mee moest doen.
In menig z.g. a-sociaalgezin kwam van dat beheer niet veel terecht.
Was men daar bonkaartenkwijt, dan moest men ze ‘zwart’ kopen bij handelaren die het geld voor­schoten maar een exorbitant hoge rente vroegen.
De gemeente Amsterdambegon daar in '42 cen stokje voor te steken: zij richtte een apart bureautjeop waar men zijn distributiebescheiden in beheer kon geven; eind '43vonden er twee ambtenaren een volledige dagtaak in het beheer van de bon­nen van bijna negenhonderd personen. W ij nemen aan dat deze vorm vanhulp ook elders in den lande geboden is.
Gelijk reeds gezegd: het land was in distributiekringen ingedeeld.
Op hetplatteland behoorden als regel verscheidene gemeenten tot één kring.
In degeografische groepering deden zich nogal eens wijzigingen voor, als regelterwille van de efficiency, later ook als gevolg van de evacuaties.
Eind '42waren er 382 distributiediensten die er tezamen 685 agentschappen op nahielden.
In een gemeente die geen eigen distributiedienst bezat, was in elkgeval een agentschap van een distributiedienst van een aangrenzende ge­meente gevestigd.
Uiteraard hadden die distributiediensten in de grootstegemeenten een aanzienlijke omvang.
Daar was nieuw personeel voor aange­nomen hetwelk, als er extra veel werkzaamheden waren (bij de uitreikingvan nieuwe bonkaarten bijvoorbeeld), telkens tijdelijk uitgebreid werd.
De
Amsterdamse distributiedienst had bijvoorbeeld eind '43 een vaste staf vanmeer dan elfhonderd krachten, bijna allen arbeidscontractanten, aan wic intijden van grote drukte ruim vierhonderd arbeidscontractanten toegevoegdwerden; de Rotterdamse dienst had in die tijd ruim twaalfhonderd manpersoneel, tijdelijke krachten meegerekend.
In het gehele land waren eind'43 ca. twaalfduizend personen in vaste dienst (wij bedoelen dit niet in juri­dische zin) bij de gemeentelijke distributie-organen ingeschakeld.

1 H N S, Research-bureau: ‘Rapport over de toestand van het Nederlandse bedrijfs­leven over de maand oktober 19 4 1’ (nov. 1941), p. 58 (CNO , 351 b).

158

DIST K IB U T IE -A PP A RAAT

Naast die twaalfduizend waren in de lente van '43 bijna zeventienhonderdpersonen werkzaam in het kader van het Centraal Distributiekantoor.1 Vandie bijna zeventienhonderd waren ruim vierhonderd in de z.g. buitendienstwerkzaam: zij waren o.m. belast met het controleren van de distributie­diensten, zulks onder toezicht van inspecteurs.
Uiteraard was het C D K eenenorme paperasscnwinkel.
Het stond in vast contact, enerzijds met de Duitse en
Nederlandse centrale overheid, anderzijds met de meer dan duizend distributicdiensten en agentschappen en met meer dan vijftienduizend instellingen dicaparte toewijzingen ontvingen (hotels, cafc’s, restaurants, allerlei soorten tehui­zen voor verpleegden, enz. enz.).
Van begin mei '40 tot eind april '45 gingenvan het C D K bijna 10 000 circulaires uit, gemiddeld dus veertig per w eek ;dat per week meer dan 100 000 poststukken de deur uitgingen, was normaal.
In de eerste jaren heerste bij het C D K een vrij strakke discipline.
Getieralkotmnissar Schmidt vond de gehele Nederlandse distributie zo bewonderens­waardig geregeld dat hij eind '4 1 de stoot gaf tot de verschijning van eenbrochure (In uw belang) waarin het systeem tot in onderdelen beschrevenwerd.
In april '43 kwam een van de Duitse hoofdambtenaren van de Haupt­abteilung Ernahrung und Landivirtschaft bij een bezoek aan Münster tot deconclusie dat de Nederlandse distributie veel effectiever controlemogelijk­heden kende dan de Duitse - wat hij van de Nederlandse vertelde, wekte bijde distributie-ambtenaren in Miinster zo groot enthousiasme dat ze meteenvroegen o f ze het Nederlandse stelsel eens van nabij mochten komen bezien.
O f deze reis doorgegaan is, weten wij niet. W el menen wij dat de Duitseambtenaren minder enthousiast naar Duitsland zouden zijn teruggekeerd alsze een jaar later op bezoek waren gekomen.
Om te beginnen hadden defrequente overvallen die vooral door de z.g.
Knokploegen op dc distributiebureaus uitgevoerd waren, de ordelijke gang van zaken toen lelijk verstoord,maar bovendien was de discipline binnen het C D K merkbaar verslapt.
Deevacuatie naar Zw olle en Hattem die in '43 voltrokken was2, had de dienstgeen goed gedaan.
Het kwam toen vaak voor dat functionarissen, ook lei­dende, afwezig waren omdat zij hun gezinnen, voorzover niet mee-geëvacueerd, wilden bezoeken.
Gevallen van fraude hadden zich van meet a f aan

1 Er bevonden zich onder hen slechts weinig N S B ’ers.
Volgens de directie waren heter in '42 vijf; onder pressie van de N SB kwamen er toen twee bij, ‘doch dezen zijn’,aldus de Hoo, ‘na een maand wegens wangedrag weer ontslagen.’ (Prac-Apeldoorn:p.v. S. de Hoo (24 juni 1946), p. 1 (Doc I-739, a-4). 2 In Hattem was van '40 a f deafdeling van het C D K gevestigd die de van de detaillisten terugstromende bonnencontroleerde, voorzover dit de provincies benoorden de rivieren betrof; voorzuidelijk Nederland bevond zich een overeenkomstige afdeling in Gennep.

159

VE RAR ME ND NEDERL ANDbij verscheidene distributiediensten voorgedaan (als regel slaagde Hirsch­felds departement er in, berichten daaromtrent, die een ongunstig cffectkonden hebben op de discipline van de consumenten, uit de pers te houden1)- die fraude was met dc schaarste toegenomen.
Naast dc op het eigenbelanggerichte fraude was er echter ook een fraude tot ontwikkeling gekomen diealtruïstisch mag heten: zij strekte namelijk tot bescherming van de onder­duikers. W ij komen er in hoofdstuk 6 van dit deel uitgebreid op terug, maarwillen hier reeds vermelden dat eind '43 een situatie ontstaan was waarin vandc oorspronkelijke administratieve zorgvuldigheid van het C D K niet veelmeer over was: de illegaliteit, met name de Landelijke Organisatie voor
Hulp aan Onderduikers, ondervond ook van functionarissen van het C D Kzoveel medewerking dat er toen en later in het C D K geen berekening meergemaakt werd die werkelijk klopte.
De zaak was dus deze dat van de zomer van '43 a f een deel van de ambte­naren van het C D K het min o f meer liet afweten en dat een ander deel het
C D K gebruikte voor illegale doeleinden - dc directeur, S. de Hoo, had dezaak niet meer in de hand.

★

Sybren dc Hoo, in 1900 in Assen geboren, had in '3 1 de Koninklijke Marineverlaten en was ambtenaar bij het departement van economische zakengeworden.
Hij werd capabel geacht, bereikte begin '40 dc rang van referen­daris cn was toen belast met de dagelijkse leiding van het nog vrij kleine
C D K .
Een andere hoofdambtenaar, dr. W . L.
Groeneveld Meyer, dirccteurgcncraal voor de middenstand, was daar directeur van.
Deze laatste werd,verdacht van tegenwerking, eind '40 op last van de Duitsers ontslagen.
De
Hoo werd dc nieuwe directeur.
Dat was van de zijde van Hirschfeld geengelukkige keuze.
Spoedig bleek namelijk dat de Hoo de sterke neiging had

1 In februari '42 zei Hirschfelds perschef op de dagelijkse persconferentie: ‘Dc tijdenzijn al zo verward en moeilijk cn er komen zoveel fraudes voor, ook bij distributie­diensten, dat deze laatste in Godsnaam niet op sensationele wijze bekendgemaaktmoeten worden . . .
Ik herinner nogmaals aan het verzoek om fraudes bij de distri­butiediensten, voorzover ze bij de ambtenaren schuilen, niet te publiceren. U behoeftniet bang te zijn dat zij in de doofpot gestopt worden’ (enkele grote gevallen werdendoor het Obergericht berecht), ‘een verontrusting van het publiek hebben wij echterminder dan ooit van node.’ (Verslag persconferentie, 7 febr. 1942 (DVK, 49)).

IÓO

CENTRAAL DISTRIBUTIEKANTOORom met N S B ’ers en Duitsers aan te pappen.
Hij voelde zich min o f meer dekoning van de Nederlandse distributie en vond het kennelijk aangenaamdat hij links en rechts gunsten kon uitdelen, zo aan Hirschfeld die op zijnbeurt de overige secretarissen-generaal, enkelen van zijn hoofdambtenaren,
Woltersom cn diens naaste medewerkers, alsmede van tijd tot tijd ook di­verse particulieren van extra-bonnen voorzag.1 Ook de N SB en bijvoorbeelddc N S D A P ontvingen extra-toewijzingen maar deze deed de Hoo niet opeigen gezag - hij ontving er aanwijzingen voor van het Reichskommissariat.
Hij protesteerde nimmer tegen dergelijke instructies en oefende bovendienweinig controle uit op de uitvoering zodat dc z.g. distributiedienst van dc
N S B in de zomer van '44 zelfs dc beschikking kon krijgen over door het
C D K afgetekende blanco-toewijzingen waarop die distributiedienst dus zelfde hoeveelheden kon invullen.
De correspondentie die dc Hoo in zijn functiemet die N S B - en Duitse instanties voerde, was van zijn kant een en alamicaliteit.
In ‘foute’ kringen werd het dan ook vrij algemeen bekend datcen persoonlijk brieQe aan de directeur van het C D K wonderen kon ver­richten. Z o stuurde een ‘foute’ rechercheur die bij de afdeling Kriminalpolizeivan de staf van de Befehhhabcr der Sicherheitspolizei und des SD ingedeeld was,de Hoo begin '44 een brief waarin hij eerst allerlei eigen wensen kenbaarmaakte en vervolgens te spreken kwam over Gruppe V - dat was het Komniando dat, eerst geleid door Krimimlkommissar Horak en nadien door
Kriminalkommissar Oskar Wcnzky, aan de Rijksrccherchecentrale toege­voegd w as:‘En last not least, verzoekt de oude heer Gerhards bij Gruppe V die de laatstemaanden sukkelende is aan spierpijnen, hem voor zijn rijwiel nieuwe banden tewillen doen verstrekken. U kent hem toch, de oude Obersturmfiihrer'? Hij kanheel moeilijk lopen, moet echter toch zijn dienst blijven doen . . .
Waar nu K.K.
Wenzky kort geleden toch banden voor dienstpersoneel heeft aangevraagd aanuw bureau, moge ik u verzoeken, bij deze toezending, die naar ik hoop spoedigzal plaatsvinden, ook tegelijkertijd aan Obersturmführer Gerhards te willen denken.
Is voor u een klein kunstje.
Van dit laatste weet K. K.
Wenzky niets afhoor Direc­teur.
Dit is slechts een onderhands verzoekje van de heer Gerhards . . . U doetmij er tevens een groot genoegen mee, omreden ik hem dikwijls nodig heb voor

1 N og een voorbeeld dat buiten het C D K ligt: de N S B ’er die directeur was van hetrijksinkoopbureau, gaf in '43 Rost van Tonningen, Rambonnet en een aantal vanzijn eigen functionarissen die N S B ’er waren, de gelegenheid, zich uit de voorradenvan het R IB artikelen aan te schaffen, die in winkels normaal niet meer te koopwaren.

161

VE RAR ME ND NEDERLANDallerlei soort ‘gevalletjes’ die zo dagelijks aan de orde zijn. U begrijpt mij hoop ikwel.
Ik hoor u al mopperen, daar komt die ‘rotvent’ ook weer aandraven met denodige verzoekjes.
Ja Hooggeachte Directeur, het is waar, maar wij moeten tochtrachten met elkaar door de moeili jkheden heen te komen.
Meer dan ooit zijn wijthans op elkaar aangewezen.
Nach dem Krieg werden wir auch lehen miissen.'1
Niet alleen echter legde de Hoo jegens Duitsers en N S B ’ers een stuitendegedienstigheid aan de dag, hij gaf zich ook veel moeite om persoonlijk deelte nemen aan politie-onderzoeken in verband met malversaties op distributiegebied en zulks mede in een fase waarin een ieder wist dat die mal­versaties in ruime mate gepleegd werden om illegale groepen en onder­duikers te helpen.
In augustus '43 verzocht hij Harster, de Bejehlshaber der
Sicherheitspolizei und des SD , om een document dat hem het recht zougeven, onmiddellijk de hulp van alle politie-organen, Nederlandse èn
Duitse, in te roepen.
In februari '44 ging hij er prat op dat hij het C D Kperfect tegen overvallen beschermd had.
Begin mei '44 beklaagde hij zichpersoonlijk bij Rauter o.m. over het feit dat Harsters opvolger hem, terwille van het verstrekken van fietsbanden, de namen opgegeven had van
Nederlanders die bij de ‘ SD ’ in dienst waren; de Hoo vond dat blijkbaaronvoorzichtig.
Kortom, tot laat in de bezetting trachtte hij bij de bezetterin het gevlij te komen.
Het paste in dat kader dat hij, wanneer hij schriftelijkbezwaren uitte tegen het beleid van Hirschfelds departement o f van Louwes’rijksbureau, steeds het Reichskommissariat achter de rug van Hirschfeld en
Louwes om een afschrift zond van zijn brieven.
Daar kwam dan nog bijdat hij zichzelf en ook wel organisaties waar hij lid van was (de Jagersvereniging bijvoorbeeld - hij was een verwoed jager), steeds de nodigeextra-bonnen toeschoof. ‘Op zijn zachtst uitgedrukt’, aldus een ambtenaardie in mei '44 aan Hirschfeld een speciaal rapport over het C D K uitbracht,‘gaat het bij de toewijzingen wel eens onbegrijpelijk toe.
Het personeel vraagtzich af, waarom sommige firma’s . . . zo goed worden bedacht.
Indertijd werder door de vele leidende figuren royaal geleefd . . .
Alles tezamen genomen is het
CD K nu niet bepaald een modelkantoor’2 en de Hoo (hij was in die tijd, van een ziekte herstellend, kennelijk over­werkt) was bepaald geen modeldirecteur meer.
Dat laatste was onmiddellijkna het bezoek van die ambtenaar gebleken, ja op de dag zelf waarop dezezijn rapport schreef: 10 mei '44.
Die dag was de Hoo namelijk in Zw olle

1 Brief, 10 jan. 1944, van K.L. aan S. de Hoo (Doc I-739, a-4). 2 H. L.
Dekking:‘Rapport organisatie C D K ’ (10 mei 1944) (Collectie-Hirschfeld, 7 e).

162

CENTRAAL DISTRIBUTIEKANTOORgaan lunchen met drie directieleden van enkele van de grootste levensmiddelenfirma’s en met een functionaris van de firma Joh.
Enschedé &
Zonen te Haarlem (waar alle distributiebescheiden gedrukt werden).
Deheren dronken een kruik jenever leeg plus enkele flessen wijn - toen de
Hoo in Hattem terugkwam, was hij dronken.
Drie dagen later kreeg hijvan Hirschfeld ziekteverlof.
Met de leiding van het C D K werd toen eenvan dc adjunct-directeuren belast, J. G.
Japikse.
De Hoo deelde nadien
Rauters adjudant schriftelijk mee dat hij ontslag wilde nemen. ‘Kommt nichtin Fragel’ schreef Seyss-Inquart op zijn brief, en Rauter antwoordde de Hoodat hij maar een geschikte plaatsvervanger moest zoeken, 'jedoch bleiben
Sie für den gesamten Apparat des Zentral Distributiekantoors in vollem Um­fang verantwortlich.’1 De bezetter achtte dus ook toen nog de Hoo eenonmisbare kracht.
Dat had óók te maken met de diensten die de Hoo bij deinvoering en uitreiking van de z.g. tweede distributiestamkaart de bezetterbewezen had - wij komen daar in hoofdstuk 5 op terug.★

Bij de levensmiddelendistributie werd er met kracht naar gestreefd, demedische normen die voor een voldoende voeding golden, scherp in hetoog te houden.
Reeds enkele weken na de capitulatie had Hirschfeld uitdc bestaande Gezondheidsraad een aparte commissie gevormd, de z.g.
Voedingsraad, die de samenstelling van het distributiepakket regelmatiganalyseerde en op grond daarvan adviezen gaf.
Als dat maar enigszinsmogelijk was, werden die adviezen door Hirschfeld en Louwes overge­nomen en door hen aan de Hauptabteilung Ernahrung und Landwirtschaftvoorgelegd - het was immers de bezetter die uiteindelijk de rantsoenenvaststelde.
Toen Engeland in '40 de strijd bleek voort te zetten, stond voor Hirschfeldcn Louwes vast dat men op den duur met de Nederlandse voedselvoor­ziening in grote moeilijkheden zou komen.
Het getuigde hunnerzijds danook van vooruitziend beleid dat zij in de loop van '40 de stoot gaven toteen belangrijke uitbreiding van het aantal kookinrichtingen waar massavoeding toebereid kon worden: de z.g.
Centrale Keukens.
Een enquêtebij de gemeentebesturen toonde aan dat er in den lande reeds 98 bestondendie elk een capaciteit hadden van minstens 500 porties (elk van f liter)

1 Brief, 12 juni 1944, van Rauter aan S. de Hoo (HSSuPF, 7 A, b).

163

VERA RM EN D NEDERL ANDper dag.
Dat aantal werd te gering geacht.
Om te beginnen werden in dcgrote steden 50 keukens ingericht die eind "40 al een gemiddelde capaciteithadden van 7 000 porties; deze was in '43 door verbeterde methoden meerdan verdubbeld.
Die 50 keukens werden door de gemeenten geëxploiteerd.
Daarnaast richtte het rijksbureau voor de voedselvoorziening in oorlogstijdook een aantal eigen keukens in en tenslotte werden grote bedrijven gesti­muleerd om elk voor zich o f gezamenlijk centrale keukens in te richten voorhet verstrekken van bonloze bijvoeding aan de arbeiders.
Eind '43 was decapaciteit van alle keukens tezamen 2 miljoen porties per dag. O ok dat was
Hirschfeld en Louwes nog te w einig; de Geallieerde invasie kon, zo meendenzij, heel wel een toestand doen ontstaan waarbij de winkels niet meerbevoorraad konden worden en de gezinnen in het geheel geen gas meerkonden krijgen.
Van alle hotels, restaurants en inrichtingen als ziekenhuizenwerden de kookinstallaties geïnventariseerd en zo werd een net van 1 200‘noodkeukens’ gevormd die een gezamenlijke capaciteit hadden van ca.8 miljoen porties per dag.
Voor alle zekerheid werd tevens door het rijks­bureau een hoeveelheid van ca. 20 000 kilo stamppot ingevroren - veelwas het niet, maar in geval van nood zouden alle beetjes helpen.1
D e centrale keukens (die in de hongerwinter een volstrekt onmisbarefunctie zouden vervullen) wierpen in de periode die wij thans behandelen,tot zomer '44 dus, reeds veel nut af. W ie thuis niet goed kon koken, kontegen inwisseling van de nodige bonnen zes dagen per week bij een van dekeukens een portie deskundig toebereid warm voedsel halen, meestalstamppot.
Daarbij trad bij de afnemers wel een zekere ‘stamppotmoeheid’op - het aantal personen die aldus hun warm voedsel betrokken, wisselde danook nogal.
Daar kwam bij dat men, teneinde tot deze voorziening toegelaten te worden, een kaart moest bezitten die alleen door de ‘foute’
Nederlandse Volksdienst afgegeven werd.
I11 Amsterdam waren er begin'41 zesduizend personen die van de centrale keukens gebruik maakten;zomer '42 waren het er vijf-en-veertigduizend, maar nadien ging dataantal dalen zodat er in de zomer van '44 nog maar achtduizend Amster­dammers waren die zes dagen per weck hun voedsel van de centrale keukensbetrokken.2
Gelijk gezegd: voor dat voedsel moest men een deel van zijn bonnenafstaan.
De bijvoeding die door een aantal grote bedrijven verstrekt werd,was bonloos en daarvan profiteerden in de zomer van '42 (het zijn de1 Het Reichskommissariat bouwde in die tijd aparte reservevoorraden voedsel op dievoor de Rijksduitsers in Nederland bestemd waren.2 In maart '45 waren hetbijna vierhonderdduizend.

164

CENTRALE KEUKENSenige gegevens die wij bezitten) meer dan driehonderdzeventigduizend ar­beiders.1 Van hen waren toen honderdvijf-en-dertigduizend werkzaamin bedrijven o f bedrijfstakken, de mijnbouw bijvoorbeeld, die door de
Riistungsinspektion van speciaal belang geaclit werden.
Kortweg kan menstellen dat in de zomer van '42 ruim één derde van de in de industrie werk­zame arbeiders bonloze bijvoeding kreeg; dat feit hield overigens dcerkenning in dat de verhoogde rantsoenen die men bij zware, zeer zwareo f langdurige arbeid ontving, niet voldoende waren om dc arbeidskrachtop peil te houden.
Een niet onaanzienlijk deel van de werkende bevolking had recht op dieverhoogde rantsoenen: in '43 bijna zeshonderdduizend personen, van wieruim vierhonderdduizend gerekend werden, ‘zeer zware arbeid’ te verrich­ten. N og andere groepen kregen meer dan de ‘normale verbruiker' diewij in dc aanlief van dit hoofdstuk introduceerden.
Om te beginnen, maardan louter naar verhouding, de kinderen; zij ontvingen rantsoenen diehun voeding beter op peil hielden dan die van de volwassenen.
De rant­soenen voor kinderen van o tot 3 jaar waren (dit alles uiteraard tot dehongerwinter begon) ongeveer gelijk aan wat kinderen van die leeftijdvolgens medische normen aan vocdselwaarden dienden te krijgen, en dievoor kinderen van 4 tot 14 jaar en van 14 tot 20 jaar lagen maar weinigbeneden die normen.
Maar kwamen dic relatief verhoogde rantsoeneninderdaad steeds bij de kinderen terecht? In menig gezin werden zij als eensoort algemene reserve beschouwd waar de vader, als hij honger had,als eerste zijn toevlucht toe nam.
Ook zieken en zwangere vrouwen hadden recht op extra-rantsoenen.
Die moesten door de behandelende huisarts aangevraagd worden; deaanvraag werd beoordeeld, in gemeenten die een eigen geneeskundige- engezondheidsdienst hadden, door die dienst, elders door een vertrouwensartsvan de inspectie van de volksgezondheid.
Geschillen werden aan provincialemedische commissies voorgelegd. W ij hebben geen gegevens over deaantallen personen die in bepaalde perioden ziekenrantsoenen ontvingenmaar er is aanleiding om te veronderstellen dat met de toekenning nogalruim omgesprongen werd - dat was althans de conclusie die zich in de lentevan '44 aan de hoofdinspecteur van de volksgezondheid, dr. C.
Banning,opgedrongen had.
Hij had vooral geconstateerd dat die ziekenrantsoenen,eenmaal toegekend, min o f meer automatisch verlengd werden; het vielveel artsen blijkbaar moeilijk, die toekenning te doen beëindigen.
De

1 Bijna 70 000 porties kwamen daarbij uit de centrale keukens van de overheid.

165

VE RA RM EN D NEDERLAND
Hauptabteilung Ernahrung und Landivirtschaft gaf toen medio juni het C D Kde nogal botte instructie om per i october het totaal der ziekenrantsoenente halveren.
In de paragraaf over de visserij vermeldden wij dat opvarenden vanvissersschepen uit de vangst officieel, d.w.z. buiten de distributie om, v ijfkilo vis mee naar huis mochten nemen (dat werden er in feite vijftien).
Diebepaling was onderdeel van een algemene regeling: allen die agrarischebedrijven bezaten dan wel als bakker o f slager werkzaam waren, golden alsz.g. zelfverzorgers; mèt hun gezinsleden hadden zij, wat de waren betrofwaarmee zij rechtstreeks te maken hadden (veehouders bijvoorbeeld metmelk, boter en kaas), recht op hogere rantsoenen: zij behielden een deelvan de productie voor eigen gebruik. Z o was het ook aan akker- en tuin­bouwers officieel tocgestaan, een klein deel van de oogst te behouden.
Landarbeiders mochten van de oogst 25 kilo graan per gezinslid mee naarhuis nemen.
W ij achten het aannemelijk dat men zich van al die normen van denbeginne a f niet veel aangetrokken heeft.
Boeren en landarbeiders haddenin elk geval voldoende te eten en van de daling van de brood- en vleesrantsoenen hadden de bakkers respectievelijk de slagers geen last.
Zijkonden zich allen over de gehele linie o f ten aanzien van bepaalde levens­middelen redden.
Het waren de ‘normale verbruikers’ die in moeilijkhedenkwamen.
Wanneer wij dan ook in een vorige paragraaf ten naaste bij becij­ferd hebben, welk percentage van de in ons land geproduceerde levens­middelen door export naar Duitsland en door leveranties aan de Wehrmachtverloren ging voor de ‘Nederlandse consumenten’ , dan moet de lezer nuwèl bedenken dat dic consumenten niet één groep vormden.
Van de aard­appeloogst '4 3 -4 4 bijvoorbeeld, ging vermoedelijk 1 5 % naar dc Duitserstoe, maar van hetgeen toen restte voor de ‘Nederlandse consumenten’ ,bleef 16 % bij de ‘zelfverzorgers’, ging 4 % extra naar de personen toe diezware, zeer zware o f langdurige arbeid verrichtten en was nog eens 3 %nodig voor de bonloze bijvoeding der industrie-arbeiders.
In verschillende publikaties zijn overzichten verschenen van het verloopvan dc rantsoenen en is ook nauwkeurig berekend wat hun calorischewaarde was1 - wij willen er hier slechts uit weergeven dat de ‘normale

1 Een overzicht van de totale hoeveelheden der gerantsoeneerde levensmiddelen perpersoon en per jaar, naar de verschillende ‘rantsoeneringsgroepen’ ingedeeld, vindtmen op de pagina’s 252-54 van de Economische en sociale kroniek der oorlogsjaren194 0 -194 5.
Dezelfde uitgave bevat op pag. 257 een tabel van het totale jaarlijkseverbruik op de consumentenbonnen en op pag. 259 een overzicht van de calorische

166
```

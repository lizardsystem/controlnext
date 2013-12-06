/*  Gebruik & initialisatie
    Uitgangspunten en opmerkingen:
    - jQuery is ingeladen (in dit voorbeeld 1.10.2)
    - jQuery ui is ingeladen (in dit voorbeeld 1.10.3)
    - HTML: 4 quadrantdelen en een quadrant "dot" vallen binnen het element waar de widget op wordt toegepast: in dit voorbeeld "quadrant-control".
        
    <div id="quadrant-control">
            ...
        <div id="quadrant-1"></div>
        <div id="quadrant-2"></div>
        <div id="quadrant-3"></div>
        <div id="quadrant-4"></div>
        <div id="quadrant-dot"></div>
    </div>
    
    - Op de plek van ... kan het label of andere elementen vrij worden ingeladen.
    - Kleur en vormgeving worden volledig bepaald door CSS
    - Class "active" wordt gebruikt om een quadrant op te lichten. Zie onderdeel "Nieuw" onderaan /css/quadrant.css
    - Positionering van de dot houdt rekening met de border radius die de dot al heeft. 50% 50% is het daadwerkelijke midden.    
    - Bij invoer van een negatieve waarde voor de dotx of doty optie wordt de dot niet weergegeven.
*/


// Eerste initialisatie kwadrant
$('#quadrant-control').quadrant({
    activequadrant: 4,
    dot:[{dotx: 0, doty: 0}]
});

// Achteraf instellen actieve quadrant
$('#quadrant-control').quadrant('option', 'activequadrant', 1);

// Dot uitzetten
$('#quadrant-control').quadrant('option', 'dot',[{doty:-1, dotx:-1}]);

// Achteraf instellen relatieve positie dot in percentages t.o.v. quadrant.
$('#quadrant-control').quadrant('option', 'dot',[{doty:50, dotx:50}]);




// Eerste initialisatie actuele water stand
$('#fill-gauge').actualwater({
    actualwater: 76
});

// Achteraf instellen actuele water stand
$('#fill-gauge').actualwater('option', 'actualwater', 40);

// Verandering van de input field actualcontrol past direct de actuele waterstand aan.
$('#actualcontrol').on('change', function() {
		$('#fill-gauge').actualwater('option', 'actualwater', $(this).val());
});

// Eerste initialisatie reverse osmose balk
/*
	Omdat de balk is gebaseerd op de looptijd van de grafieken worden alleen Datum objecten als input geaccepteerd voor de tijdsgrenzen.
	De vulling van het grijze label deel en het "Ro aan" deel wordt proportioneel geregeld op basis van de tijdsafstanden tussen de inputs.
	In de praktijk betekent dit dat een grafiek met 10 dagen loopt tijd, een verticale grijze lijn op dag 3 en een RO van dag 3 t/m dag 10 exact 
	dezelfde balk op zal leveren als grafiek met looptijd van 20 weken, een verticale grijze lijn op week 6 en een RO van week 6 t/m week 20.
	
	Onderliggende HTML in #reverse wordt automatisch via een append functie toegevoegd

*/
/*

	Voorbeeld van 28 november tot 5 december
$('#reverse').reverseosmose({
    border: new Date(2013, 12, 02),         	
	rangestart: new Date(2013, 11, 28),
	rangeend: new Date(2013, 12, 05),
	rson: new Date(2013, 12, 02),
	rsoff: new Date(2013, 12, 03),
    labeltxt: "Reverse osmose",
    filltxt: "Ro aan"
}); 
*/

//		Voorbeeld van 02 november 01:30 tot 01:31
$('#reverse').reverseosmose({
    border: new Date(2013, 12, 02, 01, 30 , 10),         	
	rangestart: new Date(2013, 12, 02, 01, 30),
	rangeend: new Date(2013, 12, 02, 01, 31),
	rson: new Date(2013, 12, 02, 01, 30, 20),
	rsoff: new Date(2013, 12, 02, 01, 31 ),
    labeltxt: "Reverse osmose",
    filltxt: "Ro aan"
}); 
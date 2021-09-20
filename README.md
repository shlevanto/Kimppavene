Tämä on HY Tietokantasovellus syksy 2021 kurssityö. Kurssin tavoitteena on rakentaa ja julkaista Herokussa toimiva web-sovellus PythoninFlask-kirjastoa ja PostgreSQL-tietokantaa hyödyntäen.

## Kimppavene -sovellus
Kimppavene on sovellus yhteisomistuksessa olevan veneen käyttövuorojen, talkootöiden ja kulujen seurantaan ja hallintaan.

Sovellusta voi testata [Herokussa](https://kimppavene.herokuapp.com).

Voit luoda oman käyttäjätilin tai käyttää valmiiksi luotuja tilejä:
| käyttäjätunnus | salasana |
| ----------- | ----------- |
| muumipappa | merimeri |
| fredrikson | havethavet |

Voit liittyä osakkaaksi Muumipapan ja Fredriksonin Merenhuiske -veneeseen avainoodilla 8623af.

## Toteutet toiminnallisuudet
- Palveluun voi luoda käyttäjätilin ja käyttäjä voi kirjautua sisään.
- Käyttäjä voi luoda tiliinsä liittyvän uuden veneen, jonka osakas hän on. Käyttäjä voi olla osakkaana useammassa kuin yhdessä veneessä.
- Käyttäjä voi liittyä osakkaaksi olemassaolevaan veneeseen syöttämällä toiselta osakkaalta saamansa veneen avainkoodin järjestelmään.
- Käyttäjä voi tehdä tapahtumakirjauksia veneelle. Kirjattavat
tapahtumat ovat käyttö, talkootyö ja kustannukset.
- Käyttöoikeuskirjanpito. Veneelle on käyttäjäkohtainen, vuosittainen oletuskäyttöoikeus 12 päivää.
- Tehdyt talkootyöt kasvattavat käyttöoikeutta ja käyttö vähentää.

## Keskeneräiset toiminnallisuudet
- Veneelle voi määritellä yhden tai useampia pääkäyttäjiä, jotka voivat muokata veneen tietoja. Veneen luonut käyttäjä määrittyy aina luomansa veneen pääkäyttäjäksi.
- Veneen pääkäyttäjä voi antaa muille veneen osakkaille pääkäyttäjän oikeudet.

## Toteuttamista odottavat toiminnallisuudet
- Käyttäjä voi tallentaa veneen tietoihin tiedostoja kuten käyttöohjeita, kuvia ja osakkaiden keskinäisiä sopimuksia.
- Järjestelmässä on raporttinäkymiä, joista veneen osakas voi seurata omaa ja muiden saman veneen osakkaiden käyttöä. Veneen käyttömäärä, tehtyjen talkootuntien määrä ja osakas- / venekohtaiset kulut ja investoinnit.
- Käyttöoikeuksille voi määritellä kertoimet eri viikoille. Lomakaudella käyttö syö enemmän käyttöoikeutta.

## Optiota lisäominaisuuksista
- Käyttäjä voi tehdä veneelle vuotuisen budjetin, jonka toteutumista voidaan seurata raporttinäkymässä.
- Varauskalenteri, jossa osakkaat voivat varata veneen käyttövuoroja.
- Varauskalenterin tapahtuman voi merkitä toteutuneeksi, jolloin se muuttuu tapahtumakirjaukseksi

## Luonnos tietokantakaaviosta
<img src='CoBoat.png'> </img>

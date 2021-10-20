Tämä on HY Tietokantasovellus syksy 2021 kurssityö. Kurssin tavoitteena on rakentaa ja julkaista Herokussa toimiva web-sovellus PythoninFlask-kirjastoa ja PostgreSQL-tietokantaa hyödyntäen.

## Kimppavene -sovellus
Kimppavene on sovellus yhteisomistuksessa olevan veneen käyttövuorojen, talkootöiden ja kulujen seurantaan ja hallintaan.

Sovellusta voi testata [Herokussa](https://kimppavene.herokuapp.com).

Voit luoda oman käyttäjätilin tai käyttää valmiiksi luotuja tilejä:
| käyttäjätunnus | salasana |
| ----------- | ----------- |
| muumipappa | merimeri |
| fredrikson | havethavet |

Muumipapalla ja Fredriksonilla on Kimppaveneessä yhteinen vene nimeltä Merenhuiske. Muumipappa on siinä pääkäyttäjänä ja pääsee muokkaamaan veneen tietoja. Fredriksonilla ei ole pääkäyttäjäoikeuksia, joten hän ei pääse käsiksi ylläpitonäkymään (https://kimppavene.herokuapp.com/manageboat).

Voit liittyä osakkaaksi Muumipapan ja Fredriksonin Merenhuiske -veneeseen avainkoodilla ```35743d```.

## Sovelluksen käynnistäminen paikallisesti
1. Kloonaa repositorio koneellesi
2. Alusta tietokanta komennolla ```psql kimppavene < schema.sql```
3. Aja oletusarvot tapahtumatyyppeihin, kuluihin ja tuloihin ```psql kimppavene < init.sql```

## Toteutetut toiminnallisuudet
- Palveluun voi luoda käyttäjätilin ja käyttäjä voi kirjautua sisään.

### Etusivu
- Raporttinäkymä, josta kirjautunut käyttäjä voi seurta veneen käyttömäärää, tehtyjen talkootuntien määrää sekä osakas- ja kululajikohtisesti veneen kuluja.

### Veneet
- Käyttäjä voi luoda tiliinsä liittyvän uuden veneen, jonka osakas hän on. Käyttäjä voi olla osakkaana useammassa kuin yhdessä veneessä.
- Käyttäjä voi liittyä osakkaaksi olemassaolevaan veneeseen syöttämällä toiselta osakkaalta saamansa veneen avainkoodin järjestelmään.
- Käyttöoikeuskirjanpito. Käyttäjälle määrittyy venekohtainen, vuosittainen oletuskäyttöoikeus 12 päivää kun käyttäjä luo uuden veneen tai liittyy olemassa olevaan veneeseen.

### Veneen pääkäyttäjänäkymä
- Veneellä on yksi tai useampia pääkäyttäjiä, jotka voivat muokata veneen tietoja.
- Pääkäyttäjänäkymään pääsee klikkaamalla 'Muokkaa' -painiketta Veneet -sivun veneen tiedoissa.
- Veneen luonut käyttäjä määrittyy aina luomansa veneen pääkäyttäjäksi.
- Veneen pääkäyttäjä voi antaa muille veneen osakkaille pääkäyttäjän oikeudet tai poistaa ne. Omia pääkäyttäjäoikeuksiaan ei voi poistaa eli veneellä on aina vähintään yksi pääkäyttäjä.
- Uudelle veneelle määrittyy oletusarvot käyttöoikeuksien kertoimille.
- Kertoimet on määritelty viikkojen numeroiden perusteella. Ideana on, että lomakaudella käyttö syö enemmän käyttöoikeutta.
- Käyttöoikeuksien kertoimia voi muokata pääkäyttäjänäkymässä.

### Tapahtumat
- Käyttäjä voi tehdä tapahtumakirjauksia veneelle. Kirjattavat
tapahtumat ovat käyttö, talkootyö, kulut ja tulot.
- Tehdyt talkootyöt kasvattavat käyttöoikeutta kertoimella 3 ja käyttö vähentää käyttöajan kertoimella. Jos samanaikaisia käyttäjiä on useampia, jaetaan kullekin osakkaalle kirjautuvat käyttötunnit käyttäjien määrällä.
- Käyttäjä voi tallentaa kuluihin kuvia kuiteista
- Listanäkymä veneen tapahtumiin vuosittain ja tapahtumalajeittain valittavana.

## Optiota lisäominaisuuksiksi
- Käyttäjä voi tallentaa veneen tietoihin tiedostoja kuten käyttöohjeita, kuvia ja osakkaiden keskinäisiä sopimuksia.
- Tapahtumien listanäkymän suodattaminen tarkemman ajanjakson ja osakkaan perusteella.
- Käyttäjä voi tehdä veneelle vuotuisen budjetin, jonka toteutumista voidaan seurata raporttinäkymässä.
- Varauskalenteri, jossa osakkaat voivat varata veneen käyttövuoroja.
- Varauskalenterin tapahtuman voi merkitä toteutuneeksi, jolloin se muuttuu tapahtumakirjaukseksi.
- Veneiden ja käyttäjien poistaminen / piilottaminen.
- Uuden käyttövuoden käynnistäminen, antaa jokaiselle osakkaalle oletusarvoisen käyttöaikakiintiön.
- Kirjattujen tapahtumien muokkaaminen.
- Raporttinäkymä aikasarjana, milloin venettä on käytetty ja kuinka paljon esim. viikottain.

## Tietokantakaavio
Tässä kuvattujen taulujen lisäksi tietokannassa on yksi näkymä eli view, jota käytetään raporttikuvaajien ja tapahtumalistauksen tekemiseen.

<img src='CoBoat.png'></img>

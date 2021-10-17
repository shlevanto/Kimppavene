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
- Käyttäjä voi luoda tiliinsä liittyvän uuden veneen, jonka osakas hän on. Käyttäjä voi olla osakkaana useammassa kuin yhdessä veneessä.
- Käyttäjä voi liittyä osakkaaksi olemassaolevaan veneeseen syöttämällä toiselta osakkaalta saamansa veneen avainkoodin järjestelmään.
- Käyttäjä voi tehdä tapahtumakirjauksia veneelle. Kirjattavat
tapahtumat ovat käyttö, talkootyö ja kustannukset.
- Käyttöoikeuskirjanpito. Veneelle on käyttäjäkohtainen, vuosittainen oletuskäyttöoikeus 12 päivää.
- Tehdyt talkootyöt kasvattavat käyttöoikeutta ja käyttö vähentää.
- Veneellä on yksi tai useampia pääkäyttäjiä, jotka voivat muokata veneen tietoja.
- Veneen luonut käyttäjä määrittyy aina luomansa veneen pääkäyttäjäksi.
- Järjestelmässä on raporttinäkymiä, joista veneen osakas voi seurata omaa ja muiden saman veneen osakkaiden käyttöä. Veneen käyttömäärä, tehtyjen talkootuntien määrä ja osakas- / venekohtaiset kulut ja investoinnit.
- Veneen pääkäyttäjä voi antaa muille veneen osakkaille pääkäyttäjän oikeudet.
- Kun luodaan uusi vene, sille määrittyy oletuskertoimet käyttöoikeuksien kertoimille. Kertoimet on määritelty viikkojen numeroiden perusteella. Ideana on, että lomakaudella käyttö syö enemmän käyttöoikeutta.
- Käyttöoikeuksien kertoimia voi määritellä pääkäyttäjänäkymässä.
- Käyttäjä voi tallentaa kuluihin kuvia kuiteista
- Listanäkymä veneen tapahtumiin

## Keskeneräiset toiminnallisuudet

## Toteuttamista odottavat toiminnallisuudet

## Optiota lisäominaisuuksista
- Käyttäjä voi tallentaa veneen tietoihin tiedostoja kuten käyttöohjeita, kuvia ja osakkaiden keskinäisiä sopimuksia.
- Listanäkymän suodattaminen tarkemman ajanjakson ja osakkaan perusteella.
- Käyttäjä voi tehdä veneelle vuotuisen budjetin, jonka toteutumista voidaan seurata raporttinäkymässä.
- Varauskalenteri, jossa osakkaat voivat varata veneen käyttövuoroja.
- Varauskalenterin tapahtuman voi merkitä toteutuneeksi, jolloin se muuttuu tapahtumakirjaukseksi

## Luonnos tietokantakaaviosta
<img src='CoBoat.png'> </img>

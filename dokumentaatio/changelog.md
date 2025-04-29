# viikko 3
- Käyttäjä näkee miinat sekä tyhjillä ruuduilla miinojen määrän lähietäisyydellä
- Testattu Board -luokan getNeighbours -metodia
- Käyttäjä pystyy klikkailemaan sekä flagaamaan, peli on nyt käytännössä toimiva
- Pelissä on kolme eri vaikeustasoa, easy (8x8), medium(16x16) ja hard(32x32). käyttäjä saa valita valita vaikeustason päävalikossa

# viikko 4
- Pelissä on nyt voitto/häviö -menu, josta pystyy yrittämään uudelleen tai palaamaan päävalikkoon.
- Ohjelman koodin laatua on paranneltu pylintin huomautuksien mukaisesti (tämänhetkinen arvosana 9.90/10)
- main.py ja game.py -tiedostoissa on käytössä # pylint: disable=no-member, sillä pylint ei osaa tunnistaa joitakin pygamen luomia ominaisuuksia ja metodeja

# viikko 5
- Peliin on lisätty ajastin, joka näkyy pelin ikkunassa, voittaessa aika tulee myös näkyviin ruudulle.
- Pelin koodia on restrukturoitu lisää (mm. lisätty Gameconfig -luokka)
- Ohjelman koodin laatua on paranneltu pylintin huomautuksien mukaisesti (tämänhetkinen arvosana 10/10)

# viikko 6
- Ohjelman luokille ja metodeille on lisätty dogstring-dokumentaatio
- Coverage-raportti näyttää nyt vain olelliset tiedostot (mm. käyttöliittymätiedosto game.py otettu pois)
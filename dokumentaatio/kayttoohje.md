# **Käyttöohje: Minesweeper**
- Siirry hakemistoon `minesweeper`
- Asenna Poetry (jos ei ole jo asennettuna)

## **Käynnistys**
- Käynnistä ohjelma komennolla
```poetry run invoke start``` (tai vaihtoehtoisesti ```python3 main.py```)

## **Testaus**
- Suorita testit komennolla
```poetry run invoke test```

## **Testikattavuuden tarkistaminen**
- Kerää kattavuustiedot komennolla
```poetry run invoke coverage```
- Luo kattavuusraportti komennolla
```poetry run invoke coverage-report```

## **Käynnistyminen**
- Sovellus käynnistyy päävalikkoon, josta pelaaja voi valita haluamansa pelimuodon
- Pelin voi lopettaa painamalla `quit` nappia päävalikossa

## **Mahdolliset virheilmoitukset poetryn käytön yhteydessä**
- Seuraaviin ongelmiin törmäsin testatessani ohjelmaa Cubbli Linux virtuaaliympäristössä:
- `Command not found: invoke`
    - asenna invoke komennolla ```poetry add python-invoke``` tai ```pip3 install invoke```
- `No module named 'pygame'`
    - Pygamen pitäisi olla valmiiksi asennettuna riippuvuutena, mutta komento ```poetry update package``` pitäisi korjata ongelman
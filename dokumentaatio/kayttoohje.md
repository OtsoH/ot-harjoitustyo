# **Käyttöohje: Minesweeper**
- Siirry hakemistoon `minesweeper`
- Asenna Poetry (jos ei ole jo asennettuna)

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
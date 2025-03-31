# **Määrittelydokumentti: Minesweeper**

## **1. Johdanto**
Minesweeper on klassinen yksinpelattava logiikkapeli, jossa pelaajan tavoitteena on löytää kaikki miinattomat ruudut pelilaudalta ilman, että osuu miinaan. Tämä projekti toteuttaa Minesweeper-pelin Pythonilla ja tarjoaa graafisen käyttöliittymän.

## **2. Toiminnalliset vaatimukset**

### **2.1 Perustoiminnallisuudet**
- Pelilauta koostuu ruudukosta, jossa on:
  - **Miinoja**: Piilotettuja ruutuja, jotka aiheuttavat pelin häviön, jos ne avataan.
  - **Numeroruudut**: Ruutuja, jotka näyttävät ympäröivien miinojen lukumäärän.
  - **Tyhjät ruudut**: Ruutuja, joissa ei ole miinoja eikä numeroita.
- Pelaaja voi:
  - **Avata ruutuja**: Paljastaa ruudun sisällön.
  - **Asettaa lippuja**: Merkitä ruutuja, joissa epäillään olevan miina.
- Peli päättyy:
  - **Voittoon**, kun kaikki miinattomat ruudut on avattu.
  - **Häviöön**, kun pelaaja avaa ruudun, jossa on miina.

### **2.2 Vaikeustasot**
- Pelissä on kolme vaikeustasoa:
  - **Helppo**: Pieni pelilauta ja vähän miinoja.
  - **Keskitaso**: Keskikokoinen pelilauta ja enemmän miinoja.
  - **Vaikea**: Suuri pelilauta ja paljon miinoja.

### **2.3 Graafinen käyttöliittymä**
- Pelissä on visuaalinen käyttöliittymä, joka näyttää:
  - Pelilaudan ja ruutujen tilan.
  - Miinojen ja lippujen määrän.
  - Pelin tilan (voitto/häviö).

## **4. Tekninen toteutus**
- **Ohjelmointikieli**: Python
- **Kirjastot**:
  - `pygame`: Käytetään graafisen käyttöliittymän toteutukseen.
  - `random`: Miinojen satunnaiseen sijoittamiseen.
- **Hakemistorakenne**:
  - `minesweeper/`: Sisältää pelin lähdekoodin.
  - `dokumentaatio/`: Sisältää projektin dokumentaation.
  - `images/`: Sisältää pelin graafiset elementit.
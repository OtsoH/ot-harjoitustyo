```mermaid
classDiagram
    Monopolipeli "1" -- "2" Noppa
    Monopolipeli "1" -- "1" Pelilauta
    Pelilauta "1" -- "40" Ruutu
    Ruutu "1" -- "1" Ruutu : seuraava
    Ruutu "1" -- "0..8" Pelinappula
    Pelinappula "1" -- "1" Pelaaja
    Pelaaja "2..8" -- "1" Monopolipeli
    Monopolipeli "1" -- "1" Aloitusruutu 
    Monopolipeli "1" -- "1" Vankila 
    SattumaJaYhteismaa "1" -- "0..*" Kortti
    Kortti "1" -- "1" Toiminto
    Ruutu "1" -- "1" Toiminto
    NormaaliKatu "1" -- "0..4" Talo
    NormaaliKatu "1" -- "0..1" Hotelli
    NormaaliKatu "1" -- "0..1" Pelaaja 
    Pelaaja "1" -- "1" Raha
    Ruutu <|-- Aloitusruutu
    Ruutu <|-- Vankila
    Ruutu <|-- SattumaJaYhteismaa
    Ruutu <|-- NormaaliKatu
    Ruutu <|-- AsemaJaLaitos
```
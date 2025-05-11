# **Arkkitehtuurikuvaus**

## **Rakenne**
```mermaid
classDiagram
    classDiagram
    Game "1" --> "1" GameUI
    Game "1" --> "1" GameLogic
    Game "1" --> "1" Board
    Game "1" --> "1" GameDatabase
    Game "1" --> "1" CustomGame
    Board "1" *-- "*" Piece
    Piece --> Piece
    CustomGame --> GameUI
    GameLogic --> Board
```

## **Käyttöliittymä**
- Käyttöliittymä sisältää itse pelinäkymän lisäksi kolme erillistä näkymää:
    - Päävalikko
    - Custom-pelimuodon valikko
    - Voitto/häviöruutu

- Käyttöliittymästä vastaa pääasiassa GameUI-luokka, joka tarjoaa metodit näkymien piirtämiseen ja käyttäjän interaktioiden käsittelyyn. Game-luokka toimii koordinaattorina, joka kutsuu GameUI-luokan metodeja tarpeen mukaan.
- Päävalikko on toteutettu Game-luokan main_menu -metodissa, näkymä piirretään GameUI-luokan draw_menu_screen-metodilla
- Custom-pelimudon valikko on toteutettu CustomGame-luokassa metodilla show_settings ja se käyttää GameUI-luokan metodeja käyttöliittymäelementtien kuten liukusäätimien piirtämiseen
- voitto/häviöruudut toteutetaan Game-luokan show_game_over_menu-metodissa, ruutu piirretään näytölle käyttäen GameUI-luokan draw_game_over_background-metodia

## **Päätoiminnallisuudet**

## **Pelin alustus ja voitto/häviötilanteet**
```mermaid
sequenceDiagram
    actor Player
    participant Game
    participant Board
    participant GameLogic
    participant GameDatabase
    participant GameUI

    Game->>Board: __init__(size, mines)
    Board->>Board: Luo ruudut (Piece)
    Board->>Board: set_board(num_mines) - Asettaa miinat satunnaisesti
    Board->>Board: set_neighbours() - Määrittää ruutujen naapurit
    Board->>Piece: set_num() - Laskee numeroarvot ruuduille
    Game->>GameLogic: __init__(board)
    Game->>Game: run() - Käynnistää pelisilmukan

    loop pelisilmukka
        Game->>GameLogic: update_time()
        Game->>Game: draw() - Päivittää näkymän

        alt pelaaja voittaa
            Board->>Game: get_won() = True
            Game->>Board: reveal_all() - Näyttää kaikki ruudut
            Game->>GameDatabase: save_score(difficulty, time)
            Game->>Game: show_game_over_menu(won=True) - Näyttää voittoilmoituksen
            Game->>Player: Näyttää Game Over -valikon
        else pelaaja häviää
            Board->>Game: get_lost() = True
            Game->>Board: reveal_all() - Näyttää kaikki ruudut
            Game->>Game: show_game_over_menu(won=False) - Näyttää häviöilmoituksen
            Game->>Player: Näyttää Game Over -valikon
        end
    end
```
- Pelin alussa Game-luokka luo Board-olion antaen sille pelilaudan koon ja miinojen määrän. Board-luokka alustaa pelilaudan luomalla Piece-oliot jokaiselle ruudulle, asettaa miinat satunnaisesti set_board-metodilla ja määrittää ruutujen naapurit set_neighbours-metodilla. Piece-oliot laskevat ympäröivien miinojen määrät set_num-metodilla. Game luo myös GameLogic-olion, joka saa parametrina pelilaudan. Pelin käynnistyessä Game-luokka aloittaa pelisilmukan run-metodilla, joka päivittää peliaikaa, käsittelee pelaajan syötteet ja piirtää pelilaudan. Pelisilmukassa tarkistetaan jatkuvasti, onko peli voitettu tai hävitty. Jos pelaaja voittaa (kaikki miinattomat ruudut avattu), Board-luokka ilmoittaa voitosta, Game-luokka paljastaa kaikki ruudut, tallentaa tuloksen tietokantaan ja näyttää voittoilmoituksen sekä Game Over -valikon. Jos pelaaja häviää (avaa miinan), Board-luokka ilmoittaa häviöstä, Game-luokka paljastaa kaikki ruudut ja näyttää häviöilmoituksen sekä Game Over -valikon.

## Ruudun klikkaaminen
```mermaid
sequenceDiagram
    actor Player
    participant Game
    participant GameLogic
    participant Board
    participant Piece

    Player->>Game: Hiiren klikkaus (sijainti, flagging)
    Game->>GameLogic: handle_click(position, piece_size, flagging)
    GameLogic->>Board: get_piece(idx)
    Board-->>GameLogic: piece
    GameLogic->>Board: clicking(piece, flagging)

    alt flagging on True
        Board->>Piece: set_flagged()
        Piece-->>Board: None
    else flagging on False
        Board->>Piece: click()
        Piece->>Piece: revealed = True

        alt piece.get_has_mine()
            Board->>Board: lost = True
        else piece.get_num() == 0
            loop naapureille
                Piece->>Piece: get_neighbours()
                Board->>Board: clicking(neighbour, False)
            end
        else
            Board->>Board: num_clicked += 1
        end
    end
```

- Kun pelaaja klikkaa ruutua pelilaudalla, käyttöliittymän tapahtumankäsittelijä kutsuu Game-luokan metodia, joka välittää klikkauksen sijainnin ja mahdollisen lippuasetuksen (flagging) GameLogic -luokalle. GameLogic selvittää Board-luokan avulla, mikä ruutu (Piece-olio) on kyseessä. Board palauttaa Piece-olion, ja GameLogic pyytää Boardia käsittelemään klikkauksen. Jos kyseessä on lippu, Board kutsuu Piece-olion set_flagged-metodia, joka asettaa tai poistaa lipun ruudusta. Jos kyseessä ei ole lippu, Board kutsuu Piece-olion click-metodia, joka paljastaa ruudun. Jos ruudussa on miina, Board asettaa pelin hävityksi. Jos ruudussa ei ole miinaa ja sen arvo on 0, Board avaa rekursiivisesti kaikki naapuriruudut. Muussa tapauksessa Board kasvattaa avattujen ruutujen laskuria. Lopputuloksena pelilauta päivittyy ja peli etenee klikkauksen mukaisesti.

## Highscoren tallennus ja näyttäminen

```mermaid
sequenceDiagram
    participant Game
    participant GameLogic
    participant GameDatabase
    participant GameUI

    GameLogic->>Game: Peli päättyy voittoon (voittoehdon täyttyminen)
    Game->>GameDatabase: save_score(difficulty, elapsed_time)
    GameDatabase-->>Game: Tallennus valmis
    Game->>GameDatabase: get_high_scores(difficulty)
    GameDatabase-->>Game: Paras aika
    Game->>GameUI: prepare_all_highscores()
    GameUI-->>Game: Highscore-pinnat valmiina
    Game->>GameUI: display_all_highscores(buttons)
    GameUI-->>Game: Highscore-näyttö päivitetty
```

- Kun peli päättyy voittoon, GameLogic-luokka ilmoittaa Game-luokalle voittoehdon täyttymisestä. Game-luokka kutsuu tietokantakerroksen (GameDatabase) save_score-metodia ja antaa parametriksi vaikeustason sekä peliajan. GameDatabase tarkistaa, onko uusi aika parempi kuin aiempi, ja tallentaa sen tarvittaessa. Tämän jälkeen Game hakee parhaat ajat kutsumalla GameDatabase:n get_high_scores-metodia.  Saatuaan parhaat ajat Game päivittää highscore-näytöt kutsumalla omaa prepare_all_highscores-metodiaan, joka luo highscore-tekstit GameUI:n avulla. Game päivittää highscore-näytöt kutsumalla omia prepare_all_highscores- ja display_all_highscores-metodejaan, jotka käyttävät GameUI:ta piirtämiseen. Näin päivitetyt highscoret näytetään päävalikossa pelaajalle.
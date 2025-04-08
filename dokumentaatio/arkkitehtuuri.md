# **Minimalistinen luokkakaavio**
```mermaid
classDiagram
    Game --> Board
    Board *-- Piece
    Piece --> Piece

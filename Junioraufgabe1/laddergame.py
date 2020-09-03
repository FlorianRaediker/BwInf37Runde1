# !/usr/bin/env python3
"""
Geschrieben für den 37. Bundeswettbewerb Informatik 2018
Autor: Florian Rädiker
Team-ID: 00133

Junioraufgabe 1: 'Auf und Ab'

PYTHON3

Simuliert beim Ausführen Leiterspiele, bei denen der jeweilige Spieler nur die Augenzahlen 1, 2, 3, 4, 5 oder 6 würfelt.
Für mehr Informationen siehe die Aufgabendokumentation.
"""
import enum


class LadderGameSimulator:
    class GameState(enum.Enum):
        SameField = 0
        Valid = 1
        Won = 2

    SameField = GameState.SameField
    Valid = GameState.Valid
    Won = GameState.Won

    ladder_pairs = (
        (6, 27),
        (14, 19),
        (21, 53),
        (31, 42),
        (33, 38),
        (46, 62),
        (51, 59),
        (57, 96),
        (65, 85),
        (68, 80),
        (70, 76),
        (92, 98)
    )
    LADDERS = {i: j for i, j in ladder_pairs + tuple((y, x) for x, y in ladder_pairs)}
    
    def __init__(self, players):
        self.players = list(players)
        self.reset()

    def reset(self):
        for player in self.players:
            player.reset(self)
        self.is_finished = False

    def do_move(self, player_num, fields):
        if self.is_finished:
            return
        player = self.players[player_num]
        code = player.move(fields)
        if code == self.SameField:
            # trapped on this field before
            return self.SameField
        elif code == self.Won:  # won
            self.won(player)
            return self.Won

    def won(self, player):
        self.is_finished = True
        print("Spieler '" + str(player.name) + "' hat in", player.moves, "Spielzügen gewonnen!")


class LadderGamePlayer:
    def __init__(self, position=0, name="Spieler"):
        self.name = name
        self.moves = 0
        self._position = position
        self.done_fields = set()
        self.game_manager = None
    
    def move(self, fields):
        return self.set_position(self._position + fields)

    def set_position(self, value):
        self.moves += 1
        print(str(self.moves) + ") move to", value)
        if value > 100:
            # player trespassed the goal
            self._position = 200 - value
            print("  Ziel nicht exakt erreicht. Gehe zurück auf", self._position)
        else:
            self._position = value
        
        if self._position in self.game_manager.LADDERS:
            # go to other lend of ladder
            self._position = self.game_manager.LADDERS[self._position]
            print("  jumping to", self._position)
        if self._position in self.done_fields:
            print("Bereits betreten")
            return LadderGameSimulator.SameField
        if self._position == 100:
            # player won
            return LadderGameSimulator.Won
        # everythin is valid, the position is added to the fields the player already entered
        self.done_fields.add(self._position)
        return LadderGameSimulator.Valid
    
    
    @property
    def position(self):
        return self._position

    def reset(self, game_manager):
        self.game_manager = game_manager
        self._position = 0
        self.moves = 0
        self.done_fields = set()


if __name__ == "__main__":
    print("DIESES PROGRAMM SIMULIERT LEITERSPIELE NACH EINER AUFGABE IM BUNDESWETTBEWERB INFORMATIK 2018\n"
          "ERSTELLT VON FLORIAN RÄDIKER")
    player = LadderGamePlayer()
    game = LadderGameSimulator((player,))
    for spots in range(1, 7):
        game.reset()
        player.name = "Spieler" + str(spots)
        print("\n########\nVersuche Augenzahl", spots)
        while True:
            code = game.do_move(0, spots)
            if code == game.SameField:
                print("Auf diesem Feld war der Spieler schon...")
                print("Spieler kann nicht gewinnen")
                break
            elif code == game.Won:
                break  # won
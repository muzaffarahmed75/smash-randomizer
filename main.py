from random import choice
from os import system

class Player:

    with open('characters.txt') as f:
        characters = [line.rstrip('\n') for line in f]
    freshness = 5

    def __init__(self, name):
        self.name = name
        self.queue = list()

    def __str__(self):
        return self.name

    def get_random(self):
        pick = choice([x for x in self.characters if x not in self.queue])
        while len(self.queue) >= self.freshness:
            self.queue.pop(0)
        self.queue.append(pick)
        return pick


def status(players, lobby):
    print("\nPlaying:")
    for port, player in enumerate(players):
        if player:
            print("P", port+1, "    ", player.name, sep="")
        else:
            print("P", port+1, sep="")
    if lobby:
        print("\nLobby:")
        for player in lobby:
            print(player)


def ansi_color(text, *attributes):
    """
    Formats/highlights text to be printed on the console as per the ANSI
    coloring scheme.
    """
    return "\x1b[{}m{}\x1b[0m".format(";".join(map(str, attributes)), text)


def main():

    system("")
    players = [None] * 4
    lobby = []
    with open('stages.txt') as f:
        stages = [line.rstrip('\n') for line in f]
    colors = [31, 34, 33, 32]
    stage_queue = []
    stage_freshness = 2*len(stages)//3

    while True:
        command = list(input(ansi_color("\nmelee@smash:$ ", 1, 36)).split())
        if len(command) == 1:
            if command[0] == "run":
                print("\nPort  Name      Character")
                print("-"*26)
                for port, player in enumerate(players):
                    if player:
                        line = ansi_color("P{0}    {1: <9} {2}".format(
                            port+1, player.name, players[port].get_random()), 1, colors[port])
                    else:
                        line = ansi_color("P"+str(port+1), colors[port])
                    print(line)
                print(ansi_color("\nStage"), end=": ")
                pick = choice([x for x in stages if x not in stage_queue])
                while len(stage_queue) >= stage_freshness:
                    stage_queue.pop(0)
                stage_queue.append(pick)
                print(ansi_color(choice(stages), 1, 35))
            elif command[0] == "status":
                status(players, lobby)
            elif command[0] in ("clear", "reset"):
                players = [None] * 4
                lobby = []
            elif command[0] in ("quit", "exit"):
                print("Exiting...")
                break
            else:
                print("Invalid command.")

        elif len(command) == 2:
            command[1] = command[1].upper()
            if command[0] == "leave":
                if command[1][0] == 'P' and command[1][1:] in list("1234"):
                    port = int(command[1][1:]) - 1
                    print("{} has left port {}.".format(players[port], port+1))
                    lobby.append(players[port])
                    players[port] = None
                elif command[1][0] == 'L' and command[1][1:] in map(str, range(1, len(lobby)+1)):
                    pos = int(command[1][1:]) - 1
                    print("{} has left the lobby.".format(lobby[pos].name, port+1))
                    lobby.pop(pos)
                else:
                    print("Invalid port/lobby number.")
                status(players, lobby)
            elif command[0] == "freshness":
                try:
                    freshness = int(command[1])
                    if freshness < 1 or freshness > 24:
                        raise ValueError
                    Player.freshness = freshness
                except ValueError:
                    print("freshness must be an integer from 1 to 24.")
            else:
                print("Invalid command.")

        elif len(command) == 3:
            if command[0] == "join":
                if command[1][0] == 'P' and command[1][1:] in list("1234"):
                    port = int(command[1][1:]) - 1
                    name = command[2]
                    if players[port]:
                        res = input("Swap {} out for {} at port {}? [Y/N] ".format(
                            players[port], command[2], port+1
                        )).upper()
                        if res == 'Y':
                            lobby.append(players[port])
                            print("\n{} moved to the lobby.".format(players[port]))
                        else:
                            continue
                    players[port] = Player(name)
                    print("{} joined at port {}.".format(name, port+1))
                else:
                    print("Invalid port number.")
                status(players, lobby)
            elif command[0] == "swap":
                if command[1][0] not in "PL" or command[2][0] not in "PL":
                    print("Invalid port/lobby number(s).")
                    continue
                idx1 = -1
                if command[1][0] == 'P':
                    try:
                        idx1 = int(command[1][1:])-1
                        if not players[idx1]:
                            raise IndexError
                    except:
                        print("Invalid port number.")
                        continue
                if command[2][0] == 'P':
                    try:
                        idx2 = int(command[2][1:])-1
                        if not players[idx2]:
                            raise IndexError
                        command[1], command[2] = command[2], command[1]
                        idx1, idx2 = idx2, idx1
                    except:
                        print("Invalid port number.")
                        continue
                if command[2][0] == 'L':
                    try:
                        idx2 = int(command[2][1:])-1
                        if not lobby[idx2]:
                            raise IndexError
                    except:
                        print("Invalid lobby number.")
                        continue
                if command[1][0] == 'P':
                    if command[2][0] == 'P':
                        print("{} swapped with {}.".format(players[idx1], players[idx2]))
                        players[idx1], players[idx2] = players[idx2], players[idx1]
                    else:
                        print("{} swapped out for {}.".format(players[idx1], lobby[idx2]))
                        players[idx1], lobby[idx2] = lobby[idx2], players[idx1]
                else:
                    print("{} swapped with {}.".format(lobby[idx1], lobby[idx2]))
                    lobby[idx1], lobby[idx2] = lobby[idx2], lobby[idx1]
                status(players, lobby)
            else:
                print("Invalid command.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
    except EOFError:
        print("Exiting...")

"""Player walker that explores the randomly generated maze."""

import random;

node Room {
    has id: str;
    has x: int;
    has y: int;
    has neighbors: dict[str, Room] = {};
    has description: str = "";
    has is_start: bool = False;
    has is_exit: bool = False;
    has has_key: bool = False;
    has has_treasure: bool = False;
    has has_monster: bool = False;
    has has_trap: bool = False;
    has visited: bool = False;
}

edge Passage {
    has direction: str = "";
}

walker Player {
    has health: int = 3;
    has has_key: bool = False;
    has treasure: int = 0;
    has steps: int = 0;
    has alive: bool = True;
    has victory: bool = False;
    has history: list[str] = [];

    can play with Room entry {
        here.visited = True;
        self.history.append(here.id);
        while self.alive and not self.victory {
            self.describe_room(here);
            self.resolve_room(here);
            if not self.alive {
                break;
            }
            if here.is_exit {
                if self.has_key {
                    print("You unlock the door with the key and escape the maze! 🎉");
                    self.victory = True;
                    break;
                } else {
                    print("The exit is locked. You need a key.");
                }
            }
            command = self.prompt_action(here);
            if command == "quit" {
                print("You decide to leave the maze for now.");
                break;
            }
            if command == "status" {
                self.print_status();
                continue;
            }
            if command == "help" {
                self.print_help(here);
                continue;
            }
            if command == "map" {
                self.print_history();
                continue;
            }
            next_room = here.neighbors.get(command);
            if next_room {
                self.steps += 1;
                visit next_room;
                here.visited = True;
                self.history.append(here.id);
            } else {
                print("You can't go that way.");
            }
        }
        if not self.alive {
            print("You collapse in the maze. Game over.");
        } elif not self.victory {
            print("Thanks for exploring the maze!");
        }
        disengage;
    }

    def resolve_room(room: Room) {
        if room.has_monster {
            print("A lurking monster attacks!");
            outcome = random.randint(1, 6);
            if outcome <= 2 {
                self.health -= 2;
                print("The monster wounds you badly (-2 health).");
                if self.health <= 0 {
                    self.alive = False;
                    return;
                }
            } else {
                print("You fend off the monster!");
                room.has_monster = False;
            }
        }
        if not self.alive {
            return;
        }
        if room.has_trap {
            print("A hidden trap springs! (-1 health)");
            self.health -= 1;
            room.has_trap = False;
            if self.health <= 0 {
                self.alive = False;
                return;
            }
        }
        if room.has_key and not self.has_key {
            self.has_key = True;
            room.has_key = False;
            print("You pick up a gleaming key.");
        }
        if room.has_treasure {
            self.treasure += 1;
            room.has_treasure = False;
            print("You scoop up some treasure!");
        }
    }

    def describe_room(room: Room) {
        print("\n" + "-" * 50);
        print(f"You are in {room.id}.");
        if room.description {
            print(room.description);
        }
        exits = ", ".join(sorted(room.neighbors.keys()));
        print(f"Visible exits: {exits}");
    }

    def prompt_action(room: Room) -> str {
        prompt = "Choose a direction or type 'status', 'map', 'help', or 'quit': ";
        while True {
            choice = input(prompt).strip().lower();
            if choice {
                return choice;
            }
            print("Please enter a command.");
        }
    }

    def print_status() {
        print(f"Health: {self.health}");
        key_status = "Yes" if self.has_key else "No";
        print(f"Key: {key_status}");
        print(f"Treasure collected: {self.treasure}");
        print(f"Steps taken: {self.steps}");
    }

    def print_help(room: Room) {
        print("Commands: direction names (e.g., north), status, map, help, quit.");
        print("Explore the maze, find the key, and escape through the exit.");
    }

    def print_history() {
        print("Visited rooms:");
        idx = 1;
        for rid in self.history {
            print(f"  {idx}. {rid}");
            idx += 1;
        }
    }
}

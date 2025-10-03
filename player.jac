"""Player walker that explores the randomly generated maze.

AI hints use the Gemini model through ByLLM. Set `GOOGLE_API_KEY` or
`GEMINI_API_KEY` in the environment before launching the maze to enable
those hints. When neither is set, the player proceeds without LLM support.
"""

import os;
import random;
import from byllm { Model }

glob GEMINI_API_ENV_VARS = ["GOOGLE_API_KEY", "GEMINI_API_KEY"];

glob DEFAULT_SECRET_PATHS = [
    os.getenv("MAZE_SECRETS_FILE"),
    os.path.expanduser("~/.config/maze-secrets.env"),
    os.path.expanduser("~/.maze-secrets"),
];

def _load_from_secret_files() -> str | None {
    for maybe_path in DEFAULT_SECRET_PATHS {
        if not maybe_path {
            continue;
        }
        cleaned_path = maybe_path.strip();
        if not cleaned_path {
            continue;
        }
        if not os.path.exists(cleaned_path) {
            continue;
        }
        try {
            with open(cleaned_path, "r") as secrets_file {
                for raw_line in secrets_file {
                    line = raw_line.strip();
                    if not line or line.startswith("#") {
                        continue;
                    }
                    for env_name in GEMINI_API_ENV_VARS {
                        prefix_options = [f"export {env_name}=", f"{env_name}="];
                        for prefix in prefix_options {
                            if not line.startswith(prefix) {
                                continue;
                            }
                            value = line[len(prefix):].strip();
                            if len(value) >= 2 {
                                first_code = ord(value[0]);
                                if first_code == ord(value[-1]) {
                                    if first_code == 34 or first_code == 39 {
                                        value = value[1:-1];
                                    }
                                }
                            }
                            if value {
                                os.environ[env_name] = value;
                                return value;
                            }
                        }
                    }
                }
            }
        } except Exception as err {
            print(f"Warning: unable to read secret file {cleaned_path}: {err}");
        }
    }
    return None;
}

def _load_gemini_api_key() -> str | None {
    for var_name in GEMINI_API_ENV_VARS {
        value = os.getenv(var_name);
        if value {
            return value;
        }
    }
    return _load_from_secret_files();
}

glob gemini_api_key = _load_gemini_api_key();

glob hint_llm = Model(
    model_name="gemini/gemini-2.0-flash",
    verbose=False,
    api_key=gemini_api_key,
);

"""Generate a concise hint that helps the player progress in the maze."""
def generate_hint(
    room_name: str,
    room_description: str,
    exits: list[str],
    has_key: bool,
    threats: list[str],
) -> str by hint_llm();

node Room {
    has id: str;
    has x: int;
    has y: int;
    has neighbors: dict[str, Room];
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
    has hint_warning_shown: bool = False;

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
            if command == "hint" {
                self.provide_hint(here);
                continue;
            }
            next_room = here.neighbors.get(command);
            if next_room {
                self.steps += 1;
                here = next_room;
                if not here.visited {
                    here.visited = True;
                }
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
        prompt = "Choose a direction or type 'status', 'map', 'help', 'hint', or 'quit': ";
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

    def provide_hint(room: Room) {
        exits = sorted(room.neighbors.keys());
        threats = [];
        if room.has_monster {
            threats.append("monster");
        }
        if room.has_trap {
            threats.append("trap");
        }
        if not gemini_api_key {
            if not self.hint_warning_shown {
                print("AI hint unavailable. Set GOOGLE_API_KEY or GEMINI_API_KEY and restart.");
                self.hint_warning_shown = True;
            }
            return;
        }
        try {
            hint = generate_hint(
                room_name=room.id,
                room_description=room.description,
                exits=exits,
                has_key=self.has_key,
                threats=threats,
            );
            print(f"AI hint: {hint}");
        } except Exception as err {
            print("AI hint unavailable. Rely on your instincts!");
            print(f"(details: {err})");
        }
    }
}

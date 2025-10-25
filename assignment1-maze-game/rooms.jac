"""Graph entities for the Maze Explorer game."""

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
    has direction: str;
}

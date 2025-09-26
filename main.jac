"""Maze Explorer Game entry point."""

import random;
import player;

def opposite_direction(direction: str) -> str {
    if direction == "north" {
        return "south";
    }
    if direction == "south" {
        return "north";
    }
    if direction == "east" {
        return "west";
    }
    return "east";
}

def connect_rooms(a: player.Room, b: player.Room, direction: str) {
    opp = opposite_direction(direction);
    a.neighbors[direction] = b;
    b.neighbors[opp] = a;
    a +>:player.Passage:direction=direction:+> b;
    b +>:player.Passage:direction=opp:+> a;
}

def carve_maze(grid: list[list[player.Room]], width: int, height: int) {
    dirs = [
        ("north", 0, -1),
        ("south", 0, 1),
        ("east", 1, 0),
        ("west", -1, 0),
    ];
    visited = set();
    stack = [];
    start = grid[0][0];
    stack.append(start);
    visited.add((start.x, start.y));
    while stack {
        current = stack[-1];
        cx = current.x;
        cy = current.y;
        options = [];
        for entry in dirs {
            dir_name = entry[0];
            dx = entry[1];
            dy = entry[2];
            nx = cx + dx;
            ny = cy + dy;
            if nx >= 0 and nx < width and ny >= 0 and ny < height {
                if (nx, ny) not in visited {
                    neighbor = grid[ny][nx];
                    options.append((dir_name, neighbor));
                }
            }
        }
        if options {
            random.shuffle(options);
            choice = options[0];
            direction = choice[0];
            next_room = choice[1];
            connect_rooms(current, next_room, direction);
            visited.add((next_room.x, next_room.y));
            stack.append(next_room);
        } else {
            stack.pop();
        }
    }
}

def choose_exit(start: player.Room, candidates: list[player.Room]) -> player.Room {
    farthest = candidates[0];
    max_dist = -1;
    for room in candidates {
        dist = abs(room.x - start.x) + abs(room.y - start.y);
        if dist > max_dist {
            max_dist = dist;
            farthest = room;
        }
    }
    return farthest;
}

def build_maze(width: int=4, height: int=4) -> dict[str, any] {
    flavors = [
        "Cobwebs cover the corners.",
        "A cold draft whispers through the stones.",
        "You hear distant dripping water.",
        "Faint torchlight flickers along the walls.",
        "Broken pottery litters the floor.",
        "The scent of damp earth fills the room.",
    ];
    grid = [];
    all_rooms = [];
    for y=0 to y<height by y+=1 {
        row = [];
        for x=0 to x<width by x+=1 {
            label = f"Room ({x}, {y})";
            desc = random.choice(flavors);
            new_room = player.Room(id=label, x=x, y=y, description=desc);
            new_room.neighbors = {};
            row.append(new_room);
            all_rooms.append(new_room);
        }
        grid.append(row);
    }
    carve_maze(grid, width, height);
    start_room = grid[0][0];
    start_room.is_start = True;
    start_room.description = "The maze entrance glows with faint light.";

    others = [];
    for room in all_rooms {
        if room is not start_room {
            others.append(room);
        }
    }

    exit_room = choose_exit(start_room, others);
    exit_room.is_exit = True;
    exit_room.description += " A heavy door marked 'EXIT' stands here.";
    others.remove(exit_room);

    key_room = random.choice(others);
    key_room.has_key = True;
    key_room.description += " A metal key lies on a pedestal.";
    others.remove(key_room);

    treasure_count = min(2, len(others));
    if treasure_count > 0 {
        treasure_rooms = random.sample(others, treasure_count);
        for room in treasure_rooms {
            room.has_treasure = True;
            room.description += " Glittering treasure catches your eye.";
            others.remove(room);
        }
    }

    monster_pool = [room for room in others];
    monster_count = min(2, len(monster_pool));
    if monster_count > 0 {
        monster_rooms = random.sample(monster_pool, monster_count);
        for room in monster_rooms {
            room.has_monster = True;
            room.description += " Something growls from the shadows.";
            others.remove(room);
        }
    }

    trap_pool = [room for room in others];
    trap_count = min(2, len(trap_pool));
    if trap_count > 0 {
        trap_rooms = random.sample(trap_pool, trap_count);
        for room in trap_rooms {
            room.has_trap = True;
            room.description += " A suspicious pressure plate rests underfoot.";
        }
    }

    return {
        "grid": grid,
        "start": start_room,
        "exit": exit_room,
        "key": key_room,
        "rooms": all_rooms,
    };
}

with entry {
    random.seed();
    print("Welcome to the Maze Explorer Game!\n");
    maze = build_maze(width=5, height=5);
    start_room = maze["start"];
    print("A maze has been created. Find the key and escape!\n");
    player.Player() spawn start_room;
}

from itertools import permutations
from collections import deque, defaultdict

# --- define nodes and adjacency ---
nodes = [
    (0,0),(2,0),(4,0),
    (1,1),(3,1),
    (0,2),(2,2),(4,2),
    (1,3),(3,3),
    (0,4),(2,4),(4,4)
]

def adjacent(a,b):
    dx,dy = abs(a[0]-b[0]), abs(a[1]-b[1])
    return (dx==2 and dy==0) or (dx==0 and dy==2) or (dx==1 and dy==1)

adj = {n:[b for b in nodes if b!=n and adjacent(n,b)] for n in nodes}

# --- shortest paths BFS ---
def all_shortest_paths(start, goal):
    if start==goal:
        return [[start]]
    q = deque([[start]])
    visited = {start:0}
    shortest = None
    paths = []
    while q:
        path = q.popleft()
        cur = path[-1]
        dist = len(path)-1
        if shortest is not None and dist>shortest:
            break
        if cur==goal:
            shortest = dist
            paths.append(path)
            continue
        for nxt in adj[cur]:
            if nxt not in visited or visited[nxt]>=dist+1:
                visited[nxt]=dist+1
                q.append(path+[nxt])
    return paths

# --- geometry helpers ---
def is_90_turn(v1,v2):
    return v1[0]*v2[0] + v1[1]*v2[1] == 0

def path_has_90_turn(path):
    for i in range(1,len(path)-1):
        a,b,c = path[i-1],path[i],path[i+1]
        v1 = (b[0]-a[0], b[1]-a[1])
        v2 = (c[0]-b[0], c[1]-b[1])
        if is_90_turn(v1,v2):
            return True
    return False

def attacked_nodes(enemy,target):
    paths = all_shortest_paths(enemy,target)
    valid = [p for p in paths if not path_has_90_turn(p)]
    if not valid:
        return {enemy,target}
    return set().union(*valid)

# --- pretty printer ---
def draw_attack(enemy,target,hit_nodes):
    grid = [['.' for _ in range(5)] for _ in range(5)]
    for (x,y) in hit_nodes:
        grid[y][x] = '*'
    ex,ey = enemy
    tx,ty = target
    grid[ey][ex] = 'E'
    grid[ty][tx] = 'T'
    print(f"\nEnemy {enemy} → Target {target}")
    for row in grid:
        print(' '.join(row))
    print()

# --- stats and optional visualization ---
stats = defaultdict(list)

for enemy,target in permutations(nodes,2):
    paths = all_shortest_paths(enemy,target)
    dist = len(paths[0])-1
    hits = attacked_nodes(enemy,target)
    stats[dist].append(len(hits))

# --- overall average ---
all_hits = [h for lst in stats.values() for h in lst]
overall_avg = sum(all_hits) / len(all_hits)
print(f"\nOverall average nodes hit (all distances): {overall_avg:.3f}")

# optional: breakdown by distance
for d in sorted(stats):
    print(f"Distance {d}: {len(stats[d])} pairs, avg = {sum(stats[d])/len(stats[d]):.3f}")

# --- summary ---
for d in [1,2,3,4]:
    vals = stats[d]
    avg = sum(vals)/len(vals)
    print(f"Distance {d}: {len(vals)} pairs, avg hit = {avg:.3f}, distribution:",
          {v:vals.count(v) for v in sorted(set(vals))})

# --- sample drawings ---
samples = [
    ((0,0),(4,0)),   # straight horizontal
    ((0,0),(3,1)),   # diagonal blend
    ((0,0),(4,2)),   # longer diagonal-ish
    ((0,0),(2,4)),   # downward diagonal
]
for e,t in samples:
    draw_attack(e,t, attacked_nodes(e,t))

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
from collections import deque
import heapq
import random


ROWS = 10
COLS = 10
START = (1, 1)
GOAL = (8, 8)
DYNAMIC_PROB = 0.05
DIRECTIONS = [(-1,0),(0,1),(1,0),(1,1),(0,-1),(-1,-1),(-1,1),(1,-1)]

COLORS = {
    'start':    '#1565C0',
    'goal':     '#2E7D32',
    'dynamic':  '#E65100',
    'frontier': '#00ACC1',
    'visited':  '#9E9E9E',
    'path':     '#F9A825',
    'current':  '#AB47BC',
    'replan':   '#FF1744',
    'bg':       '#E8E8E8',
    'grid':     '#424242',
}


def build_grid():
    return {
        'rows': ROWS,
        'cols': COLS,
        'start': START,
        'goal': GOAL,
        'dynamic_obstacles': set(),
    }


def is_valid(grid, pos):
    r, c = pos
    if r < 0 or r >= grid['rows'] or c < 0 or c >= grid['cols']:
        return False
    if pos in grid['dynamic_obstacles']:
        return False
    return True


def get_neighbors(grid, pos):
    r, c = pos
    result = []
    for dr, dc in DIRECTIONS:
        np_ = (r + dr, c + dc)
        if is_valid(grid, np_):
            cost = 1.414 if (dr != 0 and dc != 0) else 1.0
            result.append((np_, cost))
    return result


def add_dynamic_obstacle(grid):
    if random.random() >= DYNAMIC_PROB:
        return
    candidates = [
        (r, c)
        for r in range(grid['rows'])
        for c in range(grid['cols'])
        if (r, c) != grid['start']
        and (r, c) != grid['goal']
        and (r, c) not in grid['dynamic_obstacles']
    ]
    if candidates:
        grid['dynamic_obstacles'].add(random.choice(candidates))


def path_blocked(grid, path):
    return any(p in grid['dynamic_obstacles'] for p in path[1:-1])


def make_step(current, frontier, visited, replan=False):
    return {
        'current': current,
        'frontier': list(frontier),
        'visited': visited.copy(),
        'replan': replan,
    }


def reconstruct_path(came_from, goal):
    path, node = [goal], goal
    while came_from.get(node) is not None:
        node = came_from[node]
        path.append(node)
    path.reverse()
    return path


def merge_paths(fwd_parent, bwd_parent, meeting):
    path_fwd, node = [], meeting
    while node is not None:
        path_fwd.append(node)
        node = fwd_parent.get(node)
    path_fwd.reverse()
    path_bwd, node = [], bwd_parent.get(meeting)
    while node is not None:
        path_bwd.append(node)
        node = bwd_parent.get(node)
    return path_fwd + path_bwd


def with_replan(algo_fn, grid, *args):
    all_steps = []
    for attempt in range(4):
        steps, path = algo_fn(grid, *args)
        all_steps.extend(steps)
        if attempt > 0 and all_steps:
            all_steps[-len(steps)]['replan'] = True
        if not path or not path_blocked(grid, path):
            return all_steps, path
    return all_steps, path


def bfs(grid):
    queue = deque([grid['start']])
    in_queue = {grid['start']}
    came_from = {grid['start']: None}
    visited = set()
    steps = []

    while queue:
        current = queue.popleft()
        in_queue.discard(current)
        add_dynamic_obstacle(grid)
        steps.append(make_step(current, queue, visited))

        if current == grid['goal']:
            return steps, reconstruct_path(came_from, current)

        if current in visited:
            continue
        visited.add(current)

        for nbr, _ in get_neighbors(grid, current):
            if nbr not in visited and nbr not in in_queue:
                queue.append(nbr)
                in_queue.add(nbr)
                came_from[nbr] = current

    return steps, []


def dfs(grid):
    stack = [grid['start']]
    came_from = {grid['start']: None}
    visited = set()
    steps = []

    while stack:
        current = stack.pop()
        add_dynamic_obstacle(grid)
        steps.append(make_step(current, stack, visited))

        if current == grid['goal']:
            return steps, reconstruct_path(came_from, current)

        if current in visited:
            continue
        visited.add(current)

        for nbr, _ in reversed(get_neighbors(grid, current)):
            if nbr not in visited:
                stack.append(nbr)
                if nbr not in came_from:
                    came_from[nbr] = current

    return steps, []


def ucs(grid):
    counter = 0
    heap = [(0, counter, grid['start'])]
    came_from = {grid['start']: None}
    cost_so_far = {grid['start']: 0}
    visited = set()
    steps = []

    while heap:
        cur_cost, _, current = heapq.heappop(heap)
        add_dynamic_obstacle(grid)
        steps.append(make_step(current, [i[2] for i in heap], visited))

        if current == grid['goal']:
            return steps, reconstruct_path(came_from, current)

        if current in visited:
            continue
        visited.add(current)

        for nbr, edge_cost in get_neighbors(grid, current):
            new_cost = cur_cost + edge_cost
            if nbr not in cost_so_far or new_cost < cost_so_far[nbr]:
                cost_so_far[nbr] = new_cost
                counter += 1
                heapq.heappush(heap, (new_cost, counter, nbr))
                came_from[nbr] = current

    return steps, []


def dls(grid, limit=15):
    stack = [(grid['start'], 0)]
    came_from = {grid['start']: None}
    visited = set()
    steps = []

    while stack:
        current, depth = stack.pop()
        add_dynamic_obstacle(grid)
        steps.append(make_step(current, [i[0] for i in stack], visited))

        if current == grid['goal']:
            return steps, reconstruct_path(came_from, current)

        if current in visited or depth >= limit:
            continue
        visited.add(current)

        for nbr, _ in reversed(get_neighbors(grid, current)):
            if nbr not in visited:
                stack.append((nbr, depth + 1))
                if nbr not in came_from:
                    came_from[nbr] = current

    return steps, []


def iddfs(grid):
    all_steps = []
    for depth_limit in range(50):
        steps, path = dls(grid, depth_limit)
        all_steps.extend(steps)
        if path:
            if path_blocked(grid, path):
                extra, path = with_replan(dls, grid, depth_limit)
                all_steps.extend(extra)
            return all_steps, path
    return all_steps, []


def bidirectional(grid):
    fwd_queue = deque([grid['start']])
    fwd_visited = {grid['start']}
    fwd_parent = {grid['start']: None}
    bwd_queue = deque([grid['goal']])
    bwd_visited = {grid['goal']}
    bwd_parent = {grid['goal']: None}
    steps = []

    while fwd_queue or bwd_queue:
        if fwd_queue:
            cur_f = fwd_queue.popleft()
            add_dynamic_obstacle(grid)
            steps.append(make_step(cur_f, list(fwd_queue) + list(bwd_queue), fwd_visited | bwd_visited))
            if cur_f in bwd_visited:
                return steps, merge_paths(fwd_parent, bwd_parent, cur_f)
            for nbr, _ in get_neighbors(grid, cur_f):
                if nbr not in fwd_visited:
                    fwd_queue.append(nbr)
                    fwd_visited.add(nbr)
                    fwd_parent[nbr] = cur_f

        if bwd_queue:
            cur_b = bwd_queue.popleft()
            add_dynamic_obstacle(grid)
            steps.append(make_step(cur_b, list(fwd_queue) + list(bwd_queue), fwd_visited | bwd_visited))
            if cur_b in fwd_visited:
                return steps, merge_paths(fwd_parent, bwd_parent, cur_b)
            for nbr, _ in get_neighbors(grid, cur_b):
                if nbr not in bwd_visited:
                    bwd_queue.append(nbr)
                    bwd_visited.add(nbr)
                    bwd_parent[nbr] = cur_b

    return steps, []


def draw_cell(ax, r, c, facecolor, label='', label_color='white', fontsize=11):
    ax.add_patch(patches.Rectangle(
        (c - 0.45, r - 0.45), 0.9, 0.9,
        facecolor=facecolor, edgecolor=facecolor, linewidth=0, zorder=2))
    if label:
        ax.text(c, r, label, ha='center', va='center',
                fontsize=fontsize, fontweight='bold', color=label_color, zorder=3)


def draw_legend(ax):
    ax.clear()
    ax.set_facecolor('#1A1A1A')
    ax.axis('off')
    ax.text(0.5, 0.97, 'LEGEND', ha='center', va='top',
            fontsize=12, fontweight='bold', color='white',
            transform=ax.transAxes)
    items = [
        (COLORS['start'],    'S', 'Start node'),
        (COLORS['goal'],     'T', 'Target / Goal'),
        (COLORS['dynamic'],  'D', 'Dynamic obstacle'),
        (COLORS['frontier'], 'F', 'Frontier (queue)'),
        (COLORS['visited'],  '·', 'Explored node'),
        (COLORS['path'],     '1', 'Final path'),
    ]
    y = 0.82
    for color, sym, desc in items:
        ax.add_patch(patches.Rectangle(
            (0.04, y - 0.035), 0.12, 0.07,
            facecolor=color, transform=ax.transAxes, clip_on=False, zorder=3))
        ax.text(0.07, y, sym, ha='center', va='center',
                fontsize=8, fontweight='bold', color='white', transform=ax.transAxes)
        ax.text(0.22, y, desc, ha='left', va='center',
                fontsize=9, color='#CCCCCC', transform=ax.transAxes)
        y -= 0.11
    ax.text(0.5, 0.06, 'Move order: ↑ → ↓ ↘ ← ↖ ↗ ↙',
            ha='center', va='center', fontsize=8, color='#AAAAAA',
            transform=ax.transAxes,
            bbox=dict(facecolor='#2D2D2D', edgecolor='#555', pad=3))


def draw_stats(ax, algo_name, frame, steps, path, visited, frontier):
    ax.clear()
    ax.set_facecolor('#1A1A1A')
    ax.axis('off')
    ax.text(0.5, 0.97, 'STATISTICS', ha='center', va='top',
            fontsize=12, fontweight='bold', color='white',
            transform=ax.transAxes)

    search_done = frame >= len(steps)
    path_status = ('YES  ✔' if (search_done and path) else
                   'NO  ✖' if (search_done and not path) else 'Searching…')

    rows = [
        ('Algorithm:',      algo_name),
        ('Step:',           f"{min(frame+1, len(steps))} / {len(steps)}"),
        ('Nodes explored:', str(len(visited))),
        ('Frontier size:',  str(len(frontier))),
        ('Path found:',     path_status),
        ('Path length:',    str(len(path)) if (search_done and path) else '—'),
    ]
    y = 0.84
    for label, val in rows:
        ax.text(0.04, y, label, ha='left', va='center',
                fontsize=9, fontweight='bold', color='#BBBBBB',
                transform=ax.transAxes)
        val_color = ('#69F0AE' if 'YES' in val else
                     '#FF5252' if 'NO' in val else '#82B1FF')
        ax.text(0.98, y, val, ha='right', va='center',
                fontsize=9, fontweight='bold', color=val_color,
                transform=ax.transAxes)
        y -= 0.115


def visualize(grid, algo_name, steps, path):
    fig = plt.figure(figsize=(15, 9))
    fig.patch.set_facecolor('#212121')
    fig.canvas.manager.set_window_title('AI Pathfinder – Blind Search Visualizer')

    ax_main   = plt.subplot2grid((10, 13), (0, 0), colspan=8, rowspan=10)
    ax_legend = plt.subplot2grid((10, 13), (0, 9), colspan=4, rowspan=5)
    ax_stats  = plt.subplot2grid((10, 13), (5, 9), colspan=4, rowspan=5)

    def update(frame):
        ax_main.clear()
        ax_main.set_xlim(-0.5, grid['cols'] - 0.5)
        ax_main.set_ylim(-0.5, grid['rows'] - 0.5)
        ax_main.set_aspect('equal')
        ax_main.invert_yaxis()
        ax_main.set_facecolor('#2D2D2D')
        ax_main.set_xticks([])
        ax_main.set_yticks([])

        search_done = frame >= len(steps)
        suffix = ('  ✔ DONE' if (search_done and path) else
                  '  ✖ NO PATH' if (search_done and not path) else '  searching…')
        ax_main.set_title(
            f'{algo_name}{suffix}',
            fontsize=18, fontweight='bold', pad=10, color='white',
            bbox=dict(facecolor='#1A1A1A', edgecolor='none', pad=5))

        if frame < len(steps):
            st = steps[frame]
            current   = st['current']
            frontier  = set(st['frontier'])
            visited   = st['visited']
            curr_path = []
            is_replan = st.get('replan', False)
        else:
            current   = None
            frontier  = set()
            visited   = steps[-1]['visited'] if steps else set()
            curr_path = path or []
            is_replan = False

        for r in range(grid['rows']):
            for c in range(grid['cols']):
                pos = (r, c)
                border_color = COLORS['replan'] if is_replan else COLORS['grid']
                ax_main.add_patch(patches.Rectangle(
                    (c - 0.5, r - 0.5), 1, 1,
                    facecolor=COLORS['bg'], edgecolor=border_color,
                    linewidth=0.8, zorder=1))

                if pos in grid['dynamic_obstacles']:
                    draw_cell(ax_main, r, c, COLORS['dynamic'], 'D', fontsize=10)
                elif pos == grid['start']:
                    draw_cell(ax_main, r, c, COLORS['start'], 'S', fontsize=13)
                elif pos == grid['goal']:
                    draw_cell(ax_main, r, c, COLORS['goal'], 'T', fontsize=13)
                elif pos in curr_path:
                    idx = curr_path.index(pos)
                    label = str(idx) if 0 < idx < len(curr_path) - 1 else ''
                    draw_cell(ax_main, r, c, COLORS['path'], label,
                              label_color='#212121', fontsize=9)
                elif pos in frontier:
                    draw_cell(ax_main, r, c, COLORS['frontier'], 'F',
                              label_color='#212121', fontsize=9)
                elif pos in visited:
                    draw_cell(ax_main, r, c, COLORS['visited'], '·',
                              label_color='#424242', fontsize=14)

                if pos == current:
                    ax_main.add_patch(patches.FancyBboxPatch(
                        (c - 0.44, r - 0.44), 0.88, 0.88,
                        boxstyle='round,pad=0.02', facecolor='none',
                        edgecolor=COLORS['current'], linewidth=3, zorder=4))

        draw_legend(ax_legend)
        draw_stats(ax_stats, algo_name, frame, steps, path, visited, frontier)

        if is_replan:
            ax_stats.text(0.5, 0.06, '⚠ RE-PLANNING!', ha='center', va='center',
                          fontsize=11, fontweight='bold', color='#FF1744',
                          transform=ax_stats.transAxes,
                          bbox=dict(facecolor='#2D2D2D', edgecolor='#FF1744',
                                    linewidth=2, pad=4))

    anim = FuncAnimation(fig, update, frames=len(steps) + 40,
                         interval=180, repeat=False)
    plt.tight_layout(pad=1.5)
    plt.show()


def run_bfs():
    grid = build_grid()
    steps, path = with_replan(bfs, grid)
    return grid, steps, path


def run_dfs():
    grid = build_grid()
    steps, path = with_replan(dfs, grid)
    return grid, steps, path


def run_ucs():
    grid = build_grid()
    steps, path = with_replan(ucs, grid)
    return grid, steps, path


def run_dls():
    grid = build_grid()
    steps, path = with_replan(dls, grid, 15)
    return grid, steps, path


def run_iddfs():
    grid = build_grid()
    steps, path = iddfs(grid)
    return grid, steps, path


def run_bidirectional():
    grid = build_grid()
    steps, path = with_replan(bidirectional, grid)
    return grid, steps, path


ALGO_MAP = {
    '1': ('BFS',           'Breadth-First Search',        run_bfs),
    '2': ('DFS',           'Depth-First Search',          run_dfs),
    '3': ('UCS',           'Uniform Cost Search',         run_ucs),
    '4': ('DLS',           'Depth-Limited Search (L=15)', run_dls),
    '5': ('IDDFS',         'Iterative Deepening DFS',     run_iddfs),
    '6': ('Bidirectional', 'Bidirectional Search',        run_bidirectional),
}


def main():
    print('\n' + '='*62)
    print(' '*18 + 'AI  PATHFINDER')
    print(' '*12 + 'Uninformed / Blind Search ')
    print('='*62)

    while True:
        print('\n' + '-'*62)
        print('  SELECT ALGORITHM:')
        print('-'*62)
        for k, (short, long_, _) in ALGO_MAP.items():
            print(f'  {k}.  {short:14s}  -  {long_}')
        print('-'*62)

        choice = input('\n  Enter choice (1-6, or q to quit): ').strip().lower()

        if choice == 'q':
            print('\n  Goodbye!\n')
            break

        if choice not in ALGO_MAP:
            print('  Invalid choice. Please enter 1-6.')
            continue

        short_name, long_name, run_fn = ALGO_MAP[choice]
        print(f'\n  Running  {long_name} ...')

        grid, steps, path = run_fn()

        nodes_visited = len(steps[-1]['visited']) if steps else 0
        replans       = sum(1 for s in steps if s.get('replan'))

        print('='*62)
        if path:
            print(f'  PATH FOUND!   Length: {len(path)} steps')
            print(f'  Nodes explored  : {nodes_visited}')
            print(f'  Dynamic walls   : {len(grid["dynamic_obstacles"])}')
            print(f'  Re-plans done   : {replans}')
            print(f'\n  Route:')
            for i, cell in enumerate(path):
                tag = ' (Start)' if i == 0 else (' (Goal)' if i == len(path)-1 else '')
                print(f'    {i:3d}.  {cell}{tag}')
        else:
            print('  NO PATH FOUND')
            print(f'  Nodes explored  : {nodes_visited}')
            print(f'  Dynamic walls   : {len(grid["dynamic_obstacles"])}')
        print('='*62)

        print('\n  Opening animated visualization ...\n')
        visualize(grid, short_name, steps, path)

        again = input('\n  Run another algorithm? (y / n): ').strip().lower()
        if again not in ('y', 'yes'):
            print('\n  Goodbye!\n')
            break


if __name__ == '__main__':
    main()

import pandas as pd
import matplotlib.pyplot as plt

# 상수 정의
FIGURE_SIZE = (10, 8)
GRID_OFFSET = 0.5
MARKER_SIZE = 0.2
PATH_CONFIG = {
    'color': 'red',
    'linewidth': 2,
    'marker': 'o',
    'markersize': 5,
    'label': 'shortest path'
}

MARKER_CONFIGS = {
    'construction': {
        'size': 0.4,
        'facecolor': 'gray',
        'edgecolor': 'black',
        'alpha': 0.7
    },
    'building': {
        'color': 'brown',
        'markersize': 8,
        'marker': 'o'
    },
    'coffee': {
        'size': 0.4,
        'facecolor': 'green',
        'edgecolor': 'black'
    },
    'home': {
        'facecolor': 'green',
        'edgecolor': 'black'
    }
}
MOVEMENT_DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 상하좌우
OUTPUT_FILES = {
    'map': 'map_final.png',
    'path': 'dataFile/home_to_cafe.csv'
}


class Queue:
    def __init__(self):
        self.in_stack = []
        self.out_stack = []

    def append(self, item):  # enqueue
        self.in_stack.append(item)

    def popleft(self):       # dequeue
        if not self.out_stack:
            while self.in_stack:
                self.out_stack.append(self.in_stack.pop())
        if self.out_stack:
            return self.out_stack.pop()
        raise IndexError("Queue is empty")

    def __bool__(self):      # bool(queue) or `while queue:`가 가능하게
        return bool(self.in_stack or self.out_stack)


def bfs(start, goals, coords, walls):
    """최단 경로를 찾는 BFS 함수"""
    queue = Queue()
    queue.append((start, [start]))
    visited = set()
    visited.add(start)

    while queue:
        current, path = queue.popleft()
        if current in goals:
            return path, current
        for dx, dy in MOVEMENT_DIRECTIONS:
            nx, ny = current[0] + dx, current[1] + dy
            next_pos = (nx, ny)
            if (next_pos in coords and 
                next_pos not in walls and
                next_pos not in visited):
                visited.add(next_pos)
                queue.append((next_pos, path + [next_pos]))
    return None, None


def setup_grid_and_limits(ax, min_x, max_x, min_y, max_y):
    """그리드와 축 범위를 설정하는 함수"""
    # 그리드 설정
    ax.set_xlim(min_x - GRID_OFFSET, max_x + GRID_OFFSET)
    ax.set_ylim(max_y + GRID_OFFSET, min_y - GRID_OFFSET)  # y축 반전

    # 그리드 라인 그리기
    for x in range(min_x, max_x + 1):
        ax.axvline(x, color='lightgray', linewidth=0.5)
    for y in range(min_y, max_y + 1):
        ax.axhline(y, color='lightgray', linewidth=0.5)


def draw_construction_site(ax, x, y):
    """건설 현장을 그리는 함수"""
    config = MARKER_CONFIGS['construction']
    rect = plt.Rectangle((x - MARKER_SIZE, y - MARKER_SIZE), config['size'],
                        config['size'], facecolor=config['facecolor'],
                        edgecolor=config['edgecolor'], alpha=config['alpha'])
    ax.add_patch(rect)


def draw_building(ax, x, y):
    """건물(아파트/빌딩)을 그리는 함수"""
    config = MARKER_CONFIGS['building']
    ax.plot(x, y, config['marker'], color=config['color'],
            markersize=config['markersize'])


def draw_coffee_shop(ax, x, y):
    """커피숍을 그리는 함수"""
    config = MARKER_CONFIGS['coffee']
    rect = plt.Rectangle((x - MARKER_SIZE, y - MARKER_SIZE), config['size'],
                        config['size'], facecolor=config['facecolor'],
                        edgecolor=config['edgecolor'])
    ax.add_patch(rect)


def draw_home(ax, x, y):
    """집을 그리는 함수"""
    config = MARKER_CONFIGS['home']
    triangle_points = [[x, y - MARKER_SIZE], [x - MARKER_SIZE, y + MARKER_SIZE],
                      [x + MARKER_SIZE, y + MARKER_SIZE]]
    triangle = plt.Polygon(triangle_points, facecolor=config['facecolor'],
                          edgecolor=config['edgecolor'])
    ax.add_patch(triangle)


def draw_markers(ax, data):
    """모든 마커를 그리는 함수"""
    for _, row in data.iterrows():
        x, y = row['x'], row['y']
        
        # 건설 현장이 있는 경우 회색 사각형 (우선순위 높음)
        if row['ConstructionSite'] == 1:
            draw_construction_site(ax, x, y)
        # 구조물 표시
        elif row['category'] in ['Apartment', 'Building']:
            draw_building(ax, x, y)
        elif row['category'] == 'BandalgomCoffee':
            draw_coffee_shop(ax, x, y)
        elif row['category'] == 'MyHome':
            draw_home(ax, x, y)


def draw_path(ax, path):
    """경로를 그리고 저장하는 함수"""
    px, py = zip(*path)
    ax.plot(px, py, color=PATH_CONFIG['color'], 
            linewidth=PATH_CONFIG['linewidth'],
            marker=PATH_CONFIG['marker'], 
            markersize=PATH_CONFIG['markersize'],
            label=PATH_CONFIG['label'])

    # 경로를 CSV 파일로 저장
    path_df = pd.DataFrame(path, columns=['x', 'y'])
    path_df.to_csv(OUTPUT_FILES['path'], index=False)


def setup_plot_appearance(ax, min_x, max_x, min_y, max_y):
    """플롯의 외관을 설정하는 함수"""
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('BandalgomCoffee Map')
    
    # 격자 표시
    ax.grid(True, alpha=0.3)
    ax.set_xticks(range(min_x, max_x + 1))
    ax.set_yticks(range(min_y, max_y + 1))


def draw_map(data, path):
    """지도를 시각화하는 함수"""
    fig, ax = plt.subplots(figsize=FIGURE_SIZE)
    
    # 지도 크기 설정
    min_x, max_x = data['x'].min(), data['x'].max()
    min_y, max_y = data['y'].min(), data['y'].max()

    # 그리드 설정
    setup_grid_and_limits(ax, min_x, max_x, min_y, max_y)
    
    # 마커들 그리기
    draw_markers(ax, data)

    # 경로 그리기 및 저장
    draw_path(ax, path)
        
    # 플롯 외관 설정
    setup_plot_appearance(ax, min_x, max_x, min_y, max_y)

    return fig


def save_map_image(fig):
    """지도 이미지를 저장하는 함수"""
    fig.tight_layout()
    fig.savefig(OUTPUT_FILES['map'], dpi=300, bbox_inches='tight')
    print("저장 완료")
    plt.close(fig)


def get_start_and_cafe_positions(data):
    """시작점과 카페 위치를 찾는 함수"""
    # 시작점(MyHome) 찾기
    start_row = data[data['category'] == 'MyHome'].iloc[0]
    start = (start_row['x'], start_row['y'])

    # 카페 위치들 찾기
    cafe_rows = data[data['category'] == 'BandalgomCoffee'][['x', 'y']]
    cafe_list = [tuple(row) for row in cafe_rows.values]

    return start, cafe_list


def prepare_pathfinding_data(data):
    """경로 탐색을 위한 데이터를 준비하는 함수"""
    # 좌표 집합 및 장애물 집합 생성
    coords = set(zip(data['x'], data['y']))
    construction_data = data[data['ConstructionSite'] == 1]
    walls = set(zip(construction_data['x'], construction_data['y']))
    
    return coords, walls


def main():
    # 데이터 로드 및 전처리
    data = pd.read_csv('dataFile/merged_output.csv')

    # 경로 탐색 데이터 준비
    coords, walls = prepare_pathfinding_data(data)
    
    # 시작점과 목표점 찾기
    start, cafe_list = get_start_and_cafe_positions(data)

    # 최단 경로 탐색 (여러 카페 중 가장 가까운 곳)
    path, goal = bfs(start, set(cafe_list), coords, walls)
    if path is None:
        raise Exception("최단 경로를 찾을 수 없습니다.")
    
    # 지도 그리기 및 저장
    fig = draw_map(data, path)
    save_map_image(fig)


if __name__ == "__main__":
    main()

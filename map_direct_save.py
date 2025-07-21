import pandas as pd
import matplotlib.pyplot as plt

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
    moves = [(-1,0),(1,0),(0,-1),(0,1)]  # 상하좌우

    while queue:
        current, path = queue.popleft()
        if current in goals:
            return path, current
        for dx, dy in moves:
            nx, ny = current[0]+dx, current[1]+dy
            next_pos = (nx, ny)
            if next_pos in coords and next_pos not in walls and next_pos not in visited:
                visited.add(next_pos)
                queue.append((next_pos, path + [next_pos]))
    return None, None


def draw_map(data, path) :
    """지도를 시각화하는 함수 (Edit to 단계2)"""
    fig, ax = plt.subplots(figsize=(10, 8))
    # 지도 크기 설정
    min_x, max_x = data['x'].min(), data['x'].max()
    min_y, max_y = data['y'].min(), data['y'].max()

    # 그리드 설정
    ax.set_xlim(min_x - 0.5, max_x + 0.5)
    ax.set_ylim(max_y + 0.5, min_y - 0.5)  # y축 반전

     # 그리드 라인 그리기
    for x in range(min_x, max_x + 1):
        ax.axvline(x, color='lightgray', linewidth=0.5)
    for y in range(min_y, max_y + 1):
        ax.axhline(y, color='lightgray', linewidth=0.5)

    # 각 점에 대해 시각화
    for _, row in data.iterrows():
        x, y = row['x'], row['y']
        
        # 건설 현장이 있는 경우 회색 사각형 (우선순위 높음)
        if row['ConstructionSite'] == 1:
            ax.add_patch(plt.Rectangle((x-0.2, y-0.2), 0.4, 0.4, 
                                     facecolor='gray', edgecolor='black', alpha=0.7))
        
        # 구조물 표시
        elif row['category'] == 'Apartment':
            ax.plot(x, y, 'o', color='brown', markersize=8)
        elif row['category'] == 'Building':
            ax.plot(x, y, 'o', color='brown', markersize=8)
        elif row['category'] == 'BandalgomCoffee':
            ax.add_patch(plt.Rectangle((x-0.2, y-0.2), 0.4, 0.4, 
                                     facecolor='green', edgecolor='black'))
        elif row['category'] == 'MyHome':
            # 삼각형 그리기
            triangle = plt.Polygon([[x, y-0.2], [x-0.2, y+0.2], [x+0.2, y+0.2]], 
                                  facecolor='green', edgecolor='black')
            ax.add_patch(triangle)

    # 경로 그리기 및 저장 (빨간 선)
    px, py = zip(*path)
    ax.plot(px, py, color='red', linewidth=2, marker='o', markersize=5, label='shortest path')

    path_df = pd.DataFrame(path, columns=['x', 'y'])
    path_df.to_csv('dataFile/home_to_cafe.csv', index=False)
        
    # 축 설정
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('BandalgomCoffee Map')
    
    # 격자 표시
    ax.grid(True, alpha=0.3)
    ax.set_xticks(range(min_x, max_x + 1))
    ax.set_yticks(range(min_y, max_y + 1))

    return fig


def save_map_image(fig) :
    """지도 이미지를 저장하는 함수"""
    fig.tight_layout()
    fig.savefig('map_final.png', dpi=300, bbox_inches='tight')
    print("저장 완료")
    plt.close(fig)


def main() :
    # 데이터 로드 및 전처리
    data = pd.read_csv('dataFile/merged_output.csv')

    # 좌표 집합 및 장애물 집합 생성
    coords = set(zip(data['x'], data['y']))
    walls = set(zip(data[data['ConstructionSite'] == 1]['x'], data[data['ConstructionSite'] == 1]['y']))

    # 시작점(MyHome)과 도착점(BandalgomCoffee) 찾기
    start_row = data[data['category'] == 'MyHome'].iloc[0]
    start = (start_row['x'], start_row['y'])

    cafe_rows = data[data['category'] == 'BandalgomCoffee'][['x', 'y']]
    cafe_list = [tuple(row) for row in cafe_rows.values]


    # 최단 경로 탐색 (여러 카페 중 가장 가까운 곳)
    path, goal = bfs(start, set(cafe_list), coords, walls)
    if path is None:
        raise Exception("최단 경로를 찾을 수 없습니다.")
    
    # 지도 그리기 및 저장
    fig = draw_map(data, path)
    save_map_image(fig)


if __name__ == "__main__" :
    main()

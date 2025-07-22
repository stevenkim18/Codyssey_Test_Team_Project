import pandas as pd
import matplotlib.pyplot as plt

# 상수 정의
FIGURE_SIZE = (10, 8)
GRID_OFFSET = 0.5
MARKER_SIZE = 0.2
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


def setup_plot_appearance(ax, min_x, max_x, min_y, max_y):
    """플롯의 외관을 설정하는 함수"""
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('BandalgomCoffee Map')
    
    # 격자 표시
    ax.grid(True, alpha=0.3)
    ax.set_xticks(range(min_x, max_x + 1))
    ax.set_yticks(range(min_y, max_y + 1))


def draw_map(data):
    """지도를 시각화하는 함수"""
    # 지도 크기 설정
    min_x, max_x = data['x'].min(), data['x'].max()
    min_y, max_y = data['y'].min(), data['y'].max()

    fig, ax = plt.subplots(figsize=FIGURE_SIZE)

    # 그리드 설정
    setup_grid_and_limits(ax, min_x, max_x, min_y, max_y)
    
    # 모든 마커 그리기
    draw_markers(ax, data)
    
    # 플롯 외관 설정
    setup_plot_appearance(ax, min_x, max_x, min_y, max_y)
    
    # 이미지 저장
    plt.tight_layout()
    plt.savefig('map.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return fig


def main():
    """메인 함수"""
    # 데이터 로드
    data = pd.read_csv('dataFile/merged_output.csv')
    
    # 지도 그리기
    draw_map(data)


if __name__ == '__main__':
    main()
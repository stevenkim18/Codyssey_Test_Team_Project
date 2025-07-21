import pandas as pd
import matplotlib.pyplot as plt

def draw_map(data) :
    """지도를 시각화하는 함수"""
    # 지도 크기 설정
    min_x, max_x = data['x'].min(), data['x'].max()
    min_y, max_y = data['y'].min(), data['y'].max()

    fig, ax = plt.subplots(figsize=(10, 8))

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

    
    # 축 설정
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('BandalgomCoffee Map')
    
    # 격자 표시
    ax.grid(True, alpha=0.3)
    ax.set_xticks(range(min_x, max_x + 1))
    ax.set_yticks(range(min_y, max_y + 1))
    
    # 이미지 저장
    plt.tight_layout()
    plt.savefig('map.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return fig

def main():
    """메인 함수"""
    # 데이터 로드
    data = pd.read_csv('dataFile/merged_output.csv')
    
    print("=== 지도 시각화 데이터 요약 ===")
    print(f"총 데이터 수: {len(data)}")
    print(f"X 범위: {data['x'].min()} ~ {data['x'].max()}")
    print(f"Y 범위: {data['y'].min()} ~ {data['y'].max()}")
    
    # 구조물별 통계
    struct_counts = data['category'].value_counts()
    print("\n=== 구조물별 통계 ===")
    for category, count in struct_counts.items():
        print(f"{category}: {count}개")
    
    # 건설 현장 통계
    construction_counts = data['ConstructionSite'].value_counts()
    print("\n=== 건설 현장 통계 ===")
    print(f"건설 현장 없음 (0): {construction_counts.get(0, 0)}개")
    print(f"건설 현장 있음 (1): {construction_counts.get(1, 0)}개")
    
    # 중요 위치 출력
    my_home = data[data['category'] == 'MyHome']
    coffee_shops = data[data['category'] == 'BandalgomCoffee']
    
    print("\n=== 중요 위치 정보 ===")
    if not my_home.empty:
        print(f"내 집 위치: ({my_home.iloc[0]['x']}, {my_home.iloc[0]['y']})")
    
    print("반달곰 커피 위치:")
    for _, coffee in coffee_shops.iterrows():
        print(f"  - ({coffee['x']}, {coffee['y']})")
    
    # 지도 그리기
    draw_map(data)

if __name__ == '__main__':
    main()
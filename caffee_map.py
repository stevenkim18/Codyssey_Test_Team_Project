import pandas as pd

def setPandasDisplayOptions():
    """Pandas의 출력 옵션을 설정하는 함수"""
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)

# 보너스 함수
def get_csv_data(filename):
    """CSV 파일에서 데이터를 읽어오는 함수"""
    try:
        data = pd.read_csv(filename)
        print(f"데이터 로드 성공: {filename}")
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {filename}")

# 통계를 보여주는 함수 (보너스)
def show_stats(data):
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

def main():
    setPandasDisplayOptions()
    
    # 1. csv 데이터 읽고 출력
    try:
        area_category = get_csv_data('./dataFile/area_category.csv')
        area_map = get_csv_data('./dataFile/area_map.csv')
        area_struct = get_csv_data('./dataFile/area_struc.csv')
    except FileNotFoundError as e:
        print(e)
        return

    print(area_category)
    print()
    print(area_map)
    print()
    print(area_struct)
    
    # 2. area_category 기준으로 area_struct의 category를 매핑
    area_struct['category'] = area_struct['category'].map(
        dict(zip(area_category['category'], area_category['struct']))
    ).fillna('None') # 0인 경우 None으로 대체
    
    print(area_struct)
    
    # 3. 병합
    merged_df = pd.merge(area_struct, area_map, on=['x', 'y'], how='left')
    print(merged_df)
    
    # area로 정렬 (x, y로 추가 정렬)
    sorted_merged_df = merged_df.sort_values(by=['area', 'x', 'y'], ascending=[True, True, True])
    print(sorted_merged_df)
    
    sorted_merged_df.to_csv('./dataFile/merged_output.csv', index=False)
    
    # 4. area가 1인 곳 필터링
    area1_df = sorted_merged_df[sorted_merged_df['area'] == 1]
    print(area1_df)
    
    # 5. 통계 출력
    show_stats(sorted_merged_df)

if __name__ == "__main__":
    main()

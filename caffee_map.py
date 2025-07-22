import pandas as pd

# 상수 정의
CATEGORY_MAPPINGS = {
    'construction_none': 0,
    'construction_exists': 1
}

DATA_FILES = {
    'category': './dataFile/area_category.csv',
    'map': './dataFile/area_map.csv', 
    'struct': './dataFile/area_struct.csv',
    'output': './dataFile/merged_output.csv'
}


def set_pandas_display_options():
    """Pandas의 출력 옵션을 설정하는 함수"""
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)


def get_csv_data(filename):
    """CSV 파일에서 데이터를 읽어오는 함수"""
    try:
        data = pd.read_csv(filename)
        print(f"데이터 로드 성공: {filename}")
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {filename}")


def print_location_info(my_home, coffee_shops):
    """위치 정보를 출력하는 함수"""
    print("\n=== 중요 위치 정보 ===")
    if not my_home.empty:
        home_x = my_home.iloc[0]['x']
        home_y = my_home.iloc[0]['y']
        print(f"내 집 위치: ({home_x}, {home_y})")
    
    print("반달곰 커피 위치:")
    for _, coffee in coffee_shops.iterrows():
        print(f"  - ({coffee['x']}, {coffee['y']})")


def show_stats(data):
    """통계를 보여주는 함수"""
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
    none_count = construction_counts.get(CATEGORY_MAPPINGS['construction_none'], 0)
    exists_count = construction_counts.get(CATEGORY_MAPPINGS['construction_exists'], 0)
    print(f"건설 현장 없음 (0): {none_count}개")
    print(f"건설 현장 있음 (1): {exists_count}개")
    
    # 중요 위치 출력
    my_home = data[data['category'] == 'MyHome']
    coffee_shops = data[data['category'] == 'BandalgomCoffee']
    
    print_location_info(my_home, coffee_shops)


def load_and_process_data():
    """데이터를 로드하고 전처리하는 함수"""
    try:
        area_category = get_csv_data(DATA_FILES['category'])
        area_map = get_csv_data(DATA_FILES['map'])
        area_struct = get_csv_data(DATA_FILES['struct'])
    except FileNotFoundError as e:
        print(e)
        return None, None, None
    
    return area_category, area_map, area_struct


def convert_struct_ids_to_names(area_category, area_struct):
    """구조물 ID를 area_category 기준으로 이름으로 변환하는 함수"""
    print("\n=== 2번 작업: 구조물 ID 매핑 ===")

    # area_category 기준으로 area_struct의 category를 매핑
    category_mapping = dict(zip(area_category['category'],
                               area_category['struct']))
    
    print("구조물 ID 매핑 정보:")
    for struct_id, struct_name in category_mapping.items():
        print(f"  ID {struct_id} -> {struct_name}")
    
    # ID를 이름으로 변환
    area_struct_converted = area_struct.copy()
    area_struct_converted['category'] = area_struct_converted['category'].map(
        category_mapping).fillna('None')  # 0인 경우 None으로 대체
    
    print("\n변환 후 area_struct:")
    print(area_struct_converted)
    
    return area_struct_converted


def merge_and_sort_dataframes(area_struct_converted, area_map):
    """세 데이터를 하나의 DataFrame으로 병합하고 area 기준으로 정렬하는 함수"""
    print("\n=== 3번 작업: 데이터 병합 및 정렬 ===")
    
    # 병합
    merged_df = pd.merge(area_struct_converted, area_map, on=['x', 'y'], how='left')
    
    print("병합된 데이터:")
    print(merged_df)
    
    # area로 정렬 (x, y로 추가 정렬)
    print("\narea 기준으로 정렬 중 (x, y 추가 정렬)...")
    sorted_merged_df = merged_df.sort_values(
        by=['area', 'x', 'y'], ascending=[True, True, True]
    )
    
    print("정렬된 최종 데이터:")
    print(sorted_merged_df)
    
    return sorted_merged_df


def main():
    set_pandas_display_options()
    
    # 1. csv 데이터 읽고 출력
    print("=== 1번 작업: CSV 파일 로드 및 출력 ===")
    area_category, area_map, area_struct = load_and_process_data()
    if area_category is None:
        return

    print("area_category.csv:")
    print(area_category)
    print()
    
    print("area_map.csv:")
    print(area_map)
    print()
    
    print("area_struct.csv:")
    print(area_struct)
    print()
    
    # 2. 구조물 ID를 이름으로 변환
    area_struct_converted = convert_struct_ids_to_names(area_category, area_struct)
    
    # 3. 데이터 병합 및 정렬
    sorted_merged_df = merge_and_sort_dataframes(area_struct_converted, area_map)
    
    # 결과 저장
    print(f"\n결과를 {DATA_FILES['output']}에 저장합니다...")
    sorted_merged_df.to_csv(DATA_FILES['output'], index=False)
    print("저장 완료!")
    
    # 4. area가 1인 곳 필터링
    print("\n=== 4번 작업: area 1 데이터 필터링 ===")
    area1_df = sorted_merged_df[sorted_merged_df['area'] == 1]
    print("area가 1인 데이터:")
    print(area1_df)
    
    # 5. 통계 출력 (보너스)
    print("\n=== 6번 작업 (보너스): 통계 리포트 ===")
    show_stats(sorted_merged_df)


if __name__ == "__main__":
    main()

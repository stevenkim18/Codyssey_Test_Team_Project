import pandas as pd

def get_data_from_csv():
    # 전체 출력을 위한 설정
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    
    area_category = pd.read_csv('./dataFile/area_category.csv')
    area_map = pd.read_csv('./dataFile/area_map.csv')
    area_struct = pd.read_csv('./dataFile/area_struct.csv')

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
    
    # 4. area가 1인 곳 필터링
    area1_df = sorted_merged_df[sorted_merged_df['area'] == 1]
    print(area1_df)
    
def main():
    get_data_from_csv()

if __name__ == "__main__":
    main()

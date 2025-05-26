import csv
import random

def get_shuffled_names_from_csv(filename):
    """
    CSV 파일에서 명단을 읽어와 순서를 랜덤하게 섞어서 반환합니다.

    Args:
        filename (str): 읽어올 CSV 파일의 경로.

    Returns:
        list: 랜덤하게 섞인 이름들의 리스트.
              파일을 찾을 수 없거나 명단이 없으면 빈 리스트를 반환합니다.
    """
    names = []
    try:
        with open(filename, 'r', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                if row:  # 빈 줄이 아닐 경우에만 추가
                    names.append(row[0])  # 첫 번째 열의 값(이름)을 추가
    except FileNotFoundError:
        print(f"오류: '{filename}' 파일을 찾을 수 없습니다.")
        return []
    except Exception as e:
        print(f"파일을 읽는 중 오류가 발생했습니다: {e}")
        return []

    if not names:
        print("CSV 파일에 명단이 없습니다.")
        return []

    # 명단 리스트의 순서를 랜덤하게 섞습니다.
    random.shuffle(names)
    
    return names

if __name__ == "__main__":
    csv_file = 'ajo.csv'  # CSV 파일 경로

    print("1. A그룹")
    print("2. B그룹")
    c = input("입력: ")
    if c == "2":
        csv_file = 'bjo.csv'
    
    print(f"'{csv_file}' 파일에서 명단을 읽어 순서를 랜덤하게 정합니다...")
    shuffled_names = get_shuffled_names_from_csv(csv_file)

    if shuffled_names:
        print(f"\n--- 랜덤하게 정렬된 명단 ({len(shuffled_names)}명) ---")
        for i, name in enumerate(shuffled_names):
            print(f"{i+1}. {name}")
    else:
        print("랜덤하게 정렬할 명단이 없습니다.")
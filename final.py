import csv
import random

def select_and_separate_names(filename, num_to_select):
    """
    CSV 파일에서 명단을 읽어와 지정된 갯수만큼 랜덤으로 이름을 선택하고
    선택된 명단과 남은 명단을 분리하여 반환합니다.

    Args:
        filename (str): 읽어올 CSV 파일의 경로.
        num_to_select (int): 랜덤으로 선택할 이름의 갯수.

    Returns:
        tuple: (선택된 이름 리스트, 남은 이름 리스트).
               파일을 찾을 수 없거나 명단이 없으면 ([], [])를 반환합니다.
    """
    all_names = []
    try:
        with open(filename, 'r', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                if row:  # 빈 줄이 아닐 경우에만 추가
                    all_names.append(row[0])  # 첫 번째 열의 값(이름)을 추가
    except FileNotFoundError:
        print(f"오류: '{filename}' 파일을 찾을 수 없습니다.")
        return [], []
    except Exception as e:
        print(f"파일을 읽는 중 오류가 발생했습니다: {e}")
        return [], []

    if not all_names:
        print("CSV 파일에 명단이 없습니다.")
        return [], []

    if num_to_select >= len(all_names):
        print(f"요청한 갯수({num_to_select}개)가 전체 명단({len(all_names)}개)보다 많거나 같아서 전체 명단을 섞어서 선택 명단으로 반환합니다.")
        random.shuffle(all_names) # 전체 명단을 섞어서 선택 명단으로
        return all_names, [] # 남은 명단은 없음
    else:
        # random.sample()은 중복 없이 랜덤 선택
        selected_names = random.sample(all_names, num_to_select)
        
        # 남은 명단을 계산합니다.
        # 전체 명단에서 선택된 명단을 제외합니다.
        remaining_names = [name for name in all_names if name not in selected_names]
        
        return selected_names, remaining_names

if __name__ == "__main__":
    csv_file = '발표명단.csv'  # CSV 파일 경로
    
    while True:
        try:
            count = int(input("몇 명을 랜덤으로 선택하시겠습니까? (종료: 0 입력): "))
            if count == 0:
                print("프로그램을 종료합니다.")
                break
            elif count < 0:
                print("선택할 갯수는 양수여야 합니다. 다시 입력해주세요.")
                continue

            selected_names, remaining_names = select_and_separate_names(csv_file, count)

            if selected_names:
                print(f"\n--- B그룹 {len(selected_names)}명 ---")
                for i, name in enumerate(selected_names):
                    print(f"{name}")
            else:
                print("선택된 이름이 없습니다.")

            if remaining_names:
                print(f"\n--- 나머지는 A그룹 명단 {len(remaining_names)}명 ---")
                for i, name in enumerate(remaining_names):
                    print(f"{name}")
            elif not selected_names and not remaining_names: # 파일 없거나 명단 없는 경우
                pass # 이미 함수 내에서 출력했으므로 추가 출력 없음
            else: # 모든 명단이 선택된 경우
                print("\n남은 명단이 없습니다. (모든 명단이 선택되었습니다.)")

        except ValueError:
            print("올바른 숫자를 입력해주세요.")
        except Exception as e:
            print(f"예상치 못한 오류가 발생했습니다: {e}")
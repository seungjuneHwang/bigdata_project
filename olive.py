from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# --- Setup Chrome Options ---
chrome_options = Options()
# chrome_options.add_argument("--headless") # Uncomment this line to run Chrome in headless mode (no visible browser)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu") # Applicable to Windows/Linux
chrome_options.add_argument("--window-size=1920,1080") # Set a common window size

# --- Specify the path to your ChromeDriver ---
# IMPORTANT: Replace 'path/to/your/chromedriver' with the actual path to your ChromeDriver executable.
# You can download it from: https://googlechromelabs.github.io/chrome-for-testing/
# Example for Windows: service = Service("C:\\WebDriver\\chromedriver.exe")
# Example for macOS/Linux: service = Service("/usr/local/bin/chromedriver")

# Initialize the WebDriver
try:
    # Attempt to use the default service if chromedriver is in PATH
    # service = Service()
    service = Service('chromedriver.exe') # <-- 이 부분을 수정하세요.(맥사용자는 /usr/local/bin/chromedriver 등으로 수정)
    # Or, if chromedriver is not in your PATH, uncomment the line below and specify the path:
    # service = Service('path/to/your/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # The URL provided by the user
    # 아래 fltDispCatNo= 값을 해당하는 카테고리에 맞게 수정하세요.
    url = "https://www.oliveyoung.co.kr/store/main/getBestList.do?dispCatNo=900000100100001&fltDispCatNo=10000010009"
    driver.get(url)

    # 페이지가 완전히 로드될 때까지 기다립니다.
    # '.cate_prd_list li' 요소가 나타날 때까지 최대 10초 대기
    # 이제 class="flag" 유무와 상관없이 모든 li를 찾습니다.
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.cate_prd_list > li'))
    )
    time.sleep(1) # 추가적인 대기 (JS 렌더링에 필요한 경우)

    all_products_data = []

    # '.cate_prd_list' 클래스를 가진 ul 태그의 바로 아래 자식 li 요소를 모두 찾습니다.
    # 'li.flag' 대신 'li'만 사용하여 모든 li 요소를 선택합니다.
    product_elements = driver.find_elements(By.CSS_SELECTOR, '.cate_prd_list > li')

    if not product_elements:
        print("경고: '.cate_prd_list > li' 요소를 찾을 수 없습니다. HTML 구조 또는 선택자를 확인하세요.")

    # 각 제품 요소에 대해 반복하며 정보 추출
    for i, product_element in enumerate(product_elements):
        product_info = {}

        # 제품 URL 추출
        try:
            url_element = product_element.find_element(By.CSS_SELECTOR, '.prd_thumb')
            product_info['Product URL'] = url_element.get_attribute('href')
        except Exception:
            product_info['Product URL'] = None

        # 브랜드명 추출
        try:
            brand_element = product_element.find_element(By.CSS_SELECTOR, '.tx_brand')
            product_info['Brand'] = brand_element.text.strip()
        except Exception:
            product_info['Brand'] = None

        # 제품명 추출
        try:
            name_element = product_element.find_element(By.CSS_SELECTOR, '.tx_name')
            product_info['Product Name'] = name_element.text.strip()
        except Exception:
            product_info['Product Name'] = None

        # 원래 가격 추출
        try:
            # tx_org는 있을 수도 있고 없을 수도 있음
            original_price_element = product_element.find_element(By.CSS_SELECTOR, '.tx_org .tx_num')
            product_info['Original Price'] = original_price_element.text.strip() + '원'
        except Exception:
            product_info['Original Price'] = None # 없을 경우 None

        # 할인가 추출
        try:
            sale_price_element = product_element.find_element(By.CSS_SELECTOR, '.tx_cur .tx_num')
            product_info['Sale Price'] = sale_price_element.text.strip() + '원'
        except Exception:
            product_info['Sale Price'] = None # 없을 경우 None

        # 깃발/태그 (세일, 쿠폰, 오늘드림 등) 추출
        flags = []
        try:
            flag_elements = product_element.find_elements(By.CSS_SELECTOR, '.prd_flag .icon_flag')
            for flag_el in flag_elements:
                flags.append(flag_el.text.strip())
            product_info['Flags'] = flags
        except Exception:
            product_info['Flags'] = []

        # 평점 추출
        try:
            rating_element = product_element.find_element(By.CSS_SELECTOR, '.review_point .point')
            rating_text = rating_element.text.strip()
            # "10점만점에" 부분이 있으면 제거하고 숫자만 남깁니다.
            if '10점만점에' in rating_text:
                product_info['Rating'] = rating_text.replace('10점만점에 ', '')
            else:
                product_info['Rating'] = rating_text
        except Exception:
            product_info['Rating'] = None

        all_products_data.append(product_info)

    # 추출된 모든 제품 데이터 출력
    if all_products_data:
        print("--- 추출된 제품 정보 ---")
        for i, product in enumerate(all_products_data):
            print(f"제품 {i+1}:")
            for key, value in product.items():
                print(f"  {key}: {value}")
            print("-" * 30)
    else:
        print("추출된 제품 정보가 없습니다.")
    print(f"총 {len(product_elements)}개의 제품 정보를 추출했습니다.")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Always close the browser
    if 'driver' in locals() and driver:
        driver.quit()
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# === Load CSV Tasks ===
institution_col = '\ufeffSendInstitution'
course_col = 'SendCourse1CourseCode'
course_tasks = []

try:
    with open("C:/Users/RSENTHIL/Desktop/python/readmit/pemain.csv", newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            institution = row[institution_col].strip()
            course_code = row[course_col].strip()
            if institution and course_code:
                course_tasks.append((institution, course_code))
    print(f"\u2705 Loaded {len(course_tasks)} course tasks from CSV.")
except Exception as e:
    print(f"\u274C Error loading CSV: {e}")

# === Setup ===
options = Options()
options.add_argument("--start-maximized")
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(browser, 30)

# === Setup TXT logging for failures ===
failure_log_path = "C:/Users/RSENTHIL/Desktop/python/readmit/failure_log.txt"
with open(failure_log_path, mode='w') as log_file:
    log_file.write("Failed Institution-CourseCode Pairs:\n")

def log_failure(institution, course_code, error):
    with open(failure_log_path, mode='a') as log_file:
        log_file.write(f"{institution} - {course_code}\n")


def type_course_code(code):
    for _ in range(3):
        try:
            course_input = wait.until(
                EC.element_to_be_clickable((By.ID, "ContentPlaceHolder1_tbxCourseCode"))
            )
            browser.execute_script("arguments[0].scrollIntoView(true);", course_input)
            time.sleep(0.5)
            course_input.clear()
            course_input.send_keys(code)
            return
        except Exception as e:
            print(f"\u26a0\ufe0f Retrying course input due to: {e}")
            time.sleep(1)
    raise Exception("\u274c Failed to type course code after 3 attempts")


def select_department():
    for _ in range(3):
        try:
            dropdown = wait.until(
                EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_ddlEditReceiveCourseDepartment"))
            )
            Select(dropdown).select_by_value("7023968")
            return
        except Exception as e:
            print(f"\u26a0\ufe0f Retrying department selection: {e}")
            time.sleep(1)
    raise Exception("\u274c Failed to select department")

def select_departmentyear():
    for _ in range(3):
        try:
            dropdown = wait.until(
                EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_ddlEditReceiveCourseDataSet"))
            )
            Select(dropdown).select_by_value("386678")
            return
        except Exception as e:
            print(f"\u26a0\ufe0f Retrying department selection: {e}")
            time.sleep(1)
    raise Exception("\u274c Failed to select department")

def safe_logout():
    try:
        logout_btn = browser.find_element(By.ID, "btnLogOut")
        browser.execute_script("arguments[0].scrollIntoView(true);", logout_btn)
        browser.execute_script("arguments[0].click();", logout_btn)
        print("\ud83d\udd12 Logged out successfully.")
    except Exception as e:
        print(f"\u26a0\ufe0f Could not log out: {e}")

# === Start ===
try:
    browser.get("https://tes.collegesource.com/TES_login.aspx")
    input("\u23f8\ufe0f Log in to TES manually, then press Enter to continue...")

    for institution, course_code in course_tasks:
        print(f"\n\u27a1\ufe0f Processing: {institution} - {course_code}")
        try:
            # === Step 2: Go to Course Equivalency Page ===
            browser.get(
                "https://tes.collegesource.com/courseequiv/TES_courseequivindex00.aspx"
            )

            # === Step 3: Enter University Name ===
            inst_input = wait.until(
                EC.presence_of_element_located((
                    By.ID,
                    "ContentPlaceHolder1_TES_institutionsearch_uc_tbxInstitutionSearch"
                ))
            )
            inst_input.clear()
            inst_input.send_keys(institution)

            search_btn = wait.until(
                EC.element_to_be_clickable((
                    By.ID,
                    "ContentPlaceHolder1_TES_institutionsearch_uc_btnSearch"
                ))
            )
            browser.execute_script("arguments[0].click();", search_btn)

            # === Step 4: Select Exact Institution Match from Results ===
            max_results = 25
            found = False
            for i in range(max_results):
                try:
                    name_id = (
                        f"ContentPlaceHolder1_TES_institutionsearch_uc_gdvInstitution"
                        f"_lblInstitutionName_{i}"
                    )
                    name_elem = browser.find_element(By.ID, name_id)
                    if name_elem.text.strip().upper() == institution.upper():
                        select_id = (
                            f"ContentPlaceHolder1_TES_institutionsearch_uc_gdvInstitution"
                            f"_btnSelect_{i}"
                        )
                        select_btn = browser.find_element(By.ID, select_id)
                        browser.execute_script("arguments[0].click();", select_btn)
                        found = True
                        break
                except Exception:
                    break  # no more rows
            if not found:
                print(f"⚠️ No exact match found for {institution}")
                log_failure(institution, course_code, "Institution not matched")
                continue

            # === Step 5: Wait for institution page load ===
            wait.until(
                EC.element_to_be_clickable((By.ID, "ContentPlaceHolder1_btnSearchEQ"))
            )

            # === Step 6: Click Course Search Icon ===
            browser.find_element(By.ID, "ContentPlaceHolder1_btnSearchEQ").click()

            # === Step 7: Enter Course Code ===
            type_course_code(course_code)
            time.sleep(2)
            browser.find_element(By.ID, "ContentPlaceHolder1_btnCourseEQSearch").click()
            time.sleep(2)

            # === Step 8: Click Edit Button for First Result ===
            wait.until(
                EC.element_to_be_clickable((
                    By.ID,
                    "ContentPlaceHolder1_gdvCourseEQ_btnEdit_0"
                ))
            ).click()
            time.sleep(2)

            # === Step 9: Click Edit Course Icon ===
            wait.until(
                EC.element_to_be_clickable((By.ID, "ContentPlaceHolder1_btnEditCourse"))
            ).click()

            # === Step 11: Change Department in Dropdown ===
            select_department()
            time.sleep(1)

            # === Step 12: Click Add Course Button 64 ===
            wait.until(
                EC.element_to_be_clickable((
                    By.ID,
                    "ContentPlaceHolder1_gdvEditReceiveCourseList_btnAddReceiveCourse_96"
                ))
            ).click()
            time.sleep(1)

            # === Step 13: Delete Course Equivalency Entry ===
            wait.until(
                EC.element_to_be_clickable((
                    By.ID,
                    "ContentPlaceHolder1_gdvEditReceiveCourseEQList_btnDeleteReceiveCourseEQ_0"
                ))
            ).click()
            time.sleep(2)

            # === Step 14: Done Editing ===
            wait.until(
                EC.element_to_be_clickable((By.ID, "ContentPlaceHolder1_btnDone"))
            ).click()
            time.sleep(2)

            # === Restart Page for Next Iteration ===
            browser.get(
                "https://tes.collegesource.com/courseequiv/TES_courseequivindex00.aspx"
            )
            print(f"\u2705 {institution} - {course_code} processed.")

        except Exception as e:
            print(f"Failed for {institution} - {course_code}")
            log_failure(institution, course_code, e)
            continue

except Exception as e:
    print(f"\u274c Fatal error: {e}")
    safe_logout()
finally:
    try:
        # Navigate directly to home where logout is reliably located
        browser.get("https://tes.collegesource.com/TES_home.aspx")
        time.sleep(2)

        # Try clicking logout
        logout_btn = browser.find_element(By.ID, "btnLogOut")
        logout_btn.click()
        print("✅ Logged out.")
        time.sleep(3)

    except Exception as e:
        print(f"⚠️ Logout failed: {e}")

    finally:
        browser.quit()
        print("🧹 Browser closed. Exiting.")

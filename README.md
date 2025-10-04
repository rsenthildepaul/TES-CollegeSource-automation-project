# TES Course Equivalency Automation

````markdown
# ⚙️ TES Course Equivalency Automation

Automates large-scale updates to **TES (CollegeSource)** course equivalencies using **Selenium WebDriver**.  
The script reads a list of institutions and course codes from a CSV, logs into TES once manually, and automatically:
- searches for institutions,  
- edits course equivalencies,  
- updates departments and dataset years,  
- adds/removes equivalencies,  
- logs failed cases to a text file.

> ✅ Used in production to process **50 000+ course equivalency updates per day**, reducing manual workload from several days to a few hours.

---

## 🚀 Features

- 🧾 **CSV-driven automation** — reads institution and course code pairs directly from a spreadsheet  
- 🔁 **Full end-to-end flow** inside TES:
  - Finds institutions  
  - Searches course codes  
  - Edits and updates equivalencies  
  - Changes department and dataset year  
  - Adds and deletes equivalency records  
- 💾 **Failure logging** — every unmatched or failed record is written to `failure_log.txt`  
- 🧭 **Smart Selenium controls** — uses `WebDriverWait`, retries, and JavaScript `click()` for reliability  
- 🧠 **Scalable** — designed for high-volume, long-running daily automation jobs  
- 🔐 **Manual one-time login** — you log in once, session is reused for all automation steps  

---

## 🗂 Project Structure

```text
tes_automation/
│
├── tes_updater.py              # Main automation script
├── pemain.csv                  # Input dataset (Institution + CourseCode)
├── failure_log.txt             # Log file for failed items
└── README.md                   # This documentation
````

---

## 🧰 Requirements

* **Python** ≥ 3.9
* **Google Chrome** (latest version)
* **ChromeDriver** (auto-managed via `webdriver-manager`)
* TES user credentials with permission to edit course equivalencies

### Install dependencies

```bash
pip install selenium webdriver-manager
```

Recommended `requirements.txt`:

```txt
selenium>=4.23.1
webdriver-manager>=4.0.2
```

---

## ⚙️ Configuration

### 📄 Input CSV — `pemain.csv`

Your CSV must include these columns:

| Column Name           | Example Value               | Description                           |
| --------------------- | --------------------------- | ------------------------------------- |
| SendInstitution       | Waubonsee Community College | Institution name (exact match in TES) |
| SendCourse1CourseCode | ENG101                      | Institution course code to edit       |

> **Note:** Some CSV exports contain a hidden BOM (`\ufeff`); the script handles this automatically.

### 🔧 Hard-coded parameters (edit in code if needed)

```python
institution_col = '\ufeffSendInstitution'     # Column name for institution
course_col = 'SendCourse1CourseCode'          # Column name for course code
failure_log_path = "C:/Users/<you>/Desktop/python/readmit/failure_log.txt"
```

### 💡 Optional Tweaks

* Change department value in:

  ```python
  Select(dropdown).select_by_value("7023968")
  ```
* Change dataset year in:

  ```python
  Select(dropdown).select_by_value("386678")
  ```

  *(values correspond to TES internal dataset IDs)*

---

## ▶️ Usage

1. **Run the script:**

   ```bash
   python tes_updater.py
   ```

2. When prompted:

   ```
   ⏸️ Log in to TES manually, then press Enter to continue...
   ```

   * Complete your normal TES login (including MFA if required).
   * Once inside the dashboard, return to the terminal and press **Enter**.

3. The script will:

   * Read each `(Institution, CourseCode)` from `pemain.csv`
   * Search the institution in TES
   * Open its equivalency list
   * Edit the course equivalency:

     * Change department
     * Change dataset year
     * Add and delete course equivalencies
   * Log any failures

4. Progress is printed in the console; failed rows are saved in:

   ```
   failure_log.txt
   ```

5. When finished, it automatically logs out and closes Chrome.

---

## 🧾 Output Files

### `failure_log.txt`

Logs every (Institution, CourseCode) pair that failed due to:

* Institution not found
* Missing course result
* Timeout or selector changes

Example:

```text
Failed Institution-CourseCode Pairs:
Waubonsee Community College - ENG101
Elgin Community College - BIO102
```

---

## 🧩 Key Implementation Notes

* **Element handling:**
  Uses explicit waits (`WebDriverWait`) and retries for stable performance over long sessions.

* **Selectors:**
  All TES elements are referenced by static IDs such as:

  ```
  ContentPlaceHolder1_tbxCourseCode
  ContentPlaceHolder1_btnCourseEQSearch
  ContentPlaceHolder1_btnEditCourse
  ```

* **Error handling:**
  Wrapped in `try/except` blocks to continue processing next record even if one fails.

* **Long-running safety:**
  Designed to handle large CSVs (tens of thousands of records) over a full workday without restarting.

---

## ⚠️ Best Practices

* Run on a **dedicated workstation** (not a laptop that sleeps).
* Use **stable internet** and **wired connection** if possible.
* Clear TES pop-ups (session expiration warnings) occasionally during multi-hour runs.
* Avoid interacting with the browser while automation is running.

---

## 📈 Performance & Impact

* Average processing speed: **~3 s per equivalency**
* Achieved **50 000+ automated updates** in under 8 hours
* Reduced manual data-entry workload by **~80 %**
* Improved consistency and eliminated human error in repetitive TES updates

---

## 🧪 Troubleshooting

| Issue                                       | Possible Fix                                                                |
| ------------------------------------------- | --------------------------------------------------------------------------- |
| `⚠️ No exact match found for <institution>` | Verify exact institution name in TES matches CSV                            |
| Browser closes unexpectedly                 | Check ChromeDriver auto-update or version mismatch                          |
| Timeout errors                              | Increase WebDriverWait to 45 s                                              |
| Buttons unclickable                         | Use `execute_script("arguments[0].click()", element)` (already implemented) |
| Script stuck on login                       | Make sure you pressed **Enter** after successful manual login               |

---

## 🧠 Future Enhancements

* [ ] Parameterize department and dataset IDs
* [ ] Add progress tracking with timestamps
* [ ] Include optional **headless mode** for server execution
* [ ] Parallel processing with multiple TES sessions
* [ ] Build Streamlit UI to upload CSV and monitor progress

---

## 🧾 License

MIT License © 2025 Rakul Senthilkumar

---

## 📬 Contact

**Rakul Senthilkumar**
📧 [rakulsenthilkumar@gmail.com](mailto:rakulsenthilkumar@gmail.com)
🔗 [LinkedIn](https://linkedin.com/in/rakulsenthilkumar)


from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from utils import write_sheet
import logging
import time
import re


logging.basicConfig(
    filename="app.log",
    filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def is_within_24_hours(posted_time):
    if "second" in posted_time or "minute" in posted_time:
        return True
    elif "hour" in posted_time:
        hours = int(re.search(r"(\d+)", posted_time).group(1))
        return hours <= 24
    elif "day" in posted_time:
        return False
    return False


def filter_job(driver, url):
    driver.get(url)

    time.sleep(3)

    job_containers = driver.find_elements(By.TAG_NAME, "article")

    job_links = []

    for job in job_containers:
        div_ = job.find_element(By.CSS_SELECTOR, ".sc-506be909-0.ksRbQi")
        posted_time_tag = div_.find_element(By.TAG_NAME, "span")
        posted_time = posted_time_tag.text.strip()
        if not is_within_24_hours(posted_time):
            break
        link_tag = job.find_element(By.TAG_NAME, "a")
        job_link = link_tag.get_attribute("href")
        job_links.append(job_link)

    return job_links


def job_detail(driver, url):
    driver.get(url)

    time.sleep(3)

    job_content = driver.find_element(By.TAG_NAME, "main")
    job_title = job_content.find_element(
        By.CSS_SELECTOR, ".sc-a6d70f3d-0.eNLOtt"
    ).text.strip()
    apply_link = job_content.find_element(By.TAG_NAME, "a").get_attribute("href")
    company_name = job_content.find_element(
        By.CSS_SELECTOR, ".sc-a6d70f3d-0.cWvlWe"
    ).text.strip()
    published_on = driver.find_element(
        By.XPATH,
        "//dt[text()='Published on']/following-sibling::dd//span[@class='sc-a6d70f3d-0 bXFXwo']",
    ).text.strip()

    job_desc_element = job_content.find_element(
        By.CSS_SELECTOR, "section.sc-506be909-0.sc-31104e37-3.YxBTc"
    )
    job_desc_text = job_desc_element.text.strip()
    return {
        "Job_Title": job_title,
        "Apply_Link": apply_link,
        "Company_Name": company_name,
        "Published_On": published_on,
        "Job_Description": job_desc_text,
    }


def main():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    PAGE_NUMBER = 50
    try:
        job_data = []
        for page in range(1, PAGE_NUMBER):
            job_links = filter_job(driver, f"https://remote.com/jobs/all?page={page}")
            if job_links:
                for job_link in job_links:
                    job_content = job_detail(driver, job_link)
                    job_data.append(
                        [
                            job_content.get("Job_Title"),
                            job_content.get("Company_Name"),
                            job_content.get("Apply_Link"),
                            job_content.get("Published_On"),
                            job_content.get("Job_Description").replace("\n", " "),
                        ]
                    )
            else:
                break

        try:
            write_sheet(job_data)
            logger.info("Job content posted successfully")
        except Exception as e:
            logger.error("Error occurred: ", e)

    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()

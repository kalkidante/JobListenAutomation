from bs4 import BeautifulSoup
from utils import write_sheet
from datetime import datetime
import requests
import logging


logging.basicConfig(
    filename="app.log",
    filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

now = datetime.now()


def job_links():
    url = "https://weworkremotely.com/remote-jobs/search?search_uuid=&term=&sort=past_24_hours"
    try:

        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        job_listings = soup.find_all("li", class_=lambda x: x == "feature" or x == "")
        links = []
        for job in job_listings:
            a_tags = job.find_all("a")[1]
            link = a_tags.get("href") if a_tags.get("href") else None
            links.append(link)
        return links
    except Exception as e:
        print(e)


def job_detail(link):
    response = requests.get(link)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    job_title = soup.find("h1").get_text(strip=True)
    published_on = soup.find("time").get_text(strip=True)
    company_name = soup.find("h2").get_text(strip=True)
    apply_link = soup.find(
        "a", id=lambda x: x == "job-cta-alt-2" or x == "job-cta-alt"
    ).get("href")
    job_desc_text = soup.find("div", id="job-listing-show-container").get_text(
        strip=True
    )

    return {
        "Job_Title": job_title,
        "Apply_Link": apply_link,
        "Company_Name": company_name,
        "Published_On": f"{published_on}, {now.year}",
        "Job_Description": job_desc_text,
    }


def main():
    job_data = []
    for job_link in job_links():
        job_content = job_detail(f"https://weworkremotely.com{job_link}")
        job_data.append(
            [
                "https://weworkremotely.com/",
                job_content.get("Job_Title"),
                job_content.get("Company_Name"),
                job_content.get("Apply_Link"),
                job_content.get("Published_On"),
                job_content.get("Job_Description").replace("\n", " "),
            ]
        )
    try:
        write_sheet(job_data)
        logger.info("Job content posted successfully")
    except Exception as e:
        logger.error("Error occurred: ", e)


if __name__ == "__main__":
    main()

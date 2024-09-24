### JobListenAutomation Setup Guide

Follow these steps to set up the JobListenAutomation project:

1. ## Obtain the Token File:
   - Access your Google Cloud Console and download the `credentials.json` file.
   - Enable the Google Sheets API.
   - Copy the content of the `credentials.json` and create a new file named `token.json` in your working directory.

2. ## Clone the Repository:
   ```bash
   git clone https://github.com/kalkidante/JobListenAutomation.git
   cd JobListenAutomation
   ```

3. ## Set Up a Virtual Environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. ## Install Required Python Packages:
   ```bash
   pip3 install -r requirements.txt
   ```

5. ## Install Google Chrome:
   - **Update your package list:**
   ```bash
   sudo apt update
   ```

   - **Install necessary packages:**
   ```bash
   sudo apt install wget apt-transport-https ca-certificates
   ```

   - **Download and add the Google signing key:**
   ```bash
   wget https://dl.google.com/linux/linux_signing_key.pub
   sudo apt-key add linux_signing_key.pub
   ```

   - **Add the Google Chrome repository to your sources list:**
   ```bash
   sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
   ```

   - **Update the package list again:**
   ```bash
   sudo apt update
   ```

   - **Install Google Chrome:**
   ```bash
   sudo apt install google-chrome-stable
   ```

6. ## Run the Scripts:
   ```bash
   python3 remote_main.py
   python3 wwr_main.py
   ```
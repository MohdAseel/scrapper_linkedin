# scrapper_linkedin

for scraping linkedin profiles create and .env file and add your linkedin email and password

```env
LINKEDIN_EMAIL=<!urlinkedinemail>
LINKEDIN_PASSWORD=<!password>
```
Then run the following command to install the required packages:

```bash
pip install -r requirements.txt
```

To run the script, use the following command:

```bash
python direct.py
```

example run

```bash
python direct.py
<!urlinkedinemail> <!password>
Press Enter after youve completed any 2FA if prompted... <!enter key>
Driver session is still active. You can continue coding and interacting with the browser.
enter the keyword for the people you want to search for : <!stuff u wann search>
Enter the filename to save the profiles (e.g., profiles.json): <!filename>
Profiles saved to <filename>.json
```
The script will prompt you to enter a search keyword and a filename to save the scraped profiles in JSON format.

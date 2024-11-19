### Installation Steps
#### 1. First install required MySQL dependencies
##### Linux
```
sudo apt update
sudo apt install libmysqlclient-dev mysql-server mysql-client
```
##### MacOS
```
brew install mysql
```

#### 2. Install Python packages
```
cd url_shortner_server
pip install -r requirements.txt
```

#### 3. Sign up for VirusTotal and retrieve an API key
  1. Sign up [here]([https://www.virustotal.com/gui/join-us](https://ipinfo.io/signup)). We _**strongly**_ recommend signing up with your GitHub account.
  2. Follow [these instructions](https://docs.virustotal.com/docs/api-overview) to find your API key.
  3. Create a `.env` file in the `URL-Shortner/url_shortner_server/shortner` directory.
    
    touch URL-Shortner/url_shortner_server/shortner/.env 
  4. Paste your API key in like so:

    VIRUSTOTAL_API_KEY=...

#### 4. Sign up for IP Info and retrieve an Access Token
  1. Sign up [here](https://www.virustotal.com/gui/join-us). We _**strongly**_ recommend signing up with your GitHub account.
  2. Follow [this link](https://ipinfo.io/account/token) to find your Access Token.
  3. Update the `.env` file in the `URL-Shortner/url_shortner_server/shortner` directory.
  4. Paste your Access Token in like so:

    IPINFO_API_TOKEN=...

#### 5. Create a MySQL database on your system
```
# Login to MySQL
sudo mysql -u root -p
CREATE DATABASE urlshortner;
CREATE USER 'root'@'localhost' IDENTIFIED BY 'admin123';
GRANT ALL PRIVILEGES ON urlshortner.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
```

#### 6. Run Migrations and Start server
```
python3 manage.py migrate
python3 manage.py runserver
```

#### 7. Navigate to http://127.0.0.1:8000/

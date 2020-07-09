**Paragomierz server**

Flask server for [paragomierz](https://github.com/trzcioli/paragomierz) is deployed on heroku.

domain = http://paragomierz.herokuapp.com
or local domain (default) = http://127.0.0.1:5000

**api_key** - to find it, log in to [kontomierz](https://kontomierz.pl/) and go to your profile. It's in the "general" tab
**url_api_key** - to find it, log in to kontomierz and go to your profile to the "wallets" tab. You must select the checkbox "URL API active" in order to use this key.

---

Available endpoints:

- /register - POST json: { email, api_key, url_api_key, password } returns access token
- /sign_in - POST { email, password } returns access token
- /api/process-image - POST image multipart file with file as "photo" field. Returns a list of all elements exctacted from image. Login (access token) required
- /api/sum - POST, token required. Sums the expenses by categories and synchronized the result with your kontomierz wallet
- /api/categories - GET, get available categories from kontomierz using your api_key to authenticate

The token that is returned by the register and sign_in endpoints is to be used for authorization. It's extracted from username from http basic authentication, that is in order to use it, base64 encode the token with unused password (e.g. <token>:unused, https://www.base64encode.org/) and include the result in basic auth header: "Authorization: Basic <result>"

---

Example curls:

```console
curl "domain/register" -d '{"email": "your_email", "api_key": "your_api_key", "url_api_key": "your_url_api_key", "password": "your_password"}' -H "Content-Type: application/json" -v

curl "domain/sign_in -H "Content-Type: application/json" -d '{"email": "your_email", "password": "your_password"}' -v

curl "domain/categories" -H "Authorization: Basic your_base64_token" -v
```

---

How to run it locally (examples with conda in order to use pytesseract)?

```console
git clone https://github.com/trzcioli/paragomierz_server.git
cd paragomierz_server
conda create --name paragomierz-server
conda activate paragomierz-server
conda install -c conda-forge pytesseract
conda install pip
pip install -r requirements.txt
export FLASK_APP=paragomierz.py
export DATABASE_URL=your_database_connection_string
```

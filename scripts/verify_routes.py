import urllib.request
import urllib.error
import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

ROUTES = [
    "/",
    "/countries",
    "/universities",
    "/process",
    "/eligibility",
    "/blog",
    "/gallery",
    "/faq",
    "/about",
    "/contact",
    "/privacy",
    "/countries/uzbekistan",
    "/countries/kyrgyzstan",
    "/countries/kazakhstan",
    "/countries/russia",
    "/countries/bangladesh",
    "/countries/georgia",
    "/countries/nepal",
]

BASE_URL = "http://localhost:3000"

print(f"Verifying all {len(ROUTES)} exact clean routes on {BASE_URL}...\n")

passed = 0
failed = 0

for route in ROUTES:
    full_url = BASE_URL + route
    try:
        req = urllib.request.Request(full_url, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req, timeout=5)
        status = res.status
        body = res.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        status = e.code
        body = e.read().decode('utf-8')
    except Exception as e:
        print(f"FAILED: {route} -> {e}")
        failed += 1
        continue

    soup = BeautifulSoup(body, 'html.parser')
    h1 = soup.find('h1')
    h1_text = h1.get_text(strip=True) if h1 else 'No H1'

    # Check expectations
    if status == 200 and len(body) > 5000:
        print(f"OK [200 Clean]: {route} -> Status {status} | '{h1_text}' | {len(body)} bytes")
        passed += 1
    else:
        print(f"FAIL: {route} -> Status {status} | Len: {len(body)}")
        failed += 1

print(f"\nVerification Results: {passed} PASSED, {failed} FAILED out of {len(ROUTES)} routes.")

for removed_route in ["/book", "/book/", "/book.html"]:
    try:
        urllib.request.urlopen(BASE_URL + removed_route, timeout=5)
        print(f"FAIL: Removed route {removed_route} still resolves")
        failed += 1
    except urllib.error.HTTPError as error:
        if error.code == 404:
            print(f"OK [404 Removed]: {removed_route}")
        else:
            print(f"FAIL: {removed_route} -> Status {error.code}")
            failed += 1
    except Exception as error:
        print(f"FAIL: {removed_route} -> {error}")
        failed += 1

sys.exit(1 if failed else 0)

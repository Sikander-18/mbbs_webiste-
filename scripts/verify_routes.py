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
    "/faq",
    "/about",
    "/book",
    "/contact",
    "/privacy",
    "/disclaimer",
    "/countries/uzbekistan",
    "/countries/kyrgyzstan",
    "/countries/kazakhstan",
    "/countries/russia",
    "/countries/bangladesh",
    "/countries/georgia",
    "/countries/nepal",
    "/blog/mbbs-abroad-vs-private-medical-college-india-2026",
    "/blog/top-nmc-approved-universities-russia",
    "/blog/fmge-exam-what-it-is-how-to-prepare",
    "/blog/mbbs-in-georgia-complete-guide-2026",
    "/blog/mbbs-in-kazakhstan-fees-universities-eligibility",
    "/blog/how-to-get-nmc-eligibility-certificate",
    "/blog/life-as-indian-student-in-russia",
    "/blog/neet-score-required-for-mbbs-abroad",
    "/blog/mbbs-abroad-document-checklist",
    "/blog/why-fmge-pass-rate-matters-choosing-university",
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
    if route in ['/privacy', '/disclaimer']:
        if status == 404 and 'Page Not Found' in body and '404' in body:
            print(f"OK [404 Branded]: {route} -> Status {status} | '{h1_text}' | {len(body)} bytes")
            passed += 1
        else:
            print(f"FAIL [Expected 404 Branded]: {route} -> Status {status}")
            failed += 1
    else:
        if status == 200 and len(body) > 5000:
            print(f"OK [200 Clean]: {route} -> Status {status} | '{h1_text}' | {len(body)} bytes")
            passed += 1
        else:
            print(f"FAIL: {route} -> Status {status} | Len: {len(body)}")
            failed += 1

print(f"\nVerification Results: {passed} PASSED, {failed} FAILED out of {len(ROUTES)} routes.")

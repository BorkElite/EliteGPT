
import requests
import concurrent.futures
import time
from playwright.sync_api import sync_playwright

# SOCKS5 sources
proxy_sources = [
    "https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/SOCKS5.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks5.txt",
    "https://api.openproxylist.xyz/socks5.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_anonymous/socks5.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks5.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
    "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
    "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies_anonymous/socks5.txt",
    "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/socks5.txt",
    "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks5.txt",
    "https://raw.githubusercontent.com/prxchk/proxy-list/main/socks5.txt",
    "https://spys.me/socks.txt",
    "https://github.com/zloi-user/hideip.me/raw/refs/heads/master/socks5.txt",
    "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/elliottophellia/yakumo/master/results/socks5/global/socks5_checked.txt",
    "https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/refs/heads/main/socks5.txt",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/refs/heads/main/proxies/protocols/socks5/data.txt"
]

def scrape_proxies():
    proxies = set()
    for url in proxy_sources:
        try:
            response = requests.get(url, timeout=10)
            if response.ok:
                for line in response.text.splitlines():
                    line = line.strip()
                    if line and ':' in line:
                        proxies.add(line)
        except Exception:
            continue
    return list(proxies)

def quick_check_proxy(proxy):
    try:
        proxies = {
            "http": f"socks5h://{proxy}",
            "https": f"socks5h://{proxy}"
        }
        r = requests.get("https://login.live.com", proxies=proxies, timeout=5)
        return r.status_code == 200
    except:
        return False

def fast_validate_stage1(proxies):
    good = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        results = list(executor.map(quick_check_proxy, proxies))
        good = [p for p, passed in zip(proxies, results) if passed]
    return good

def advanced_validate_stage2(proxies):
    verified = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for proxy in proxies:
            try:
                server = "socks5://" + proxy
                context = browser.new_context(proxy={"server": server})
                page = context.new_page()
                page.goto("https://login.live.com", timeout=15000)
                page.wait_for_selector("input[name='loginfmt']", timeout=10000)
                page.goto("https://www.epicgames.com/id/login", timeout=15000)
                page.wait_for_selector("text='Sign in with Epic Games'", timeout=10000)
                verified.append(proxy)
                context.close()
            except:
                context.close()
                continue
        browser.close()
    return verified

def main():
    print("🔍 Scraping proxies...")
    proxies = scrape_proxies()
    print(f"📥 {len(proxies)} proxies scraped.")
    print("⚡ Stage 1: Fast filtering...")
    stage1 = fast_validate_stage1(proxies)
    print(f"✅ {len(stage1)} passed Stage 1.")
    print("🧠 Stage 2: Headless validation...")
    stage2 = advanced_validate_stage2(stage1)
    print(f"🏁 {len(stage2)} proxies fully verified.")
    with open("elite_socks5_proxies.txt", "w") as f:
        for proxy in stage2:
            f.write(proxy + "\n")
    print("📄 Saved to elite_socks5_proxies.txt")

if __name__ == "__main__":
    main()

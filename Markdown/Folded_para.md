<details>
<summary>Async variant</summary>

```py
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        async def log_and_continue_request(route, request):
            print(request.url)
            await route.continue_()

        # Log and continue all network requests
        await page.route("**/*", log_and_continue_request)
        await page.goto("http://todomvc.com")
        await browser.close()

asyncio.run(main())
```

</details>
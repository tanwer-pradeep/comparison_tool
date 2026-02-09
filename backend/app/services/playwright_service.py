from playwright.async_api import async_playwright
import os
import time

class PlaywrightService:
    async def capture_screenshot(self, url: str, output_path: str, width: int = 1920, height: int = 1080):
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            # Emulate browser context if needed
            context = await browser.new_context(viewport={"width": width, "height": height})
            page = await context.new_page()
            
            try:
                await page.goto(url, wait_until="networkidle") # Wait for networkidle to ensure crucial assets loaded
                # Simple heuristic to wait a bit more for stabilize
                # In production, use more robust wait conditions
                await page.wait_for_timeout(2000) 
                
                # Make sure directory exists
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                await page.screenshot(path=output_path, full_page=True)
            except Exception as e:
                print(f"Error capturing screenshot: {e}")
                # Retry logic or handle failure
                raise e
            finally:
                await browser.close()

playwright_service = PlaywrightService()

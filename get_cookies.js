const puppeteer = require('puppeteer');

const fs = require('fs').promises;



(async () => {
  const browser = await puppeteer.launch({args: ['--no-sandbox', '--disable-setuid-sandbox']});
  const page = await browser.newPage();
  await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 SE 2.X MetaSr 1.0');
  await page.goto('https://www.taptap.com/',{timeout:0});
  await page.screenshot({ path: 'example.png' });
  const cookies = await page.cookies();
  await fs.writeFile('./cookies.json', JSON.stringify(cookies, null, 2));

  await browser.close();
})();

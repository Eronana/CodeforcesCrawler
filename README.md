# CodeforcesCrawler
A python script to crawl problems in [Codeforces](http://codeforces.com/)
## How to use
Install wkhtmltopdf
```bash
#Just for Mac users
$ brew cask install wkhtmltopdf
```
Crawl problems and Convert to pdf
```python
python crawl_html.py 1 123 555
#crawl problem from  1 to 123 by 555 threads
```
Now,problems in ./pdf already

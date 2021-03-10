coverage run -m pytest tests
coverage html
cd htmlcov
iexplore.exe index.html
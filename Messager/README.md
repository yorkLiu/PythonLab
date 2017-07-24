# PythonLab
Python Lab

# Required pip tools
```
    pip install requests scrapy logging selenium
```

# Required PhantomJS brwoser
About more [PhantomJS](http://phantomjs.org/)
## To fixed the PhantomJS issue "[Handling JS alert/confirm/prompt](https://github.com/keathley/wallaby/issues/169)"
```
    driver.execute_script("window.alert = function(){}")
    driver.execute_script("window.confirm = function(){return true;}")
    driver.execute_script("window.onbeforeunload=null")
```
That's means define the alert, confirm and onbeforeunload not pop up the model box.


# Using Chrome Driver
```
    chrome = os.environ['webdriver.chrome.driver'] = '/webDriverpath/chromedriver'
    driver = webdriver.Chrome(chrome)
```

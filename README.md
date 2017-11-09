# dioivo
HTTP Benchmarking tool using access log to extract requests and simulate traffic

## What is it?

`dioivo`, previously known as `pywench`, is a tool coded in python that extracts urls from access log file (from apache or nginx)
and generates requests to a target server in a sequenced or random way. 

## Why?

I coded `dioivo` becouse I could not find any tool that does anything similar. I used tools like `ab` to benchmark websites but
only test a single url. I wanted a tool to benchmark a website or an http service based in the requests it uses to have, in the
same proportions of static and dynamic requests and the same proportion of each. 

Thanks to `dioivo` it is easy to actually measure the impact on performance that some configuration values have or any other
measures you take to improve performance. This way it is very useful to optimize websites or to estimate the ammount of traffic
that a platform can handle. I used `dioivo` many times with these objectives and I can say that the numbers look quite good.

## What can it do?

It benchmarks a website and then shows the _minimum_, _average_ and _maximum_ values for *ttfb* (_time to first byte_), *ttlb*
(_time to last byte_) and bandwidth use (_NOTE: the bandwidth use is very rough estimation and it was included recently as an experimental feature_).
Additionaly, it shows the URLs that had, on average, the _minimum_ and _maximum_ _ttfb_ and _ttlb_ so you can identify problematic urls.

A sumary of the returned HTTP codes is shown too.

Then it generates 4 files:
* `.txt` Saves the stats as they are presented in console.
* `.csv` Saves the raw data in case you can use it elsewhere (spreadsheet, graphs, etc)
* `.stat` Saves the stats in JSON format
* `.png` Saves a plot of the `ttfb` and `ttlb` during the benchmark

These are the options it has:

```
usage: usage: dioivo [options] -s SERVER -u URLS_FILE -c CONCURRENCY -n NUMBER_OF_REQUESTS

optional arguments:
  -h, --help            show this help message and exit
  -i TEST_ID, --test-id TEST_ID
                        Identificator for the test. This name will be a suffix
                        for the output files.
  -s HOST, --server HOST
                        Host to benchmark. It must include the protocol and
                        lack of trailing slash. For example:
                        https://example.com
  -u URLS_FILE, --urls URLS_FILE
                        File with url's to test. This file must be directly an
                        access.log file from nginx or apache. It can be
                        gzipped (must end with .gz).
  -c CONCURRENCY, --concurrency CONCURRENCY
                        Number of concurrent requests
  -n TOTAL_REQUESTS, --number-of-requests TOTAL_REQUESTS
                        Number of requests to send to the host.
  -m MODE, --mode MODE  Mode can be 'random' or 'sequence'. It defines how the
                        urls will be chosen from the url's file.
  -R REPLACE_PARAMETER, --replace-parameter REPLACE_PARAMETER
                        Replace parameter on the URLs that have such
                        parameter: p.e.: 'user=hackme' will set the parameter
                        'user' to 'hackme' on all url that have the 'user'
                        parameter. Can be called several times to make
                        multiple replacements.
  -A AUTH_RULE, --auth AUTH_RULE
                        Adds rule for form authentication with cookies.
                        Syntax:
                        'METHOD::URL[::param1=value1[::param2=value2]...]'.
                        For example: 'POST::http://example.com/login.py::user=
                        root::pass=hackme'. NOTE: Use full url with protocol
                        as in the example.
  --http-version HTTP_VERSION
                        Defines which protocol version to use. Use '11' for
                        HTTP 1.1 and '10' for HTTP 1.0
  -H HEADERS, --add-header HEADERS
                        Adds a header to the requests. It can be specified
                        multiple times. For example: -H 'User-Agent:
                        MyUserAgent'
  -e, --examine         If you enable this flag, you'll be able to examine the
                        graph for the benchmark when it finishes. Note that
                        this requires matplotlib and an X environment.
  -M METHODS, --methods METHODS
                        Comma separated list of methods to be looked for in
                        the access log file. Default only GET requests are
                        used. For example: 'GET,PUT,DELETE'
  -D, --debug           Show debug information. For debugging only.
  -V, --version         Show version information and exit.
```

## Example of use

In this example I used a test server with a new wordpress installation. I got the `access.log` file (this one had only around 20 requets but it may have thousands, that is why it also opens gziped access.log) and executed the following command with the most basic options that `dioivo` requires. _NOTE: The domain is of course an example_.

```
dioivo -s https://wordpress.myexample.net -u /tmp/test_access.log -c 20 -n 5000
```
And after the fancy progress bar finishes, we see this information in the console output

```
  Requests: 5000		Concurrency: 20
                                                                    
  Stats              

  	    minimum		     average		    maximum
  	    -------		     -------		    -------
  ttfb	0.04933 s	     0.06236 s	    0.85967 s
  ttlb	0.04943 s	     0.06917 s	    0.91487 s

  mbps	2.329 Mbps	   100.574 Mbps	  418.695 Mbps


  Requests per second: 285 rps


  URL min ttfb: (0.05925 s) /wp-content/themes/twentyseventeen/assets/js/global.js?ver=1.0
  URL max ttfb: (0.06688 s) /wp-includes/js/jquery/jquery-migrate.min.js?ver=1.4.1
  URL min ttlb: (0.05944 s) /wp-content/themes/twentyseventeen/assets/js/global.js?ver=1.0
  URL max ttlb: (0.14086 s) /wp-content/themes/twentyseventeen/assets/images/header.jpg
  NOTE: These stats are based on the average time (ttfb or ttlb) for each url.


  Protocol stats:
	     HTTP 200:  5000 requests (100.00%)
```
And it also generates this 4 files:

* wordpress.myexample.net_r5000_c20.csv
* wordpress.myexample.net_r5000_c20.png
* wordpress.myexample.net_r5000_c20.stat
* wordpress.myexample.net_r5000_c20.txt

In this case, the generated graph looks like this

![plot](https://i.imgur.com/fjQpHPo.png)

*Clarification* You may ask why the initial spike. This was a new server installed behind the _treitos caching platform_. The first requests were not in the cache so they took more time to be served. Afther the caches were populated things were much faster.


## How can I install it?

`dioivo` has 2 requirements

  * `urllib3`
  * `numpy`
  
 but if you want to have the graphs, you will need to install `matplotlib` too.
 
 You can install `dioivo` with
 
 ```
 pip install dioivo
 ```

## FAQ

* Why was it splited from the dgtool repository ?

  I found that the project got mature enough to have a repository of its own so I could properly manage it.
  
* Why the name change ?

  Well... I thought that `pywench` was not a bad enough name.
  
* What headers does `dioivo` use by default ?

  By default it sends:
  
  * `User-Agent: dioivo/{{ VERSION }}`                                                                                                                                                                                                     
  * `Accept-Encoding: gzip, deflate`

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







## FAQ

* Why was it splited from the dgtool repository ?
* Why the name change ?
* What headers does `dioivo` use by default ?

import concurrent.futures
import requests

URLS = ["http://participedia.net/en/node/" + str(num) for num in range(4256)]

# Retrieve a single page and report the url and contents
def load_url(url, timeout):
    return requests.get(url).text

# We can use a with statement to ensure threads are cleaned up promptly
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    # Start the load operations and mark each future with its URL
    future_to_url = {executor.submit(load_url, url, 60): url for url in URLS}
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            data = future.result()
        except Exception as exc:
            print('%r generated an exception: %s' % (url, exc))
        else:
            print('%r page is %d bytes' % (url, len(data)))
            fname = url[url.rindex('/')+1:]
            open('www.participedia.net/'+fname, 'w').write(data.encode('utf-8'))

import requests
import time
import boto3

# Cloudfront URLs
main_page = "https://d375bq98et1741.cloudfront.net/index.html"
dogs_page = "https://d375bq98et1741.cloudfront.net/dogs.html"
cats_page = "https://d375bq98et1741.cloudfront.net/cats.html"


def invalidate_cache(distribution_id, paths):
    client = boto3.client('cloudfront')
    invalidation = client.create_invalidation(
        DistributionId=distribution_id,
        InvalidationBatch={
            'Paths': {
                'Quantity': len(paths),
                'Items': paths
            },
            'CallerReference': str(time.time())
        }
    )
    return invalidation

def make_request(url, expected_x_cache):
    start_time = time.time()
    response = requests.get(url)
    elapsed_time = time.time() - start_time
    x_cache = response.headers.get('x-cache', '')
    print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())}, Elapsed Time: {elapsed_time}, URL: {url}, HTTP Response Code: {response.status_code}, x-cache: {x_cache}")
    assert x_cache == expected_x_cache, f"Expected x-cache {expected_x_cache}, but got {x_cache}"
    return response

def check_invalidation_status(distribution_id, invalidation_id):
    client = boto3.client('cloudfront')
    invalidation = client.get_invalidation(DistributionId=distribution_id, Id=invalidation_id)
    return invalidation['Invalidation']['Status']

# Invalidate cache at the beginning of the test
distribution_id = 'E3BS5Y813LSP7U'
paths = ['/*']  # Invalidate all paths
invalidation = invalidate_cache(distribution_id, paths)
invalidation_id = invalidation['Invalidation']['Id']

# Wait for the invalidation to complete
while check_invalidation_status(distribution_id, invalidation_id) != 'Completed':
    print('Waiting for invalidation to complete...')
    time.sleep(30)  # Wait for 30 seconds before checking again

print('Invalidation completed.')

# Simulate cache hits and misses
for page in [main_page, dogs_page, cats_page]:
    make_request(page, 'Miss from cloudfront')  # Cache miss
    time.sleep(5)  # Wait for less than 15 seconds
    make_request(page, 'Hit from cloudfront')  # Cache hit
    time.sleep(20)  # Wait for more than 15 seconds
    make_request(page, 'RefreshHit from cloudfront')  # Refresh hit
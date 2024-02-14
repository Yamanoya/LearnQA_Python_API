import requests

base_path = "https://playground.learnqa.ru/api/"


def exams_six_long_redirect():
    response = requests.get(url=base_path + "long_redirect", allow_redirects=True)
    count_redirects = 0

    for urls in response.history:
        count_redirects += 1
        print(f"Редирект {count_redirects}:", urls.url)

    endpoint_url = response.url
    print('Конечный url:', endpoint_url)

    print('Общее кол-во редиректов:', count_redirects)


exams_six_long_redirect()


def exams_seven_requests_and_methods():
    url = 'https://playground.learnqa.ru/ajax/api/compare_query_type'

    # запрос get без параметра
    response_without_method = requests.get(url=url)
    print(response_without_method.text)

    # запрос не из списка. HEAD
    response_invalid_method = requests.head(url=url)
    print(response_invalid_method.text)

    # запрос с правильным значением method post
    response_valid_method = requests.post(url=url, data={"method": "POST"})
    print(response_valid_method.text)

    # цикл с запросами
    methods = ['GET', 'POST', 'PUT', 'DELETE']

    for method in methods:
        response_get = requests.get(url, params={'method': method})
        print(response_get.text)

    for method in methods:
        response_post = requests.post(url, data={'method': method})
        print(response_post.text)

    for method in methods:
        response_put = requests.put(url, data={'method': method})
        print(response_put.text)

    for method in methods:
        response_delete = requests.delete(url, data={'method': method})
        print(response_delete.text)


exams_seven_requests_and_methods()

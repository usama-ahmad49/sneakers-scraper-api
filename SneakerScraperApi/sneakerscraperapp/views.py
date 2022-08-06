from django.http import JsonResponse
from django.http import HttpResponse
# from regex import E
from .models import Drink
from .serializers import DrinkSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests
import json
import random
import os
import urllib.request
import concurrent.futures
 
cwd = os.getcwd()
#D:\DjangoAPI\Drinks\SneakerScraperApi\sneakerscraperapp\proxies.txt
value = open('.\sneakerscraperapp\proxies.txt','r')
proxy = value.readlines()[0]

certificate = 'D:\Work\sneakers-scraper-api\SneakerScraperApi\sneakerscraperapp\zyte-smartproxy-ca.crt'
proxy_auth = proxy
proxies={
        "http": f"http://{proxy_auth}@proxy.crawlera.com:8011/",
        "https": f"http://{proxy_auth}@proxy.crawlera.com:8011/",
    }
def set_http_proxy(proxy):
        if proxy == None: # Use system default setting
            proxy_support = urllib.request.ProxyHandler()
        elif proxy == '': # Don't use any proxy
            proxy_support = urllib.request.ProxyHandler({})
        else: # Use proxy
            proxy_support = urllib.request.ProxyHandler(proxy)
        opener = urllib.request.build_opener(proxy_support)
        urllib.request.install_opener(opener)

# def proxy_request(url, prox, headers):
#     try:
#         set_http_proxy(prox)
#         request = urllib.request.Request(url, headers=headers)
#         response = urllib.request.urlopen(request)
#         response_json = json.loads(response.read())
#         return response_json
#     except:
#         pass

@api_view(['GET','PUT','DELETE'])
def sku_details(request,id):    
    # stockx_sku = str(id)
    try:         
        split_sku = str(id).split('_')
        stockx_sku = split_sku[0]
        goat_sku = split_sku[1]
        region = split_sku[2]
        proxy_flag = split_sku[3]
    except:
        return JsonResponse({'message':'something went wrong Please try again'},safe=False)
    
        # goat_sku_2 =  goat_sku.replace('%20',' ')
        
    headers_stockx = {
        'authority': 'stockx.com',
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9',
        'app-platform': 'Iron',
        'app-version': '2022.05.22.05',
        # 'cookie': 'stockx_market_country=PK; _ga=GA1.2.788108403.1627381998; pxcts=0e9c4630-eec6-11eb-8f35-456c805b484e; _scid=d66f0315-e66c-43f7-9088-cb913be1d684; below_retail_type=; product_page_affirm_callout_enabled_web=false; riskified_recover_updated_verbiage=true; home_vertical_rows_web=true; _px_f394gi7Fvmc43dfg_user_id=MTA0OTU5ZjEtZWVjNi0xMWViLTkzMWQtNzU0NDc2NWQ2YjUy; QuantumMetricUserID=d09c7fd3ca35f4883252442e93c26ffb; rskxRunCookie=0; rCookie=o5z2ngw5qrkce8yubt0e7tkrlx854q; __pdst=889c3ece03e34c9b91f9e7bf94bb5d0f; IR_gbd=stockx.com; _rdt_uuid=1627382004357.08170ccd-84e5-4727-b809-30b9e8d7868b; __ssid=3ff3af1fd98b9b60409658d135799ec; __pxvid=87150fcf-0428-11ec-a4f3-0242ac110002; _ts_yjad=1629827453266; stockx_preferred_market_activity=sales; stockx_dismiss_modal_set=2021-09-16T06%3A39%3A57.270Z; stockx_dismiss_modal=true; stockx_dismiss_modal_expiration=2022-09-16T06%3A39%3A57.270Z; language_code=en; stockx_selected_locale=en; stockx_selected_region=AE; _pin_unauth=dWlkPVpUbGhZMlJqTURVdFlUQmhNaTAwTnpBeUxXSXpNVFl0WmpFeFpUZzRPVFF5WkdGag; ajs_user_id=ac1c19d7-2c10-11ec-9825-124738b50e12; hide_my_vices=false; _ga=GA1.2.788108403.1627381998; _pxvid=585cc9e2-407d-11ec-8d1c-64567a454275; tracker_device=27b681b3-d4ee-46b6-a122-8f55e17dbcd6; stockx_default_watches_size=All; ops_banner_id=blt055adcbc7c9ad752; ajs_group_id=ab_3ds_messaging_eu_web.false%2Cab_aia_pricing_visibility_web.novariant%2Cab_chk_germany_returns_cta_web.true%2Cab_chk_order_status_reskin_web.false%2Cab_chk_place_order_verbage_web.true%2Cab_chk_remove_affirm_bid_entry_web.true%2Cab_chk_remove_fees_bid_entry_web.true%2Cab_citcon_psp_web.true%2Cab_desktop_home_hero_section_web.control%2Cab_home_contentstack_modules_web.variant%2Cab_home_dynamic_content_targeting_web.variant%2Cab_low_inventory_badge_pdp_web.variant_1%2Cab_pirate_recently_viewed_browse_web.true%2Cab_product_page_refactor_web.true%2Cab_recently_viewed_pdp_web.variant_1%2Cab_test_korean_language_web.true%2Cab_web_aa_1103.true; ajs_anonymous_id=b9050503-b549-4117-af17-cac10db592f1; rbuid=rbos-61bd9993-7bb9-479b-a120-f59e7774fe7c; stockx_seen_ask_new_info=true; __lt__cid=10d40d29-894a-4333-ba79-89ba26e91495; stockx_device_id=web-410547fe-366d-4695-9c14-ec7bb493c03a; stockx_default_collectibles_size=All; stockx_default_streetwear_size=XL; _gcl_au=1.1.929965137.1650868871; _tt_enable_cookie=1; _ttp=943cb6e4-acfa-4634-ac92-93ef25b9a577; _derived_epik=dj0yJnU9YlJyUXhxZG5sVy1ZdDVXS2p4anhZbGJqWjU1R05Zcncmbj1ud042c3BJT0cwa09SOE5ZRkxqaWJnJm09MSZ0PUFBQUFBR0ozZDQ4JnJtPTEmcnQ9QUFBQUFHSjNkNDg; stockx_default_handbags_size=All; OptanonAlertBoxClosed=2022-05-30T07:00:41.776Z; NA_SAC=dT1odHRwcyUzQSUyRiUyRnN0b2NreC5jb20lMkZidXklMkZuaWtlLWR1bmstbG93LXJhY2VyLWJsdWUtd2hpdGUlM0ZzaXplJTNEMTQlMjZkZWZhdWx0QmlkJTNEdHJ1ZXxyPQ==; _gid=GA1.2.1140692933.1654499259; stockx_default_sneakers_size=All; stockx_selected_currency=USD; _clck=11tpq9c|1|f25|0; QuantumMetricSessionID=8ec698fb4284a7ad892efac38609cc43; stockx_session=1e4e5212-493f-48ca-9fb1-6eb4b24c27f2; stockx_homepage=handbags; stockx_product_visits=458; __cf_bm=rA21_wOyvht3ww6tE1U1scoR3AaKQkiVp.OUl9_DxiM-1654666582-0-AQsjlHGG/Z7ouifxEgbZh21ZqCrSOHryXSyO2ig4Gp7nonNON2Gtnu7eSSjLTE2NtX8wx4fjmnscOWDpwU0hpp0=; _pxff_idp_c=1,s; OptanonConsent=isGpcEnabled=0&datestamp=Wed+Jun+08+2022+10%3A36%3A25+GMT%2B0500+(Pakistan+Standard+Time)&version=6.36.0&isIABGlobal=false&hosts=&consentId=f03f1052-c1ce-4d1a-bbfc-3c958dc4d2c9&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0005%3A1%2CC0004%3A1%2CC0003%3A1&AwaitingReconsent=false&geolocation=PK%3BPB; _gat=1; forterToken=f97714707aaa44c8bda665516444d4dd_1654666585203_8757_UDF43_13ck; _px3=43ff5af2ceadb9c3fb2d6d01b2a1be4a22d6e9f6ef4ff86a4d544055326c111e:6Ic6vf80GL6tCB84QP1utKUYl246BE3AMqezybcVpJWglAmiYXUETmrZYoeFW8uvZUHCZsgJ8HHs8vuMcKmrzw==:1000:FJVQFgTNG94ud9T91fY5SMnNwQpoTVGWnKfsDiuEFYd1q7DfCG8oBIyEbezdcmHeT8hOye1oWLGNBto2jpsFSsPgIAsDLDYz1MilVDjZa9zFzrYUE15jhNkPvPWinRHducVzL7f41XqB9+JfFCjPpOKiVmewPg6oWYsfEVVEOV8h9RrWWgi7pALoqiFEpVRhm1sBPpbFf3Riz3jPQ/F6YjVXQORiWDon12WIyHmRFyY=; _uetsid=5bcced00e56711ecb1b9412aa71c20e6; _uetvid=0f591ae0eec611eb9ff5fdfee065b825; lastRskxRun=1654666589796; IR_9060=1654666591150%7C0%7C1654666591150%7C%7C; IR_PI=124d676f-eec6-11eb-84ad-4f7348310cc7%7C1654752991150; _clsk=11noh3o|1654666592371|5|0|j.clarity.ms/collect; _pxde=135c39b4e9e2c20d7f0f4890957ddc0b2dd0a89e1c55d0e0769f12aec385613f:eyJ0aW1lc3RhbXAiOjE2NTQ2NjY2MDU0MTIsImZfa2IiOjB9; _dd_s=rum=0&expire=1654667525616',
        'dnt': '1',
        'if-none-match': 'W/"4d7-uDYu/KTc1fvaVY0AFnSCdrRNFxU"',
        'referer': 'https://stockx.com/',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        "X-Crawlera-Profile":"pass"
    }
    headers = {
        'Host': 'stockx.com',
        'Connection': 'keep-alive',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
        'sec-ch-ua-mobile': '?0',
        'App-Platform': 'Iron',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'App-Version': '2022.05.22.04',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://stockx.com/buy/nike-dunk-low-racer-blue-white?size=14&defaultBid=true',
        "X-Crawlera-Profile":"pass",
        
        # 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US,en;q=0.9',
        # 'Cookie':'stockx_device_id=0420c803-759c-4e65-aea0-4255ff491cbd; stockx_session=7b72df45-ec30-4b91-a2a8-a4acd5d3c486; pxcts=77c76a62-ebc8-11ec-a732-63766b486259; _pxvid=77c75f03-ebc8-11ec-a732-63766b486259; _ga=undefined; __pxvid=786173fa-ebc8-11ec-ac1a-0242ac120002; ajs_anonymous_id=61c6c8b8-5730-4ae4-aeb3-ddc9cb54c077; __ssid=ac596e942ac2d7706166fecf1797338; rskxRunCookie=0; rCookie=wlbmhbmv5bihlzer6pv4ial4dzqzdx; rbuid=rbos-90198fa9-287b-44e5-9689-6270bad8753a; _pin_unauth=dWlkPVlURmpNV1psTmpZdE9ESTRNaTAwTVROakxXSmxZakV0WkROa1ltRXhZbVV4TWpsaA; stockx_selected_currency=SGD; stockx_selected_locale=en; language_code=en; stockx_selected_region=SG; stockx_dismiss_modal=true; stockx_dismiss_modal_set=2022-06-14T09%3A58%3A03.261Z; stockx_dismiss_modal_expiration=2023-06-14T09%3A58%3A03.260Z; stockx_preferred_market_activity=sales; stockx_default_sneakers_size=All; stockx_homepage=sneakers; __cf_bm=OloZda.vx_3EuBUUmetulZ4Dua4OnH_PCl70JPC2hAk-1655201479-0-AQKcHlqpuY8ac9dActCoJucZ+IfpR66V5l+2Y1tbc5tWiZBMMxu0wYp8r7pYDjwvc9QYpwkXNu2u53EOCO2b7A4=; stockx_product_visits=2; _pxff_idp_c=1,s; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Jun+14+2022+15%3A11%3A21+GMT%2B0500+(Pakistan+Standard+Time)&version=6.36.0&isIABGlobal=false&hosts=&consentId=60d00bff-a929-4c57-a324-d1b700db881b&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A0%2CC0004%3A0%2CC0005%3A0%2CC0003%3A0&AwaitingReconsent=false; forterToken=bddd440983b6481d9121c3a95761fd51_1655201481105__UDF43_13ck; _px3=e754a73fcc1e50eefecb0a051eb0067b12d196ad39ce9986cd8b918a327a5fd4:RUp382dSczzIyJP2JtPQ5Wl2YncZCJCapoHRgBo3wwSku0lfIxH9hs3NHKvaZGouqEaTxE/67E4/+1p6l1OU5w==:1000:jA6132MynF+dwMqHSP8wQXrmUCiskN5saSXHHyvgWNm1miR2q0ko4V8lTXpaMhNZ+tEvbFenBRQQFYmTKaBTAJo9S8A6PDmDeI9aXlry/wiYUuzdpi4DeyNwboeBCZigfV2G5jVs6JHx5dXH/AJ9kYN3b5Eh77kx65SwET8SmR4alb6pB5gvKUMmjyWYZjst6u1jmKzH7EBZeo/ru7Cdbg==; lastRskxRun=1655201486553; _dd_s=rum=0&expire=1655202392628; _pxde=b6db7aaa3d29356fa5f3846824a8bedf143b0f8d81c046d9d72d932523564355:eyJ0aW1lc3RhbXAiOjE2NTUyMDE0OTI4NDYsImZfa2IiOjB9'
    }
    

    url=f'https://stockx.com/api/browse?_search={stockx_sku}&resultsPerPage=10&dataType=product&facetsToRetrieve[]=browseVerticals&propsToRetrieve[][]=brand&propsToRetrieve[][]=colorway&propsToRetrieve[][]=media&propsToRetrieve[][]=title&propsToRetrieve[][]=productCategory&propsToRetrieve[][]=shortDescription&propsToRetrieve[][]=styleId&&propsToRetrieve[][]=urlKey'
    if proxy_flag=='Yes':
        try:
            response = requests.get(url, proxies=proxies, verify=certificate, headers = headers_stockx)
            response_json = json.loads(response.text)
        except:
            return JsonResponse({'message':'something went wrong Please try again'},safe=False)
    elif proxy_flag=='No':
        try:
            response_json =json.loads(requests.get(url=url,headers=headers_stockx).text)    
        except:
            return JsonResponse({'message':'something went wrong Please try again'},safe=False)
    else:
        return JsonResponse({'message':'something went wrong Please try again part'},safe=False)



    
    try:
        for i in response_json['Products']:
            if i['styleId'] == stockx_sku:            
                url_key = i['urlKey']
                break
        if proxy_flag=='Yes':
            url = f'https://stockx.com/api/products/{url_key}?includes=market,360&currency=USD&country={region}'
            try:
                response = requests.get(url, proxies=proxies, verify=certificate, headers = headers_stockx)
                product_json = json.loads(response.text)
            except:
                return JsonResponse({'message':'something went wrong Please try again'},safe=False)

        elif proxy_flag=='No':
            try:
                product_json = json.loads(requests.get(f'https://stockx.com/api/products/{url_key}?includes=market,360&currency=USD&country={region}',headers=headers).text)
            except:
                return JsonResponse({'message':'something went wrong Please try again'},safe=False)    

        main_dic = dict()
        try:
            main_dic["lowestResellPrice"] = dict()
            main_dic["lowestResellPrice"]['stockX'] = product_json['Product']['market']['lowestAsk']
            main_dic["lowestResellPrice"]['goat'] = ''
        
            main_dic['resellPrices'] = dict()

            main_dic['resellPrices']['stockX'] = dict()
            main_dic['resellPrices']['goat'] = dict()

            for children in product_json['Product']['children']:
                if product_json['Product']['children'][children]['market']['lowestAsk']!=0:
                    main_dic['resellPrices']['stockX'][product_json['Product']['children'][children]['shoeSize']] = product_json['Product']['children'][children]['market']['lowestAsk']
        except:
            JsonResponse({'message':'something went wrong Please try again'},safe=False)


        # goat scraping

        headers_goat = {
            'authority': 'ac.cnstrc.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'origin': 'https://www.goat.com',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
            }

        params_goat = {
            'c': 'ciojs-client-2.27.10',
            'key': 'key_XT7bjdbvjgECO5d8',
            'i': '778c546d-41a5-4c0e-b56d-6a3d8de8a6aa',
            's': '4',
            'num_results_per_page': '25',
            '_dt': '1654779233399',
        }
        headers2 = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Origin': 'https://www.goat.com',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
            'content-type': 'application/x-www-form-urlencoded',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            }
        try:
            search_json = json.loads(requests.get(f'https://ac.cnstrc.com/search/{goat_sku}', params=params_goat, headers=headers_goat).text)
        except:
            return JsonResponse({'message':'something went wrong Please try again'},safe=False)    
        search_id_goat = ''
        slug = ''
        # print(search_json)
        for i in search_json['response']['results']:
            if i['data']['sku'] == goat_sku:
                
                search_id_goat = i['data']['id']                
                slug = i['data']['slug']                                                                        
                main_dic['lowestResellPrice']['goat'] =  i['data']['lowest_price_cents']/100
                   
                

        data = '{"query":"","facetFilters":["product_template_id:'+search_id_goat+'"],"hitsPerPage":100}'    

        # if proxy_flag=='Yes':    
        #     response_product = json.loads(requests.post('https://2fwotdvm2o-dsn.algolia.net/1/indexes/product_variants_v2/query?x-algolia-agent=Algolia%20for%20JavaScript%20(4.13.1)%3B%20Browser%20(lite)&x-algolia-api-key=ac96de6fef0e02bb95d433d8d5c7038a&x-algolia-application-id=2FWOTDVM2O', headers=headers2, data=data).text)

        # else:
        #     response_product = json.loads(requests.post('https://2fwotdvm2o-dsn.algolia.net/1/indexes/product_variants_v2/query?x-algolia-agent=Algolia%20for%20JavaScript%20(4.13.1)%3B%20Browser%20(lite)&x-algolia-api-key=ac96de6fef0e02bb95d433d8d5c7038a&x-algolia-application-id=2FWOTDVM2O', headers=headers2, data=data,proxies=proxies).text)
        try:
            response_product = json.loads(requests.post('https://2fwotdvm2o-dsn.algolia.net/1/indexes/product_variants_v2/query?x-algolia-agent=Algolia%20for%20JavaScript%20(4.13.1)%3B%20Browser%20(lite)&x-algolia-api-key=ac96de6fef0e02bb95d433d8d5c7038a&x-algolia-application-id=2FWOTDVM2O', headers=headers2, data=data).text)     
        except:
            return JsonResponse({'message':'something went wrong Please try again'},safe=False)    
               
        try:
            # if proxy_flag=='Yes':  
            #     try:          
            #         response_product = json.loads(requests.post('https://2fwotdvm2o-dsn.algolia.net/1/indexes/product_variants_v2/query?x-algolia-agent=Algolia%20for%20JavaScript%20(4.13.1)%3B%20Browser%20(lite)&x-algolia-api-key=ac96de6fef0e02bb95d433d8d5c7038a&x-algolia-application-id=2FWOTDVM2O', headers=headers2, data=data,proxies=proxies).text)
            #     except:
            #         return JsonResponse({'message':'something went wrong Please try again'},safe=False)    
            # elif proxy_flag=='No':
            #     try:
            #         response_product = json.loads(requests.post('https://2fwotdvm2o-dsn.algolia.net/1/indexes/product_variants_v2/query?x-algolia-agent=Algolia%20for%20JavaScript%20(4.13.1)%3B%20Browser%20(lite)&x-algolia-api-key=ac96de6fef0e02bb95d433d8d5c7038a&x-algolia-application-id=2FWOTDVM2O', headers=headers2, data=data).text)     
            #     except:
            #         return JsonResponse({'message':'something went wrong Please try again'},safe=False)    
            for j in response_product['hits']:                            
                if ((j['shoe_condition'] == 'new_no_defects') and (j['has_stock'] == True) and (j['box_condition']=='good_condition')):                
 
                    main_dic['resellPrices']['goat'][j['size']] = j['lowest_price_cents_usd']/100
                               
        except:
            return JsonResponse({'message':'something went wrong Please try again'})



        main_dic['imageLinks'] = []
        try:
            main_dic['_id'] = product_json['Product']['id']
        except:
             main_dic['_id'] = ''
        try:
            main_dic['shoeName'] = product_json['Product']['title']
        except:
            main_dic['shoeName'] = ''
        try:
            main_dic['brand'] = product_json['Product']['brand']
        except:
             main_dic['brand'] = ''


        try:
            main_dic['silhoutte'] = product_json['Product']['shoe']
        except:
             main_dic['silhoutte'] = ''    
        try:
            main_dic['styleID'] = product_json['Product']['styleId']
        except:
             main_dic['styleID'] = ''    
        try:     
            main_dic['make'] = product_json['Product']['shoe']
        except:
            main_dic['make'] = ''

        try:
            main_dic['colorway'] = product_json['Product']['colorway']
        except:
             main_dic['colorway'] =''

        try:
            main_dic['retailPrice'] = product_json['Product']['retailPrice']
        except:
             main_dic['retailPrice'] = ''

        try:
            main_dic['thumbnail'] = product_json['Product']['media']['thumbUrl']
        except:
            main_dic['thumbnail'] =''

        main_dic['releaseDate'] = ''
        main_dic['description'] = ''
        try:
            main_dic['urlKey'] = product_json['Product']['urlKey']
        except:
            main_dic['urlKey'] = ''

        main_dic['resellLink'] = dict()
        try:    
            main_dic['resellLink']['stockX'] = 'https://stockx.com/'+main_dic['urlKey']
        except:
            main_dic['resellLink']['stockX'] = ''

        try:
            main_dic['resellLink']['goat'] = slug
        except:
            main_dic['resellLink']['goat'] = ''

 
        return JsonResponse(main_dic,safe=False)

    except Exception as e:
        return JsonResponse(main_dic,safe=False)


@api_view(['GET','PUT','DELETE'])
def stockx_details(request,id):
    try:
        stockx_sku_split = str(id)
        stockx_sku = stockx_sku_split.split('_')[0]    
        region = stockx_sku_split.split('_')[1]
        proxy_flag = stockx_sku_split.split('_')[2]

    except:
        return JsonResponse({'message':'something went wrong Please try again'})


    
    headers_stockx = {
        'authority': 'stockx.com',
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9',
        'app-platform': 'Iron',
        'app-version': '2022.05.22.05',
        # 'cookie': 'stockx_market_country=PK; _ga=GA1.2.788108403.1627381998; pxcts=0e9c4630-eec6-11eb-8f35-456c805b484e; _scid=d66f0315-e66c-43f7-9088-cb913be1d684; below_retail_type=; product_page_affirm_callout_enabled_web=false; riskified_recover_updated_verbiage=true; home_vertical_rows_web=true; _px_f394gi7Fvmc43dfg_user_id=MTA0OTU5ZjEtZWVjNi0xMWViLTkzMWQtNzU0NDc2NWQ2YjUy; QuantumMetricUserID=d09c7fd3ca35f4883252442e93c26ffb; rskxRunCookie=0; rCookie=o5z2ngw5qrkce8yubt0e7tkrlx854q; __pdst=889c3ece03e34c9b91f9e7bf94bb5d0f; IR_gbd=stockx.com; _rdt_uuid=1627382004357.08170ccd-84e5-4727-b809-30b9e8d7868b; __ssid=3ff3af1fd98b9b60409658d135799ec; __pxvid=87150fcf-0428-11ec-a4f3-0242ac110002; _ts_yjad=1629827453266; stockx_preferred_market_activity=sales; stockx_dismiss_modal_set=2021-09-16T06%3A39%3A57.270Z; stockx_dismiss_modal=true; stockx_dismiss_modal_expiration=2022-09-16T06%3A39%3A57.270Z; language_code=en; stockx_selected_locale=en; stockx_selected_region=AE; _pin_unauth=dWlkPVpUbGhZMlJqTURVdFlUQmhNaTAwTnpBeUxXSXpNVFl0WmpFeFpUZzRPVFF5WkdGag; ajs_user_id=ac1c19d7-2c10-11ec-9825-124738b50e12; hide_my_vices=false; _ga=GA1.2.788108403.1627381998; _pxvid=585cc9e2-407d-11ec-8d1c-64567a454275; tracker_device=27b681b3-d4ee-46b6-a122-8f55e17dbcd6; stockx_default_watches_size=All; ops_banner_id=blt055adcbc7c9ad752; ajs_group_id=ab_3ds_messaging_eu_web.false%2Cab_aia_pricing_visibility_web.novariant%2Cab_chk_germany_returns_cta_web.true%2Cab_chk_order_status_reskin_web.false%2Cab_chk_place_order_verbage_web.true%2Cab_chk_remove_affirm_bid_entry_web.true%2Cab_chk_remove_fees_bid_entry_web.true%2Cab_citcon_psp_web.true%2Cab_desktop_home_hero_section_web.control%2Cab_home_contentstack_modules_web.variant%2Cab_home_dynamic_content_targeting_web.variant%2Cab_low_inventory_badge_pdp_web.variant_1%2Cab_pirate_recently_viewed_browse_web.true%2Cab_product_page_refactor_web.true%2Cab_recently_viewed_pdp_web.variant_1%2Cab_test_korean_language_web.true%2Cab_web_aa_1103.true; ajs_anonymous_id=b9050503-b549-4117-af17-cac10db592f1; rbuid=rbos-61bd9993-7bb9-479b-a120-f59e7774fe7c; stockx_seen_ask_new_info=true; __lt__cid=10d40d29-894a-4333-ba79-89ba26e91495; stockx_device_id=web-410547fe-366d-4695-9c14-ec7bb493c03a; stockx_default_collectibles_size=All; stockx_default_streetwear_size=XL; _gcl_au=1.1.929965137.1650868871; _tt_enable_cookie=1; _ttp=943cb6e4-acfa-4634-ac92-93ef25b9a577; _derived_epik=dj0yJnU9YlJyUXhxZG5sVy1ZdDVXS2p4anhZbGJqWjU1R05Zcncmbj1ud042c3BJT0cwa09SOE5ZRkxqaWJnJm09MSZ0PUFBQUFBR0ozZDQ4JnJtPTEmcnQ9QUFBQUFHSjNkNDg; stockx_default_handbags_size=All; OptanonAlertBoxClosed=2022-05-30T07:00:41.776Z; NA_SAC=dT1odHRwcyUzQSUyRiUyRnN0b2NreC5jb20lMkZidXklMkZuaWtlLWR1bmstbG93LXJhY2VyLWJsdWUtd2hpdGUlM0ZzaXplJTNEMTQlMjZkZWZhdWx0QmlkJTNEdHJ1ZXxyPQ==; _gid=GA1.2.1140692933.1654499259; stockx_default_sneakers_size=All; stockx_selected_currency=USD; _clck=11tpq9c|1|f25|0; QuantumMetricSessionID=8ec698fb4284a7ad892efac38609cc43; stockx_session=1e4e5212-493f-48ca-9fb1-6eb4b24c27f2; stockx_homepage=handbags; stockx_product_visits=458; __cf_bm=rA21_wOyvht3ww6tE1U1scoR3AaKQkiVp.OUl9_DxiM-1654666582-0-AQsjlHGG/Z7ouifxEgbZh21ZqCrSOHryXSyO2ig4Gp7nonNON2Gtnu7eSSjLTE2NtX8wx4fjmnscOWDpwU0hpp0=; _pxff_idp_c=1,s; OptanonConsent=isGpcEnabled=0&datestamp=Wed+Jun+08+2022+10%3A36%3A25+GMT%2B0500+(Pakistan+Standard+Time)&version=6.36.0&isIABGlobal=false&hosts=&consentId=f03f1052-c1ce-4d1a-bbfc-3c958dc4d2c9&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0005%3A1%2CC0004%3A1%2CC0003%3A1&AwaitingReconsent=false&geolocation=PK%3BPB; _gat=1; forterToken=f97714707aaa44c8bda665516444d4dd_1654666585203_8757_UDF43_13ck; _px3=43ff5af2ceadb9c3fb2d6d01b2a1be4a22d6e9f6ef4ff86a4d544055326c111e:6Ic6vf80GL6tCB84QP1utKUYl246BE3AMqezybcVpJWglAmiYXUETmrZYoeFW8uvZUHCZsgJ8HHs8vuMcKmrzw==:1000:FJVQFgTNG94ud9T91fY5SMnNwQpoTVGWnKfsDiuEFYd1q7DfCG8oBIyEbezdcmHeT8hOye1oWLGNBto2jpsFSsPgIAsDLDYz1MilVDjZa9zFzrYUE15jhNkPvPWinRHducVzL7f41XqB9+JfFCjPpOKiVmewPg6oWYsfEVVEOV8h9RrWWgi7pALoqiFEpVRhm1sBPpbFf3Riz3jPQ/F6YjVXQORiWDon12WIyHmRFyY=; _uetsid=5bcced00e56711ecb1b9412aa71c20e6; _uetvid=0f591ae0eec611eb9ff5fdfee065b825; lastRskxRun=1654666589796; IR_9060=1654666591150%7C0%7C1654666591150%7C%7C; IR_PI=124d676f-eec6-11eb-84ad-4f7348310cc7%7C1654752991150; _clsk=11noh3o|1654666592371|5|0|j.clarity.ms/collect; _pxde=135c39b4e9e2c20d7f0f4890957ddc0b2dd0a89e1c55d0e0769f12aec385613f:eyJ0aW1lc3RhbXAiOjE2NTQ2NjY2MDU0MTIsImZfa2IiOjB9; _dd_s=rum=0&expire=1654667525616',
        'dnt': '1',
        'if-none-match': 'W/"4d7-uDYu/KTc1fvaVY0AFnSCdrRNFxU"',
        'referer': 'https://stockx.com/',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        "X-Crawlera-Profile":"pass"
    }
    headers = {
        'Host': 'stockx.com',
        'Connection': 'keep-alive',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
        'sec-ch-ua-mobile': '?0',
        'App-Platform': 'Iron',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'App-Version': '2022.05.22.04',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://stockx.com/buy/nike-dunk-low-racer-blue-white?size=14&defaultBid=true',
        "X-Crawlera-Profile":"pass"
        # 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US,en;q=0.9',
        # 'Cookie':'stockx_device_id=0420c803-759c-4e65-aea0-4255ff491cbd; stockx_session=7b72df45-ec30-4b91-a2a8-a4acd5d3c486; pxcts=77c76a62-ebc8-11ec-a732-63766b486259; _pxvid=77c75f03-ebc8-11ec-a732-63766b486259; _ga=undefined; __pxvid=786173fa-ebc8-11ec-ac1a-0242ac120002; ajs_anonymous_id=61c6c8b8-5730-4ae4-aeb3-ddc9cb54c077; __ssid=ac596e942ac2d7706166fecf1797338; rskxRunCookie=0; rCookie=wlbmhbmv5bihlzer6pv4ial4dzqzdx; rbuid=rbos-90198fa9-287b-44e5-9689-6270bad8753a; _pin_unauth=dWlkPVlURmpNV1psTmpZdE9ESTRNaTAwTVROakxXSmxZakV0WkROa1ltRXhZbVV4TWpsaA; stockx_selected_currency=SGD; stockx_selected_locale=en; language_code=en; stockx_selected_region=SG; stockx_dismiss_modal=true; stockx_dismiss_modal_set=2022-06-14T09%3A58%3A03.261Z; stockx_dismiss_modal_expiration=2023-06-14T09%3A58%3A03.260Z; stockx_preferred_market_activity=sales; stockx_default_sneakers_size=All; stockx_homepage=sneakers; __cf_bm=OloZda.vx_3EuBUUmetulZ4Dua4OnH_PCl70JPC2hAk-1655201479-0-AQKcHlqpuY8ac9dActCoJucZ+IfpR66V5l+2Y1tbc5tWiZBMMxu0wYp8r7pYDjwvc9QYpwkXNu2u53EOCO2b7A4=; stockx_product_visits=2; _pxff_idp_c=1,s; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Jun+14+2022+15%3A11%3A21+GMT%2B0500+(Pakistan+Standard+Time)&version=6.36.0&isIABGlobal=false&hosts=&consentId=60d00bff-a929-4c57-a324-d1b700db881b&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A0%2CC0004%3A0%2CC0005%3A0%2CC0003%3A0&AwaitingReconsent=false; forterToken=bddd440983b6481d9121c3a95761fd51_1655201481105__UDF43_13ck; _px3=e754a73fcc1e50eefecb0a051eb0067b12d196ad39ce9986cd8b918a327a5fd4:RUp382dSczzIyJP2JtPQ5Wl2YncZCJCapoHRgBo3wwSku0lfIxH9hs3NHKvaZGouqEaTxE/67E4/+1p6l1OU5w==:1000:jA6132MynF+dwMqHSP8wQXrmUCiskN5saSXHHyvgWNm1miR2q0ko4V8lTXpaMhNZ+tEvbFenBRQQFYmTKaBTAJo9S8A6PDmDeI9aXlry/wiYUuzdpi4DeyNwboeBCZigfV2G5jVs6JHx5dXH/AJ9kYN3b5Eh77kx65SwET8SmR4alb6pB5gvKUMmjyWYZjst6u1jmKzH7EBZeo/ru7Cdbg==; lastRskxRun=1655201486553; _dd_s=rum=0&expire=1655202392628; _pxde=b6db7aaa3d29356fa5f3846824a8bedf143b0f8d81c046d9d72d932523564355:eyJ0aW1lc3RhbXAiOjE2NTUyMDE0OTI4NDYsImZfa2IiOjB9'
    }
    url=f'https://stockx.com/api/browse?_search={stockx_sku}&resultsPerPage=10&dataType=product&facetsToRetrieve[]=browseVerticals&propsToRetrieve[][]=brand&propsToRetrieve[][]=colorway&propsToRetrieve[][]=media&propsToRetrieve[][]=title&propsToRetrieve[][]=productCategory&propsToRetrieve[][]=shortDescription&propsToRetrieve[][]=styleId&&propsToRetrieve[][]=urlKey'
    if proxy_flag=='Yes':
        try:
            response = requests.get(url, proxies=proxies, verify=certificate, headers = headers_stockx)
            response_json = json.loads(response.text)
        except:
            return JsonResponse({'message':'something went wrong Please try again'},safe=False)
    elif proxy_flag=='No':
        try:
            response_json =json.loads(requests.get(url=f'https://stockx.com/api/browse?_search={stockx_sku}&resultsPerPage=10&dataType=product&facetsToRetrieve[]=browseVerticals&propsToRetrieve[][]=brand&propsToRetrieve[][]=colorway&propsToRetrieve[][]=media&propsToRetrieve[][]=title&propsToRetrieve[][]=productCategory&propsToRetrieve[][]=shortDescription&propsToRetrieve[][]=styleId&&propsToRetrieve[][]=urlKey',headers=headers_stockx).text)
        except:
            return JsonResponse({'message':'something went wrong Please try again'},safe=False)
    else:
        return JsonResponse({'message':'something went wrong Please try again'},safe=False)
                     


    

    try:
        for i in response_json['Products']:
            if i['styleId'] == stockx_sku:            
                url_key = i['urlKey']

        
        if proxy_flag=='Yes':
            url = f'https://stockx.com/api/products/{url_key}?includes=market,360&currency=USD&country={region}'
            try:
                response = requests.get(url, proxies=proxies, verify=certificate, headers = headers_stockx)
                product_json = json.loads(response.text)
            except:
                return JsonResponse({'message':'something went wrong Please try again'},safe=False)

        
        elif proxy_flag=='No':
            try:
                product_json = json.loads(requests.get(f'https://stockx.com/api/products/{url_key}?includes=market,360&currency=USD&country={region}',headers=headers).text)
            except:
                return JsonResponse({'message':'something went wrong Please try again'},safe=False)      


        main_dic = dict()
        main_dic["lowestResellPrice"] = dict()
        main_dic["lowestResellPrice"]['stockX'] = product_json['Product']['market']['lowestAsk']
        # main_dic["lowestResellPrice"]['goat'] = ''
       
        main_dic['resellPrices'] = dict()

        main_dic['resellPrices']['stockX'] = dict()
        # main_dic['resellPrices']['goat'] = dict()

        for children in product_json['Product']['children']:
            if product_json['Product']['children'][children]['market']['lowestAsk']!=0:
                main_dic['resellPrices']['stockX'][product_json['Product']['children'][children]['shoeSize']] = product_json['Product']['children'][children]['market']['lowestAsk']

        


        main_dic['imageLinks'] = []
        try:
            main_dic['_id'] = product_json['Product']['id']
        except:
             main_dic['_id'] = ''
        try:
            main_dic['shoeName'] = product_json['Product']['title']
        except:
            main_dic['shoeName'] = ''
        try:
            main_dic['brand'] = product_json['Product']['brand']
        except:
             main_dic['brand'] = ''


        try:
            main_dic['silhoutte'] = product_json['Product']['shoe']
        except:
             main_dic['silhoutte'] = ''    
        try:
            main_dic['styleID'] = product_json['Product']['styleId']
        except:
             main_dic['styleID'] = ''    
        try:     
            main_dic['make'] = product_json['Product']['shoe']
        except:
            main_dic['make'] = ''

        try:
            main_dic['colorway'] = product_json['Product']['colorway']
        except:
             main_dic['colorway'] =''

        try:
            main_dic['retailPrice'] = product_json['Product']['retailPrice']
        except:
             main_dic['retailPrice'] = ''

        try:
            main_dic['thumbnail'] = product_json['Product']['media']['thumbUrl']
        except:
            main_dic['thumbnail'] =''

        main_dic['releaseDate'] = ''
        main_dic['description'] = ''
        try:
            main_dic['urlKey'] = product_json['Product']['urlKey']
        except:
            main_dic['urlKey'] = ''

        main_dic['resellLink'] = dict()
        try:    
            main_dic['resellLink']['stockX'] = 'https://stockx.com/'+main_dic['urlKey']
        except:
            main_dic['resellLink']['stockX'] = ''

 
 
        return JsonResponse(main_dic,safe=False)

    except Exception as e:
        return JsonResponse(main_dic,safe=False)


@api_view(['GET','PUT','DELETE'])
def goat_details(request,id):
    try:
        value = open('./drinks/proxies.txt','r')
        proxy = value.readlines()
        proxy = [v.strip() for v in proxy]
        value_choice = random.choice(proxy)

        proxies = {
        "http": f"http://{value_choice}",
        "https": f"https://{value_choice}",
        }
        
        goat_sku_split = str(id)
        goat_sku = goat_sku_split.split('_')[0]
        proxy_flag = goat_sku_split.split('_')[1]
    except:
        return JsonResponse({'message':'something went wrong Please try again'},safe=False)    
   
    try:
        
        main_dic = dict()
        main_dic["lowestResellPrice"] = dict()
        
        main_dic["lowestResellPrice"]['goat'] = ''
       
        main_dic['resellPrices'] = dict()

        
        main_dic['resellPrices']['goat'] = dict()

       

        # goat scraping

        headers_goat = {
            'authority': 'ac.cnstrc.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'origin': 'https://www.goat.com',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
            }

        params_goat = {
            'c': 'ciojs-client-2.27.10',
            'key': 'key_XT7bjdbvjgECO5d8',
            'i': '778c546d-41a5-4c0e-b56d-6a3d8de8a6aa',
            's': '4',
            'num_results_per_page': '25',
            '_dt': '1654779233399',
        }
        headers2 = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Origin': 'https://www.goat.com',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
            'content-type': 'application/x-www-form-urlencoded',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            }
         
        if proxy_flag=='Yes':
            try:
                search_json = json.loads(requests.get(f'https://ac.cnstrc.com/search/{goat_sku}', params=params_goat, headers=headers_goat,proxies=proxies).text)
            except:
                return JsonResponse({'message':'something went wrong Please try again'},safe=False)     
        elif proxy_flag=='No':
            try:
                search_json = json.loads(requests.get(f'https://ac.cnstrc.com/search/{goat_sku}', params=params_goat, headers=headers_goat).text)    
            except:
                return JsonResponse({'message':'something went wrong Please try again'},safe=False)
        else:
            return JsonResponse({'message':'something went wrong Please try again'},safe=False)             
        search_id_goat = ''
        retail_price = ''
        try:
            for i in search_json['response']['results']:
                if i['data']['sku'] == goat_sku:
                    search_id_goat = i['data']['id']                
                    main_dic['lowestResellPrice']['goat'] =  i['data']['lowest_price_cents']/100
                    retail_price = i['data']['retail_price_cents']

            data = '{"query":"","facetFilters":["product_template_id:'+search_id_goat+'"],"hitsPerPage":100}'
        except:
            return JsonResponse({'message':'something went wrong Please try again'},safe=False) 

        if proxy_flag=='Yes':
            try:                 
                response_product = json.loads(requests.post('https://2fwotdvm2o-dsn.algolia.net/1/indexes/product_variants_v2/query?x-algolia-agent=Algolia%20for%20JavaScript%20(4.13.1)%3B%20Browser%20(lite)&x-algolia-api-key=ac96de6fef0e02bb95d433d8d5c7038a&x-algolia-application-id=2FWOTDVM2O', headers=headers2, data=data,proxies=proxies).text)
            except:
                return JsonResponse({'message':'something went wrong Please try again'},safe=False)     
        elif proxy_flag=='No':
            try:
                response_product = json.loads(requests.post('https://2fwotdvm2o-dsn.algolia.net/1/indexes/product_variants_v2/query?x-algolia-agent=Algolia%20for%20JavaScript%20(4.13.1)%3B%20Browser%20(lite)&x-algolia-api-key=ac96de6fef0e02bb95d433d8d5c7038a&x-algolia-application-id=2FWOTDVM2O', headers=headers2, data=data).text)
            except:
                return JsonResponse({'message':'something went wrong Please try again'},safe=False)     

        # if proxy_flag:
        #     response_product = json.loads(requests.post('https://2fwotdvm2o-dsn.algolia.net/1/indexes/product_variants_v2/query?x-algolia-agent=Algolia%20for%20JavaScript%20(4.13.1)%3B%20Browser%20(lite)&x-algolia-api-key=ac96de6fef0e02bb95d433d8d5c7038a&x-algolia-application-id=2FWOTDVM2O', headers=headers2, data=data,proxies=proxies).text)
        # else:
        #     response_product = json.loads(requests.post('https://2fwotdvm2o-dsn.algolia.net/1/indexes/product_variants_v2/query?x-algolia-agent=Algolia%20for%20JavaScript%20(4.13.1)%3B%20Browser%20(lite)&x-algolia-api-key=ac96de6fef0e02bb95d433d8d5c7038a&x-algolia-application-id=2FWOTDVM2O', headers=headers2, data=data).text)     
        brand = response_product['hits'][0]['brand_name']
        id_shoe = search_id_goat  
        shoe_name = response_product['hits'][0]['name']  
        silhoutte = response_product['hits'][0]['silhouette']
        make = silhoutte
        styleid = response_product['hits'][0]['sku']                       
        colorway = response_product['hits'][0]['details']
        retail_price = retail_price
        thumb = response_product['hits'][0]['main_display_picture_url']
        slug = response_product['hits'][0]['slug']

        
        try:                            
            for j in response_product['hits']: 
                if ((j['shoe_condition'] == 'new_no_defects') and (j['has_stock'] == True) and(j['box_condition']=='good_condition')):                                                                                    
                    main_dic['resellPrices']['goat'][j['size']] = j['lowest_price_cents_usd'] / 100 

                                
        except:
            return JsonResponse({'message':'try again'})



        main_dic['imageLinks'] = []
        try:
            main_dic['_id'] = id_shoe
        except:
             main_dic['_id'] = ''
        try:
            main_dic['shoeName'] = shoe_name
        except:
            main_dic['shoeName'] = ''
        try:
            main_dic['brand'] = brand
        except:
             main_dic['brand'] = ''


        try:
            main_dic['silhoutte'] = silhoutte
        except:
             main_dic['silhoutte'] = ''    
        try:
            main_dic['styleID'] = styleid
        except:
             main_dic['styleID'] = ''    
        try:     
            main_dic['make'] = make
        except:
            main_dic['make'] = ''

        try:
            main_dic['colorway'] = colorway
        except:
             main_dic['colorway'] =''

        try:
            main_dic['retailPrice'] = retail_price/100
        except:
             main_dic['retailPrice'] = ''

        try:
            main_dic['thumbnail'] = thumb
        except:
            main_dic['thumbnail'] =''

        main_dic['releaseDate'] = ''
        main_dic['description'] = ''
        try:
            main_dic['urlKey'] = slug
        except:
            main_dic['urlKey'] = ''

        main_dic['resellLink'] = dict()
       

        main_dic['resellLink']['goat'] = slug
 
        return JsonResponse(main_dic,safe=False)

    except Exception as e:
        return JsonResponse(main_dic,safe=False)

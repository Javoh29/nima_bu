import aiohttp
from services.uzum.utils import TokenExpiredError, handle_token_expiration
from services.uzum.schema import UzumSearchSchema

# from services.base import BaseService

# class UzumService(BaseService):


class UzumService:
    def __init__(self):
        self.token = "eyJraWQiOiIwcE9oTDBBVXlWSXF1V0w1U29NZTdzcVNhS2FqYzYzV1N5THZYb0ZhWXRNIiwiYWxnIjoiRWREU0EiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJVenVtIElEIiwiaWF0IjoxNzQ3NjQ4OTkyLCJzdWIiOiIwZTFiNzlmMi0zNWE0LTQ0MGMtOWYwOS0yMGFhYjE0NThiZmUiLCJhdWQiOlsidXp1bV9hcHBzIiwibWFya2V0L3dlYiJdLCJldmVudHMiOnt9LCJleHAiOjE3NDc2NzA1OTJ9.S8TSBV5WNKGt9H4jtujKe-2b2MinxhkYHmCGpSGfsr0DIKEpBNe1N6zGlbjMdfqPC3cGMz8cMxz3j2nDuh5wCQ"

    async def refresh_token(self):
        headers = {
            "Authorization": "Bearer",
            "Cookie": "_fbp=fb.1.1739537667739.510661864999872257; _ym_uid=1739537668928522300; _ym_d=1739537668; cf_clearance=L5YSW27UbeFWxWYmLanMtfoAYUBW0Ez6qqkr2VXsb7M-1739537667-1.2.1.1-MuoW_6o4wrzOZHm48Df3l4o7L8PBsSs2rvRrXm3pfvYDetzFFJhqzvkRKJCLXua2LDhDeGqlc78NzkvfE_YEvklrSmQwkqiXepQcVhjSnyf2mav6FXfY7vjqbz7927qaDSZTw_l7Mn93u0yT75.ZO3O0XKrBmUnV7LbXp0rpga8i0jViNR.I2G4qoO7Tl76Eq0s9XHYIqhrOIg8WFpyXgI2ECTeGrwl9zcQe_0qBZdbxexSTTTzYpFNasPsR0e1vdHk6eEmehgI9LwD333hMyFxhHUELdsAobfc341Hfg0A; access_token=eyJraWQiOiIwcE9oTDBBVXlWSXF1V0w1U29NZTdzcVNhS2FqYzYzV1N5THZYb0ZhWXRNIiwiYWxnIjoiRWREU0EiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJVenVtIElEIiwiaWF0IjoxNzQ3NDE4ODU2LCJzdWIiOiIwZTFiNzlmMi0zNWE0LTQ0MGMtOWYwOS0yMGFhYjE0NThiZmUiLCJhdWQiOlsidXp1bV9hcHBzIiwibWFya2V0L3dlYiJdLCJldmVudHMiOnt9LCJleHAiOjE3NDc0NDA0NTZ9.9JeN77D_U2ZQISciSvccwzEKQVULsXMzezYtNI65ceB0eUXRaN_znyVCd4bWLlcGLFqigQAuKlHS6TKwOiSjCw; refresh_token=ia7RolR8A%2FI5e%2BoukgM%2BbVlXWE%2B325h8%2B99TJJ%2FqsL08A3QmVy3fxgcXQ%2BjrLy2YkihwLG2OZfyVs3QVIymqnC7wDWRy2cVsBA7MRyAe2xwqgn8RYQK91t31yGzF8iK6dxsBnHUu%2F4CoT0XBOIPbgP9Dw3GGWUu5nBzomVUxB796ccWWdjd8GZwMk9YBnwFIU7%2FaNuiw9BnlkqdjeFS%2FqNrglblvnf09xVYER0V8lR3hGTNuzDRirYcR3P205DBLmOG7%2BwzFdSvkwNUS67iF3UmHVqIN8mBx%2F7vwVWi%2Bx4o9h7cQC8SsBppZlZcMFxTrOFRwSJHATAx41h1TDJ2N8R33d%2FwXaXpbsClggo6bz1F%2FtxosQNXwXlXEVgr5QAyYKCwxvGdJhgRPNPvtAXunM37JyMoKWS0mMuXcoubfzYPNNbgMfJfDVj7lyFAWT656doSMbzRn7mErgotSkY6DR6Vl5OzDgcxbgb8ZlKBLAT5dFjGLDFTegHF7iCiRa63zu%2ByJ2mVumE2llaiQyUwzOtwFVhLpnG33TzeJcDtcqxGAiaikpiiOlwnTeFEvyQo2tbN93trVCHDF9ESRlBdHpGPGdKsVZoVIBp%2B3qn%2BQhWSeFbSMLBTv%2F9YDRu5x6urEMsZoyt7DrRXAMItoxQl%2BrJUjH1nqzqvFuzHWXgRPdGeP8mvLVdYuR1IJxcOXz1jD8KJ8PB0%3D--Kjm54Q3Fezzck3iE--%2BCssg0EfIrFQAmqNRxoo2w%3D%3D; _gcl_au=1.1.1084367693.1747419104; _gid=GA1.2.1108127043.1747419104; _ga=GA1.1.2123446510.1739537668; _ga_EZ8RKY9S93=GS2.2.s1747419104$o4$g1$t1747419303$j0$l0$h0; _ga_7KCSSWWYYD=GS2.1.s1747419103$o1$g1$t1747419583$j60$l0$h0; _yasc=KOT3aYdP8COsrz5gzkySB2XUoXvMGC8/I3+gEWVJkTkVxZukhrIvmS6G/8VgXigUTF6T; _yasc=RUWqCPOwjm7TCyGFx50awtmj39GcncenLgOjTKyLKgIGaMAWCJIsXREsjF8haII9; access_token=eyJraWQiOiIwcE9oTDBBVXlWSXF1V0w1U29NZTdzcVNhS2FqYzYzV1N5THZYb0ZhWXRNIiwiYWxnIjoiRWREU0EiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJVenVtIElEIiwiaWF0IjoxNzQ3NjQ4OTkyLCJzdWIiOiIwZTFiNzlmMi0zNWE0LTQ0MGMtOWYwOS0yMGFhYjE0NThiZmUiLCJhdWQiOlsidXp1bV9hcHBzIiwibWFya2V0L3dlYiJdLCJldmVudHMiOnt9LCJleHAiOjE3NDc2NzA1OTJ9.S8TSBV5WNKGt9H4jtujKe-2b2MinxhkYHmCGpSGfsr0DIKEpBNe1N6zGlbjMdfqPC3cGMz8cMxz3j2nDuh5wCQ; refresh_token=wSJxLSbaU060tsBjCNLyzJjQXe8%2F0whtPJAJgbskcVyeRN2SqiVxLUYWqplyTOifGlkWrhnXv6zwM9S9k36hulCMn6Z5zNDZhs0zfm1Z%2FcKsysdcGj%2BFryTDlIF%2B2bqw4GkYFmOoFDOHs7%2FqQgXmu5h%2FIrQm12hL4COJREXZOXmuJLip%2BIMMvPAd8eKTPLq3KxjdVL3oLkU%2Bw63K0Ujvcu%2FHXGZdLQBCBNtLwHSnHermOxiE40xHBPrE6CB%2FPZejYxpyu2X%2F8dJDyviazPaXE0BkdC5bwSdh5J5O0k4f5S7ioMZRgfeAloreAZchGP1jWmwvXwtUKxl71HpgX85AF%2FqYNcG6F%2BqqeYrjyzc6AH%2FJw2NCOXMgMYtSCHIro1YW6EaQgCQ9qCTXZU%2Bf%2FhIGo2cyI0knTnFSMO9%2BtKssvcPZlB9591vL%2FYDWDqjzptVjvh1hKAamr6vWCcSr%2FhK%2F7whlCQVxVTse40VuTLEFpSQ7%2Fepizigj36BHP46UIzBqksFNYAXgvCZBpvzZR5sUJWdQO%2FtV2Nxq0g%2F3ZxiExDZvFA66eHZk%2Bn4PtAaHNADsqZzq4%2F%2BDhc%2BV4UtFIt3%2FBOPePfMkChVuZk%2BDorG%2FLInvKmgcbz2QHcU%2BXjKMmEU8IUvcSoNjOpbDlzjszxFYLdH69b0MvO0mS3Mgdzxe20rDoGzCm4oCZYMHr1FLW0501%2F%2FkIpo%3D--3iAfMKCDZeUh6F%2Bb--3yjFsu0vwdmPmTuQ510aew%3D%3D",
            "Accept-Language": "uz",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
            "Content-Type": "application/json",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "sec-ch-ua": '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "Host": "id.uzum.uz",
            "Origin": "https://uzum.uz",
            "Referer": "https://uzum.uz/",
            "Accept": "*/*",
        }
        url = "https://id.uzum.uz/api/auth/token"
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers) as response:
                cookie = response.cookies
                self.token = cookie.get("access_token").value

    @handle_token_expiration
    async def search(self, text: str, offset: int = 0, limit: int = 3):
        url = "https://graphql.uzum.uz/"
        headers = {
            "accept": "*/*",
            "accept-language": "uz-UZ",
            "apollographql-client-name": "web-customers",
            "apollographql-client-version": "1.48.1",
            "authorization": f"Bearer {self.token}",
            "baggage": "sentry-environment=production,sentry-release=uzum-market%401.48.1,sentry-public_key=948fdc05a99a018e8d3ab003bee4b5a3,sentry-trace_id=5377fdbeace54306a3862111def5261e,sentry-sample_rate=0.01,sentry-transaction=search,sentry-sampled=false",
            "content-type": "application/json",
            "origin": "https://uzum.uz",
            "priority": "u=1, i",
            "referer": "https://uzum.uz/",
            "sec-ch-ua": '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "sentry-trace": "5377fdbeace54306a3862111def5261e-8f3934428d376a40-0",
            "test-header": "test-header-value-apollo",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
            "x-iid": "049f4997-c022-4091-a9c1-50d67e9e022e",
            "Cookie": "_yasc=RUWqCPOwjm7TCyGFx50awtmj39GcncenLgOjTKyLKgIGaMAWCJIsXREsjF8haII9; access_token=eyJraWQiOiIwcE9oTDBBVXlWSXF1V0w1U29NZTdzcVNhS2FqYzYzV1N5THZYb0ZhWXRNIiwiYWxnIjoiRWREU0EiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJVenVtIElEIiwiaWF0IjoxNzQ3NjQ4OTkyLCJzdWIiOiIwZTFiNzlmMi0zNWE0LTQ0MGMtOWYwOS0yMGFhYjE0NThiZmUiLCJhdWQiOlsidXp1bV9hcHBzIiwibWFya2V0L3dlYiJdLCJldmVudHMiOnt9LCJleHAiOjE3NDc2NzA1OTJ9.S8TSBV5WNKGt9H4jtujKe-2b2MinxhkYHmCGpSGfsr0DIKEpBNe1N6zGlbjMdfqPC3cGMz8cMxz3j2nDuh5wCQ; _yasc=U5n74SQh1UlubfkLTjt7oN5MuAkHAVhXV34s14gyXBb0eK7zSQPDQel2LWdlHT4k; route=1747648073.51.838.190374|f28b5fe4c5802f4f3e68b73a841acf3b",
        }

        payload = {
            "query": """
            query getMakeSearch($queryInput: MakeSearchQueryInput!) {
              makeSearch(query: $queryInput) {
                total
                items {
                  catalogCard {
                    ...SkuGroupCardFragment
                  }
                }
              }
            }

            fragment SkuGroupCardFragment on SkuGroupCard {
              ...DefaultCardFragment
              photos {
                link(trans: PRODUCT_540){ high }
              }
            }

            fragment DefaultCardFragment on CatalogCard {
              minFullPrice
              minSellPrice
              id: productId
              title
            }
            """,
            "variables": {
                "queryInput": {
                    "text": text,
                    "showAdultContent": "NONE",
                    "filters": [],
                    "sort": "BY_RELEVANCE_DESC",
                    "pagination": {"offset": offset, "limit": limit},
                    "correctQuery": False,
                    "getFastCategories": False,
                    "fastCategoriesLimit": 11,
                    "fastCategoriesLevelOffset": 2,
                    "getPromotionItems": True,
                    "getFastFacets": False,
                    "fastFacetsLimit": 0,
                }
            },
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                if response.status == 401:
                    raise TokenExpiredError
                try:
                    json = await response.json()
                    data = UzumSearchSchema.model_validate(json)
                    return data.to_main_schema(offset=offset, limit=limit)
                except Exception as e:
                    print(e)
                    return



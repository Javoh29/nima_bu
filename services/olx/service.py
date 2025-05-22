import asyncio
import aiohttp
from services.base import BaseService
from services.olx.schema import OlxSearchSchema


class OlxService(BaseService):

    async def search(self, text: str, offset: int = 0, limit: int = 3) -> dict:
        url = "https://www.olx.uz/apigateway/graphql"
        headers = {"Content-Type": "application/json"}

        payload = {
            "query": """
            query ListingSearchQuery($searchParameters: [SearchParameter!]) {
                clientCompatibleListings(searchParameters: $searchParameters) {
                    ... on ListingSuccess {
                    items: data {
                        id
                        photos {
                        link
                        height
                        width
                        }
                        title
                        url
                        params {
                        key
                        name
                        value {
                            ... on PriceParam {
                            value
                            previous_value
                            converted_value
                            converted_previous_value
                            converted_currency
                            }
                        }
                        }
                    }
                    metadata {
                        total_elements
                        visible_total_count
                    }
                    }
                    ... on ListingError {
                    error {
                        code
                        detail
                        status
                        title
                        validation {
                        detail
                        field
                        title
                        }
                    }
                    }
                }
                }

            """,
            "variables": {
                "searchParameters": [
                    {"key": "offset", "value": str(offset)},
                    {"key": "limit", "value": str(limit)},
                    {"key": "query", "value": text},
                    {"key": "suggest_filters", "value": "true"},
                    {"key": "sl", "value": "196da442f38x7e3c9731"},
                ]
            },
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                try:
                    json = await response.json()
                    data = OlxSearchSchema.model_validate(json)
                    return data.to_main_schema(offset=offset, limit=limit)
                except Exception as e:
                    print(e)
                    return

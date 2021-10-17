from typing import Union


class Providers:
    APIS_NINJA_AIR_QUALITY = 'APIS_NINJA_AIR_QUALITY'
    EMISSIONS_API = 'EMISSIONS_API'
    BLOOWATCH = 'BLOOWATCH'
    AIRCHECKER_CITY = 'AIRCHECKER_CITY'
    AMBEE_BY_CITY = 'AMBEE'

    EMISSIONS_PROVIDERS = [EMISSIONS_API, APIS_NINJA_AIR_QUALITY]
    CITY_DATA_PROVIDERS = [APIS_NINJA_AIR_QUALITY, AMBEE_BY_CITY, AIRCHECKER_CITY]


class APIsURLs:
    _map = {
        Providers.EMISSIONS_API: 'https://api.v2.emissions-api.org/api/v2/{data_type}/statistics.json',
        Providers.APIS_NINJA_AIR_QUALITY: 'https://api.api-ninjas.com/v1/airquality',
        Providers.BLOOWATCH: 'http://bloowatch.org/developers/json/species/',
        Providers.AMBEE_BY_CITY: 'https://api.ambeedata.com/latest/by-city',
        Providers.AIRCHECKER_CITY: ''
    }

    @classmethod
    def _get_url(cls, key):
        try:
            return cls._map[key]
        except KeyError:
            raise KeyError(f'the provided key: {key} was not found on the urls map, are you sure its there?')

    @classmethod
    def get_urls(cls, provider_or_providers: Union[str, list]):
        """
        is a string is provided returns the url for this key
        if a list, returns a list of those urls
        """
        if isinstance(provider_or_providers, str):
            return cls._get_url(provider_or_providers)
        else:
            return [
                cls._get_url(provider) for provider in provider_or_providers
            ]

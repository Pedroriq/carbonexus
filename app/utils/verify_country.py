import pycountry


def get_zone_code(country_name):
    try:
        return pycountry.countries.lookup(country_name).alpha_2
    except LookupError:
        print(f"Please, use a valid country. {country_name} not found")
        return None
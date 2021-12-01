def list_countries(cursor):
    cursor.execute("SELECT * from public.countries ORDER BY country_code ASC")
    elements = cursor.fetchall()
    colnames = [desc[0] for desc in cursor.description]
    results = []
    for element in elements:
        el_dict = dict(zip(colnames, element))
        results.append(el_dict)
    return results

def list_subCountries(cursor, countryCode):
    cursor.execute(f"SELECT * from public.countries_subdivisions WHERE country_code='{countryCode}' ORDER BY id_subdivision ASC ")
    elements = cursor.fetchall()
    colnames = [desc[0] for desc in cursor.description]
    results = []
    for element in elements:
        el_dict = dict(zip(colnames, element))
        results.append(el_dict)
    return results
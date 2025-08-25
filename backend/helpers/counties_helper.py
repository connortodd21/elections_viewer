from string import capwords


def capitalizeCountyName(county_name: str) -> str:
    """
    Most county names can be properly capitzlaied (only the first letter in each word capitalized) using string.capwords()

    There exists a few (10) counties which have either an apostrophe (') or a dash (-). string.capwords() does not
    work for those counties. This method ensures these special cases are handled.

    There are 4 counties with a ':
        O'Brien,IA
        Prince George's,MD
        Queen Anne's,MD
        St. Mary's,MD
    for O'Brien,IA, we can use capwords() with an '. 
    for the others, we can use capwords normally

    There are 6 counties with a -
        Hoonah-Angoon,AK
        Matanuska-Susitna,AK
        Prince of Wales-Hyder
        Valdez-Cordova,AK
        Yukon-Koyukuk,AK
        Miami-Dade,FL
    for Prince of Wales-Hyde, capwords won't work, we need custom handling
    for the others, we can use capwords() with a -
    """
    if "-" in county_name:
        if county_name.upper() == "PRINCE OF WALES-HYDER":
            return "Prince of Wales-Hyder"
        else:
            return capwords(county_name, "-")
    elif county_name == "O'Brien":
        return capwords(county_name, "'")
    else:
        return capwords(county_name)
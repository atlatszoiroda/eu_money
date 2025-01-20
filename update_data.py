import requests
import pandas as pd

FIRST_RUN = False


# Define the translation table
trans_table = str.maketrans({
    'á': 'a',
    'é': 'e',
    'í': 'i',
    'ó': 'o',
    'ö': 'o',
    'ő': 'o',
    'ú': 'u',
    'ü': 'u',
    'ű': 'u',
})

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'hu-HU,hu;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://archive.palyazat.gov.hu',
    'priority': 'u=1, i',
    'referer': 'https://archive.palyazat.gov.hu/',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
}



n_rows = 500000

def clean_special_characters(text):
# Különböző nem kívánt karakterek eltávolítása
# Ha csak a szövegből nem alfanumerikus karaktereket szeretnél eltávolítani
    if text:
        cleaned_text = ''.join(e for e in text if e.isalnum() or e.isspace())
        return cleaned_text

def get_one_projet(program_name):
    print(program_name)
    json_data = {
        'filter': {
            'where': {
                'fejlesztesi_program_nev': program_name,
            },
            'skip': '0',
            'limit': n_rows, # 9920
            'order': 'konstrukcio_kod desc',
        },
    }

    response = requests.post('https://ginapp-api.fair.gov.hu/api/tamogatott_proj_kereso/find2', headers=headers, json=json_data)
    t = response.json()
    print(len(t))
    return(t)



if FIRST_RUN:
    all_data = []
    program_names = ['Széchenyi terv plusz', 'RRF Végrehajtás', 'Széchenyi 2020', 'KTIA', 'Széchenyi 2020 Pénzügyi eszközök', 'NFT', 'EU 2007-2013', 'Széchenyi 2020 VP', 'Brexitkár-enyhítő Beruházás Támogatási Terv' ]

    for program_name in program_names:
        t = get_one_projet(program_name)
        all_data.extend(t)

    all_data = pd.DataFrame(all_data)
    # clean city data
    all_data.loc[all_data["megval_megye_nev"] == "Csongrád", "megval_megye_nev"] = "Csongrád-Csanád"
    all_data.loc[all_data["kisterseg_nev"] == "Derecske-Létavértesi", "kisterseg_nev"] = "Derecske-Létavérte"
    all_data.loc[all_data["kisterseg_nev"] == "Őriszentpéteri", "kisterseg_nev"] = "őriszentpéteri"
    all_data['helyseg_nev_join'] = all_data['helyseg_nev'].str.split('(').str[0].str.strip()
    all_data['helyseg_nev_join'] = all_data['helyseg_nev_join'].str.split(',').str[0].str.strip()
    all_data['helyseg_nev_join'] = all_data['helyseg_nev_join'].str.split('-').str[0].str.strip()

    # Apply the translation table to the 'helyseg_nev' column
    all_data['helyseg_nev_join'] = all_data['helyseg_nev_join'].str.translate(trans_table)
    all_data['helyseg_nev_join'] = all_data['helyseg_nev_join'].str.title()


    all_data.to_parquet('all_eu_money.parquet')


    # Apply the function to the 'sheet_names' column
    all_data['konstrukcio_nev'] = all_data['konstrukcio_nev'].apply(clean_special_characters)
    all_data['palyazo_neve'] = all_data['palyazo_neve'].apply(clean_special_characters)
    all_data['projekt_cime'] = all_data['projekt_cime'].apply(clean_special_characters)
    all_data['megval_regio_nev'] = all_data['megval_regio_nev'].apply(clean_special_characters)
    all_data.to_excel('all_eu_money.xlsx', index=False)


else:
    new_data = []

    # all_data = pd.read_parquet('all_eu_money.parquet')
    all_data = pd.read_parquet('all_eu_money.parquet')

    program_names = ['Széchenyi terv plusz', 'RRF Végrehajtás', 'Széchenyi 2020' ]

    for program_name in program_names:
        t = get_one_projet(program_name)
        new_data.extend(t)

    new_data = pd.DataFrame(new_data)

    # select new data based on id_palyazat
    true_new_data = new_data[~new_data['id_palyazat'].isin(all_data['id_palyazat'])]

    # rbind
    all_data = pd.concat([all_data, true_new_data])
    # reset index
    all_data = all_data.reset_index(drop=True)

    # clean city data
    all_data.loc[all_data["megval_megye_nev"] == "Csongrád", "megval_megye_nev"] = "Csongrád-Csanád"
    all_data.loc[all_data["kisterseg_nev"] == "Derecske-Létavértesi", "kisterseg_nev"] = "Derecske-Létavérte"
    all_data.loc[all_data["kisterseg_nev"] == "Őriszentpéteri", "kisterseg_nev"] = "őriszentpéteri"
    all_data['helyseg_nev_join'] = all_data['helyseg_nev'].str.split('(').str[0].str.strip()
    all_data['helyseg_nev_join'] = all_data['helyseg_nev_join'].str.split(',').str[0].str.strip()
    all_data['helyseg_nev_join'] = all_data['helyseg_nev_join'].str.split('-').str[0].str.strip()

    # Apply the translation table to the 'helyseg_nev' column
    all_data['helyseg_nev_join'] = all_data['helyseg_nev_join'].str.translate(trans_table)
    all_data['helyseg_nev_join'] = all_data['helyseg_nev_join'].str.title()




    all_data.to_parquet('all_eu_money.parquet')

    # Apply the function to the 'sheet_names' column
    all_data['konstrukcio_nev'] = all_data['konstrukcio_nev'].apply(clean_special_characters)
    all_data['palyazo_neve'] = all_data['palyazo_neve'].apply(clean_special_characters)
    all_data['projekt_cime'] = all_data['projekt_cime'].apply(clean_special_characters)
    all_data['megval_regio_nev'] = all_data['megval_regio_nev'].apply(clean_special_characters)
    all_data.to_excel('all_eu_money.xlsx', index=False)






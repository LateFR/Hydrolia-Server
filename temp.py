import requests
import csv

def compute_tva(siren: str) -> str:
    """
    Calcule le numéro de TVA intracommunautaire à partir d'un SIREN.
    La formule est : TVA = "FR" + clé à 2 chiffres + SIREN,
    où la clé est calculée par : clé = (12 + 3*(int(SIREN) mod 97)) mod 97.
    """
    siren_int = int(siren)
    key = (12 + 3 * (siren_int % 97)) % 97
    key_str = f"{key:02d}"
    return f"FR{key_str}{siren}"

def search_company(company_name: str, api_token: str):
    """
    Recherche une entreprise par nom via l'API Sirene.
    Cette fonction renvoie le premier établissement trouvé.
    """
    url = "https://api.insee.fr/entreprises/sirene/V3/etablissements"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Accept": "application/json"
    }
    # Le paramètre "q" permet de faire une recherche par nom
    params = {
        "q": company_name,
        "nombre": 1  # On limite la réponse à 1 résultat
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print("Erreur lors de la requête :", response.status_code, response.text)
        return None

    data = response.json()
    # On suppose que la réponse contient une liste d'établissements dans "etablissements"
    if "etablissements" in data and len(data["etablissements"]) > 0:
        return data["etablissements"][0]
    else:
        return None

def save_to_csv(data: dict, csv_filename: str):
    """
    Enregistre les informations de l'entreprise dans un fichier CSV.
    """
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["Nom", "SIRET", "TVA"])
        writer.writeheader()
        writer.writerow(data)

def main():
    company_name = input("Entrez le nom de l'entreprise : ")
    api_token = "VOTRE_API_TOKEN_ICI"  # Remplacez par votre token valide pour l'API Sirene
    result = search_company(company_name, api_token)
    if result:
        siret = result.get("siret")
        if siret and len(siret) >= 9:
            # Le SIREN est constitué des 9 premiers chiffres du SIRET
            siren = siret[:9]
            tva = compute_tva(siren)
        else:
            tva = "Non disponible"
        company_info = {
            "Nom": company_name,
            "SIRET": siret,
            "TVA": tva
        }
        print("Données récupérées :", company_info)
        save_to_csv(company_info, "entreprise.csv")
        print("Les informations ont été sauvegardées dans 'entreprise.csv'.")
    else:
        print("Aucun résultat trouvé pour l'entreprise.")

if __name__ == "__main__":
    main()

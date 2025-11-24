import sys
import requests
from bs4 import BeautifulSoup
import csv
from typing import List, Tuple


def get_soup(url: str) -> BeautifulSoup:
    """Stáhne a vrátí obsah stránky jako BeautifulSoup objekt."""
    resp = requests.get(url)
    resp.raise_for_status()
    return BeautifulSoup(resp.content, "html.parser")


def parse_municipalities(soup: BeautifulSoup) -> List[Tuple[str, str]]:
    """Z detailní stránky územního celku vrátí seznam obcí s jejich odkazy."""
    tables = soup.find_all("table", {"class": "table"})
    municipal_table = tables[1] if len(tables) > 1 else tables[0]
    municipalities = []
    for row in municipal_table.find_all("tr")[1:]:
        cols = row.find_all("td")
        if len(cols) > 1:
            link_tag = cols[0].find("a")
            if link_tag:
                name = cols[1].get_text(strip=True)
                link = link_tag["href"]
                municipalities.append((name, link))
    return municipalities


def parse_results_table(soup: BeautifulSoup) -> Tuple[List[str], List[List[str]]]:
    """Parsuji výsledky hlasování v tabulce, vrátí hlavičku a seznam řádků."""
    table = soup.find("table", {"class": "table"})
    if table is None:
        return [], []
    header_cells = [th.get_text(strip=True) for th in table.find("tr").find_all("th")]
    rows = []
    for row in table.find_all("tr")[1:]:
        cells = [td.get_text(strip=True) for td in row.find_all("td")]
        if cells:
            rows.append(cells)
    return header_cells, rows


def extract_vote_data(results_header: List[str], results_rows: List[List[str]]) -> List[List[str]]:
    """Extrahuju sloupce: kód, název, voliči, obálky, platné hlasy, hlasy pro strany."""
    result = []
    for row in results_rows:
        data = row[:5]  # kód, název, voliči, vydané obálky, platné hlasy
        data.extend(row[5:])  # hlasy pro kandidující strany
        result.append(data)
    return result


def save_to_csv(header: List[str], rows: List[List[str]], filename: str) -> None:
    """Uloží data do CSV souboru s daným jménem."""
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def main() -> int:
    """Hlavní funkce - načte argumenty, stáhne a uloží výsledky."""
    if len(sys.argv) != 3:
        print("Použití: python main.py <URL územního celku> <výstupní soubor.csv>")
        return 1

    url = sys.argv[1]
    output_file = sys.argv[2]

    if not (url.startswith("https://volby.cz/pls/ps2017nss/ps32") or
            url.startswith("https://www.volby.cz/pls/ps2017nss/ps32")):
        print("Neplatný URL odkaz na územní celek.")
        return 1

    try:
        soup = get_soup(url)
        municipalities = parse_municipalities(soup)

        results = []
        header_saved = False

        for municipality_name, link in municipalities:
            full_url = "https://volby.cz" + link
            try:
                soup_munic = get_soup(full_url)
                header, rows = parse_results_table(soup_munic)
                if not header_saved:
                    save_header = ["Kód obce", "Název obce", "Voliči v seznamu", "Vydané obálky", "Platné hlasy"] + header[5:]
                    header_saved = True
                data = extract_vote_data(header, rows)
                results.extend(data)
            except Exception as e:
                print(f"Chyba při stahování {municipality_name}: {e}")

        save_to_csv(save_header, results, output_file)
        print(f"Data uložena do souboru {output_file}")

    except Exception as e:
        print("Chyba při stahování dat:", e)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())

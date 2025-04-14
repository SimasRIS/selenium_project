# Selenium project

### Užduotis:
Variantas Surinkti klientų atsiliepimus apie kinų restoranus iš svetainių (pvz., „TripAdvisor“, „Google Reviews“),
išanalizuoti ir vizualizuoti atsiliepimų turinį ir reitingus, bei suskirstyti restoranus ar apžvalgas į grupes naudojant klasterizavimo algoritmus (KMeans, DBSCAN).

### Reikalavimai:

1. Bibliotekos
    pandas – struktūrizuotų duomenų analizė
    bs4 (BeautifulSoup) – HTML apžvalgų nuskaitymas
    matplotlib – duomenų vizualizavimas
    sklearn – klasterizacijos metodai (KMeans, DBSCAN).

2. Funkcionalumas

    Duomenų surinkimas(<5000 duomenų)
        Naudoti BeautifulSoup norint išgauti restoranų pavadinimus, klientų atsiliepimus (tekstas), reitingus, datas iš apžvalgų puslapių.

    Duomenų analizė su pandas
        Struktūrizuoti duomenis į lentelę su stulpeliais:
        Restorano pavadinimas
        Atsiliepimo tekstas
        Reitingas (1–5)
        Data
        Pašalinti pasikartojančius ar nereikalingus įrašus.

    Vizualizacijos su matplotlib
        Rodyti reitingų pasiskirstymą (histograma arba bar diagrama).
        Rodyti dažniausiai vartojamus žodžius atsiliepimuose.
        Atsiliepimų kiekio pasiskirstymas pagal datas.

3. Grupavimas su KMeans arba DBSCAN
        Pritaikyti KMeans arba DBSCAN:
        Grupavimas pagal atsiliepimų turinį (temos).
        Grupavimas pagal reitingus ir teksto emocijas.
        Vizualizuoti klasterius (pvz., PCA plokštumoje).
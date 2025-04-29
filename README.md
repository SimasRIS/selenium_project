# Selenium project

### Užduotis:
Variantas Surinkti klientų atsiliepimus apie kinų restoranus iš svetainių (pvz., „TripAdvisor“, „Google Reviews“),
išanalizuoti ir vizualizuoti atsiliepimų turinį ir reitingus, bei suskirstyti restoranus ar apžvalgas į grupes naudojant klasterizavimo algoritmus (KMeans, DBSCAN).

---

### Reikalavimai:

1. Bibliotekos
    pandas – struktūrizuotų duomenų analizė.
    bs4 (BeautifulSoup) – HTML apžvalgų nuskaitymas.
    matplotlib – duomenų vizualizavimas.
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
---
# Restoranų atsiliepimų analizės projektas

## Turinys

1. Projekto apžvalga
2. Diegimo ir paleidimo instrukcijos
3. Programos meniu
4. Vizualizacijos ir įžvalgos
5. Duomenų grupavimas

---

## Diegimo ir paleidimo instrukcijos

```bash
# 1 — Klonuokite saugyklą
$ git clone https://github.com/SimasRIS/selenium_project.git
$ cd kinu_restoranai

# 2 — (Rekomenduojama) Sukurkite virtualią aplinką
$ python -m venv venv
# Windows
$ venv\Scripts\activate
# macOS/Linux
$ source venv/bin/activate

# 3 — Įdiekite priklausomybes
$ pip install -r requirements.txt

# 4 — Paleiskite programą
$ python main.py
```

## Programos naudojimas

Paleidus `main.py`, terminale matysite šias parinktis:

1. Restoranų URL nuskaitymas
2. Atsiliepimų nuskaitymas
3. Duomenų valymas
4. Visualizacijos
5. Klasterizavimas
6. Išeiti

Pasirinkite norimą veiksmą įvesdami atitinkamą skaičių.

---

## Projekto apžvalga

Šis projektas automatiškai surenka, apdoroja ir analizuoja kinų restoranų atsiliepimus iš **Google Maps**. Pagrindinės funkcijos:

- Restoranų URL paieška ir išsaugojimas (`web_page_extraction.py`)
- Atsiliepimų nuskaitymas (`comments_extraction.py`)
- Duomenų valymas (`review_comments_cleaning.py`)
- Vizualizacijos (`visualisation.py`)
- Klasterizavimas DBSCAN algoritmu (`clusters.py`)

Projekto tikslas – išanalizuoti, kaip klientai vertina kinų restoranus skirtinguose Lietuvos miestuose ir nustatyti dažniausiai pasikartojančius žodžius atsiliepimų turinyje.

---

## Vizualizacijos ir įžvalgos

Čia aprašyta, kokius grafikus programa sukuria ir ką iš jų galime sužinoti.

### 1. Restoranų įvertinimų diagrama

**Failas:** `visualisation.py` | **Funkcija:** `reiting_destribution()`

- **Ką matome:** Grafikas rodo, kiek restoranai gavo kokių įvertinimų. Kairėje pusėje matome įvertinimų skaičių, o apačioje - žvaigždučių skaičių nuo 1 iki 5.
- **Ką tai reiškia:** Dauguma žmonių restoranams davė gerus įvertinimus (4-5 žvaigždutes). Mažai kas įvertino prastai (1-2 žvaigždutėmis), ir iš to galime lengvai pamatyti, kiek yra nepatenkintų klientų.

### 2. Žodžių dažnumo diagrama

**Failas:** `visualisation.py` | **Funkcija:** `most_used_words()`

- Matome stulpelinę diagramą, kuri parodo 10 žodžių, kuriuos klientai dažniausiai mini savo atsiliepimuose. Programa automatiškai pašalina įprastus lietuviškus žodžius (pavyzdžiui, "ir", "bet", "kad").
- Ši diagrama greitai parodo, ką klientai dažniausiai mini apie restoraną. Pavyzdžiui, jei dažnai kartojasi teigiami žodžiai kaip "skanu" ar "greita", žinome, kad klientai patenkinti. Jei matome daug neigiamų žodžių, kaip "brangu" ar "lėta", tai rodo restorano silpnąsias vietas.

### 3. Žodžių debesies (Word Cloud) vizualizacija

**Failas:** `visualisation.py` | **Funkcija:** `generate_wordcloud()`

- **Kas rodoma:** Sistema sukuria žodžių debesį, kuriame dažniau naudojami žodžiai rodomi didesniu šriftu.
- **Įžvalgos:** Žodžių debesis leidžia greitai pamatyti, apie ką žmonės dažniausiai kalba savo atsiliepimuose - tiek geras, tiek blogas puses.

### 4. Atsiliepimų kiekio kitimas laike

**Failas :** `visualisation.py`   |  **Funkcija :** `review_count_by_date()`

- **Kas rodoma :** Linijinė diagrama, rodanti kiek atsiliepimų palikta kiekvieną datą.
- **Įžvalgos :** Aiškūs pikai gali sutapti su šventėmis ar akcijomis, kai restoranai sulaukia daugiau lankytojų. Staigus kritimas – potencialus ženklas techniniam ar reputaciniam incidentui.

---

## Duomenų grupavimas

Programa naudoja **DBSCAN** metodą duomenims grupuoti - tai padeda atrasti panašius atsiliepimus. Visi rezultatai automatiškai išsaugomi ir parodomi grafikuose, naudojant `clusters.py` programos dalį.

### 5. Atsiliepimų grupavimas pagal turinį

**Failas:** `clusters.py` | **Pirma dalis**

- **Ką matome:** Grafikas, kuris parodo, kaip atsiliepimai susiskirsto į grupes. Kiekvienas taškas reiškia vieną atsiliepimą, o skirtingos spalvos rodo skirtingas grupes.
- **Ką tai reiškia:** Programa sugrupuoja panašius atsiliepimus. Pavyzdžiui, vienoje grupėje gali būti atsiliepimai apie maistą, kitoje - apie aptarnavimą ar kainas. Pavieniai taškai dažniausiai reiškia ypatingus ar neįprastus atsitikimus.

### 6. Atsiliepimų grupavimas pagal įvertinimus ir turinį

**Failas:** `clusters.py` | **Antra dalis**

- **Ką matome:** Grafikas, kuris rodo, kaip atsiliepimai pasiskirsto pagal jų turinį ir žvaigždučių skaičių.
- **Ką tai reiškia:** Grafike aiškiai matosi, kurie atsiliepimai yra teigiami (su daug žvaigždučių), o kurie neigiami (su mažai žvaigždučių). Tai padeda suprasti, kokios problemos labiausiai mažina restorano įvertinimus.
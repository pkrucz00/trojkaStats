# trojkaStats
Analizyng data from polish oldest music chart - "Lista Przebojów Trójki". Made with R language and ggplot2

## Wybrane pliki
`lp3WebScratch.py` - program that "scraps" data from site "https://www.lp3.pl/" (site with all the chart data) and saving it to `data.csv` with UNICODE
`listaPrzebojowTrojki.db` - database with table consisting of chart records; converted from `data.csv` to table in the database with SQLite
`Analiza Listy Przebojów Trójki.ipynb` - notebook with main analysis of the content of `listaPrzebojowTrojki.db`, that is - the "Trójka" chart

folder `pdfy` - pdf files exported from the notebook, made with LaTeX

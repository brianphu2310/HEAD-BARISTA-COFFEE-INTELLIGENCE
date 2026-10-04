# Last live ingestion run (brewing methods)

Written by the workflow `live-ingestion.yml` on a GitHub-hosted runner. Run: https://github.com/brianphu2310/HEAD-BARISTA-COFFEE-INTELLIGENCE/actions/runs/37233338557

- Run at (UTC): 2026-10-04T20:46:29Z
- `data/raw/brewing_healthline.csv`: 3 rows
- `data/raw/brewing_nca.csv`: 5 rows
- `data/raw/brewing_wikipedia.csv`: 13 rows

## First rows

`data/raw/brewing_healthline.csv`
```
source,source_url,scraped_at,drink_name,caffeine_range_text,caffeine_avg_mg
Healthline,https://www.healthline.com/nutrition/how-much-caffeine-in-coffee,2026-10-04T20:46:19+00:00,tall/small,260 mg,260
Healthline,https://www.healthline.com/nutrition/how-much-caffeine-in-coffee,2026-10-04T20:46:19+00:00,grande/medium,330 mg,330
Healthline,https://www.healthline.com/nutrition/how-much-caffeine-in-coffee,2026-10-04T20:46:19+00:00,venti/large,410 mg,410
```

`data/raw/brewing_nca.csv`
```
source,source_url,scraped_at,method_section,guide_snippet
National Coffee Association,https://www.ncausa.org/About-Coffee/Brewing-Methods,2026-10-04T20:46:29+00:00,Drip coffee,
National Coffee Association,https://www.ncausa.org/About-Coffee/Brewing-Methods,2026-10-04T20:46:29+00:00,Pour over coffee,
National Coffee Association,https://www.ncausa.org/About-Coffee/Brewing-Methods,2026-10-04T20:46:29+00:00,Espresso,
National Coffee Association,https://www.ncausa.org/About-Coffee/Brewing-Methods,2026-10-04T20:46:29+00:00,French press coffee,
National Coffee Association,https://www.ncausa.org/About-Coffee/Brewing-Methods,2026-10-04T20:46:29+00:00,Cold brew coffee,
```

`data/raw/brewing_wikipedia.csv`
```
source,source_url,scraped_at,method,description,brew_time_scraped,caffeine_scraped_mg
Wikipedia,https://en.wikipedia.org/wiki/Espresso,2026-10-04T20:45:53+00:00,Espresso,"Espresso /ɛˈsprɛsoʊ/ ⓘ, Italian: eˈsprɛsso is a concentrated form of coffee produced by forcing hot water under high pressure through finely ground
Wikipedia,https://en.wikipedia.org/wiki/Ristretto,2026-10-04T20:45:54+00:00,Ristretto,"Ristretto Italian: risˈtretto,1 known in full in Italian as caffè ristretto, is a ""short shot"" of a highly concentrated espresso, 20 ml 0.7 imp fl oz
Wikipedia,https://en.wikipedia.org/wiki/Lungo,2026-10-04T20:45:56+00:00,Lungo,"Lungo lit. 'long', known in full in Italian as caffè lungo, is a coffee made by using an espresso machine to make an Italian-style coffee—short black a single
Wikipedia,https://en.wikipedia.org/wiki/AeroPress,2026-10-04T20:45:58+00:00,AeroPress,"The AeroPress is a manual coffeemaker invented by Alan Adler, founder of AeroPress, Inc. formerly Aerobie Inc.. It consists of a cylindrical brewing cham
Wikipedia,https://en.wikipedia.org/wiki/Moka_pot,2026-10-04T20:46:01+00:00,Moka Pot,"The moka pot12 is a stove-top or electric coffee maker that brews coffee by passing hot water driven by vapor pressure and heat-driven gas expansion throug
```

## Run log (tail)
```
2026-10-04 20:46:12,989 INFO ingestion.fetch: cache hit https://en.wikipedia.org/wiki/Cold_brew_coffee
2026-10-04 20:46:15,057 DEBUG urllib3.connectionpool: https://en.wikipedia.org:443 "GET /wiki/Drip_coffee_maker HTTP/1.1" 200 None
2026-10-04 20:46:15,065 INFO ingestion.fetch: fetched https://en.wikipedia.org/wiki/Drip_coffee_maker (330825 chars)
2026-10-04 20:46:15,188 INFO ingestion.brewing_methods: wikipedia: 13 rows
2026-10-04 20:46:16,898 DEBUG urllib3.connectionpool: Starting new HTTPS connection (1): www.healthline.com:443
2026-10-04 20:46:17,178 DEBUG urllib3.connectionpool: https://www.healthline.com:443 "GET /robots.txt HTTP/1.1" 200 None
2026-10-04 20:46:18,999 DEBUG urllib3.connectionpool: https://www.healthline.com:443 "GET /nutrition/how-much-caffeine-in-coffee HTTP/1.1" 200 None
2026-10-04 20:46:19,007 INFO ingestion.fetch: fetched https://www.healthline.com/nutrition/how-much-caffeine-in-coffee (386955 chars)
2026-10-04 20:46:19,036 INFO ingestion.brewing_methods: healthline: 3 rows
2026-10-04 20:46:20,899 DEBUG urllib3.connectionpool: Starting new HTTPS connection (1): perfectdailygrind.com:443
2026-10-04 20:46:25,513 DEBUG urllib3.connectionpool: https://perfectdailygrind.com:443 "GET /robots.txt HTTP/1.1" 202 178
2026-10-04 20:46:25,529 DEBUG urllib3.connectionpool: https://perfectdailygrind.com:443 "GET /2019/10/a-guide-to-every-coffee-brewing-method/ HTTP/1.1" 202 221
2026-10-04 20:46:25,530 INFO ingestion.fetch: fetched https://perfectdailygrind.com/2019/10/a-guide-to-every-coffee-brewing-method/ (221 chars)
2026-10-04 20:46:25,530 INFO ingestion.brewing_methods: pdg: 0 rows
2026-10-04 20:46:27,514 DEBUG urllib3.connectionpool: Starting new HTTPS connection (1): www.ncausa.org:443
2026-10-04 20:46:27,662 DEBUG urllib3.connectionpool: https://www.ncausa.org:443 "GET /robots.txt HTTP/1.1" 200 732
2026-10-04 20:46:29,523 DEBUG urllib3.connectionpool: https://www.ncausa.org:443 "GET /About-Coffee/Brewing-Methods HTTP/1.1" 301 145
2026-10-04 20:46:29,524 DEBUG urllib3.connectionpool: Starting new HTTPS connection (1): www.aboutcoffee.org:443
2026-10-04 20:46:29,594 DEBUG urllib3.connectionpool: https://www.aboutcoffee.org:443 "GET / HTTP/1.1" 200 125927
2026-10-04 20:46:29,609 INFO ingestion.fetch: fetched https://www.ncausa.org/About-Coffee/Brewing-Methods (357260 chars)
2026-10-04 20:46:29,636 INFO ingestion.brewing_methods: nca: 5 rows
2026-10-04 20:46:29,636 INFO ingestion.brewing_methods: wrote data/raw/brewing_wikipedia.csv
2026-10-04 20:46:29,637 INFO ingestion.brewing_methods: wrote data/raw/brewing_healthline.csv
2026-10-04 20:46:29,637 WARNING ingestion.brewing_methods: pdg: no rows, no file written
2026-10-04 20:46:29,637 INFO ingestion.brewing_methods: wrote data/raw/brewing_nca.csv
```

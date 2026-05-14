import scrapy


class BMW2025Spider(scrapy.Spider):
    name = "motorcycle_com_page"
    allowed_domains = ["www.motorcycle.com"]

    total_pages = 5

    custom_headers = {
        "User-Agent": "Mozilla/5.0"
    }

    def start_requests(self):

        base_url = "https://www.motorcycle.com/specs/cfmoto.html"

        yield scrapy.Request(
            base_url,
            headers=self.custom_headers,
            callback=self.parse_list_page
        )

        for i in range(2, self.total_pages + 1):
            url = f"{base_url}?page_num={i}"
            yield scrapy.Request(
                url,
                headers=self.custom_headers,
                callback=self.parse_list_page
            )

    # PARSE LIST PAGES
    def parse_list_page(self, response):

        # Extract motorcycle detail links
        links = response.css("a.card-link::attr(href)").getall()

        for link in links:
            yield response.follow(
                link,
                headers=self.custom_headers,
                callback=self.parse_specs
            )

    # PARSE INDIVIDUAL BIKE SPEC PAGE
    def parse_specs(self, response):

        bike_name = response.css("h1.hdr-h.sl-post-title::text").get()
        bike_name = bike_name.strip() if bike_name else ""

        for panel in response.css("div.spec-page-section div.panel"):

            section = panel.css("h4.panel-title::text").get()
            if not section:
                continue

            section = section.strip()

            for row in panel.css("div.vs-specs-table-row"):
                key = row.css("div.spec-key::text").get()
                if not key:
                    continue
                key = key.strip()

                raw_parts = row.css("div.spec-value ::text").getall()
                value = " ".join(p.strip() for p in raw_parts if p.strip())

                yield {
                    "bike": bike_name,
                    "section": section,
                    "key": key,
                    "value": value,
                    "url": response.url,
                }

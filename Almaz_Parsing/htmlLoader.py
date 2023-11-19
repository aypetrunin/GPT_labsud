# дозагрузка отсутствующих файлов

import SiteLoader
import nest_asyncio
nest_asyncio.apply()
from langchain.document_loaders.sitemap import SitemapLoader

def reloadhtml():
    docsload = SiteLoader.list_docs_toload()
    pages = list(map(lambda x: x.page, docsload))
    url_site_map=""
    sitemap_loader = SitemapLoader(url_site_map)
    docs = sitemap_loader.scrape_all(pages)
    SiteLoader.saveDocs_toload(docs, docsload)

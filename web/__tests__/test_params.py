from ..params import IdQuery, SearchParam, URLParam, CollectionParam, PostQueryParams, PostNeighboursParams, \
    PostURLIngestParams


def test_id_query():
    param = IdQuery(id="my-id")
    assert param.id == "my-id"
    assert param.id == param.get_id()


def test_id_query_index():
    param = IdQuery(id="my-id/")
    assert param.id == "my-id/"
    assert param.get_id() == "my-id/index.md"


def test_search_param():
    param = SearchParam(search="my keyword")
    assert param.search == "my keyword"


def test_url_param():
    param = URLParam(url="my/url")
    assert param.url == "my/url"


def test_collection_param():
    param = CollectionParam(collection="mycollection")
    assert param.collection == "mycollection"


def test_post_query_params():
    param = PostQueryParams(search="my keyword", collection="mycollection")
    assert param.search == "my keyword"
    assert param.collection == "mycollection"


def test_post_neighbours_params():
    param = PostNeighboursParams(id="my-id", collection="mycollection")
    assert param.id == "my-id"
    assert param.collection == "mycollection"


def test_post_url_ingest_params():
    param = PostURLIngestParams(url="my/url", collection="mycollection")
    assert param.url == "my/url"
    assert param.collection == "mycollection"

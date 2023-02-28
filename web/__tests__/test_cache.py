from ..cache import get_md5, get_cache, set_cache, prune_cache


def test_get_md5():
    response = get_md5('')
    assert response == 'd41d8cd98f00b204e9800998ecf8427e'

    response = get_md5('shopware')
    assert response == 'a256a310bc1e5db755fd392c524028a8'


def test_get_cache():
    response = get_cache('nonexistent')
    assert response is None


def test_set_cache():
    value = 'my-existent-value'
    set_cache('existent', value)
    assert get_cache('existent') == value


def test_prune_cache():
    pass

import time

import pytest


@pytest.fixture(
    params=[
        1293840000,  # 2011-01-01 00:00:00
        1293839999,  # 2010-12-31 23:59:59
    ]
)
def source_date_year(request, monkeypatch):
    source_date_epoch = request.param
    with monkeypatch.context() as m:
        m.setenv('SOURCE_DATE_EPOCH', str(source_date_epoch))
        yield time.gmtime(source_date_epoch).tm_year


@pytest.mark.sphinx('html', testroot='copyright-multiline')
def test_html_multi_line_copyright(app):
    app.build(force_all=True)

    content = (app.outdir / 'index.html').read_text(encoding='utf-8')

    # check the copyright footer line by line (empty lines ignored)
    assert '  &#169; Copyright 2006.<br/>\n' in content
    assert '  &#169; Copyright 2006-2009, Alice.<br/>\n' in content
    assert '  &#169; Copyright 2010-2013, Bob.<br/>\n' in content
    assert '  &#169; Copyright 2014-2017, Charlie.<br/>\n' in content
    assert '  &#169; Copyright 2018-2021, David.<br/>\n' in content
    assert '  &#169; Copyright 2022-2025, Eve.' in content

    # check the raw copyright footer block (empty lines included)
    assert (
        '      &#169; Copyright 2006.<br/>\n'
        '    \n'
        '      &#169; Copyright 2006-2009, Alice.<br/>\n'
        '    \n'
        '      &#169; Copyright 2010-2013, Bob.<br/>\n'
        '    \n'
        '      &#169; Copyright 2014-2017, Charlie.<br/>\n'
        '    \n'
        '      &#169; Copyright 2018-2021, David.<br/>\n'
        '    \n'
        '      &#169; Copyright 2022-2025, Eve.'
    ) in content


@pytest.mark.sphinx('html', testroot='copyright-multiline')
def test_html_multi_line_copyright_sde(source_date_year, app):
    app.build(force_all=True)

    content = (app.outdir / 'index.html').read_text(encoding='utf-8')

    # check the copyright footer line by line (empty lines ignored)
    assert f'  &#169; Copyright {source_date_year}.<br/>\n' in content
    assert f'  &#169; Copyright 2006-{source_date_year}, Alice.<br/>\n' in content
    assert f'  &#169; Copyright 2010-{source_date_year}, Bob.<br/>\n' in content
    assert f'  &#169; Copyright 2014-{source_date_year}, Charlie.<br/>\n' in content
    assert f'  &#169; Copyright 2018-{source_date_year}, David.<br/>\n' in content
    assert f'  &#169; Copyright 2022-{source_date_year}, Eve.' in content

    # check the raw copyright footer block (empty lines included)
    assert (
        f'      &#169; Copyright {source_date_year}.<br/>\n'
        f'    \n'
        f'      &#169; Copyright 2006-{source_date_year}, Alice.<br/>\n'
        f'    \n'
        f'      &#169; Copyright 2010-{source_date_year}, Bob.<br/>\n'
        f'    \n'
        f'      &#169; Copyright 2014-{source_date_year}, Charlie.<br/>\n'
        f'    \n'
        f'      &#169; Copyright 2018-{source_date_year}, David.<br/>\n'
        f'    \n'
        f'      &#169; Copyright 2022-{source_date_year}, Eve.'
    ) in content
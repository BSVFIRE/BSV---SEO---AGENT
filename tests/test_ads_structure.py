from seo_agent.ads_structure import parse


def test_counts_match_declared():
    camps = parse()
    assert [len(sum((g["keywords"] for g in c["ad_groups"]), [])) for c in camps] == [63, 34, 8]
    for c in camps:
        for g in c["ad_groups"]:
            assert len(g["keywords"]) == g["declared"], g["ad_group"]
    assert sum(c["declared"] for c in camps) == 105


def test_landing_pages_cover_all_ad_groups():
    from seo_agent.ads_structure import landing_pages
    lp = {r["ad_group"] for r in landing_pages()}
    assert all(g["ad_group"] in lp for c in parse() for g in c["ad_groups"] if g["ad_group"] != "(ingen)")

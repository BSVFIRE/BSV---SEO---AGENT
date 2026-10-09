from seo_agent.ads_structure import parse


def test_counts_match_declared():
    camps = parse()
    assert [len(sum((g["keywords"] for g in c["ad_groups"]), [])) for c in camps] == [63, 34, 8]
    for c in camps:
        for g in c["ad_groups"]:
            assert len(g["keywords"]) == g["declared"], g["ad_group"]
    assert sum(c["declared"] for c in camps) == 105

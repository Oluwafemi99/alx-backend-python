# fixtures.py
TEST_PAYLOAD = [
    (  # org_payload
        {"repos_url": "https://api.github.com/orgs/google/repos"},
        [  # repos_payload
            {"name": "repo1", "license": {"key": "apache-2.0"}},
            {"name": "repo2", "license": {"key": "other-license"}},
        ],
        ["repo1", "repo2"],  # expected_repos
        ["repo1"],  # apache2_repos
    )
]

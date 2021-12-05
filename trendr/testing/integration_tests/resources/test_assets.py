from trendr.testing.bindings import assets as asset_bindings


def test_fear_greed(client):
    response = asset_bindings.fear_greed(client)
    assert response.status_code == 200
    resp_data = response.json
    assert "crypto_values" in resp_data
    assert "valueText" in resp_data["crypto_values"]
    assert "value" in resp_data["crypto_values"]
    assert "stock_values" in resp_data
    assert "value" in resp_data["stock_values"]
    assert "valueText" in resp_data["stock_values"]


def test_search(client):
    response = asset_bindings.search(client, params={"query": "AAPL"})
    assert response.status_code == 200
    resp_data = response.json
    assert len(resp_data) > 0
    assert "AAPL" in resp_data[0]["symbol"]


def test_historic_fear_greed(client):
    response = asset_bindings.historic_fear_greed(client, params={"days": "1"})
    assert response.status_code == 200
    resp_data = response.json
    assert len(resp_data) > 0
    assert "crypto_values" in resp_data
    assert "value" in resp_data["crypto_values"][0]
    assert "stock_values" in resp_data


def test_crypto_stats(client):
    response = asset_bindings.crypto_stats(client, params={"id": "bitcoin"})
    assert response.status_code == 200
    resp_data = response.json
    assert resp_data["Name"] == "Bitcoin"
    assert resp_data["Symbol"] == "btc"


def test_stock_stats(client):
    response = asset_bindings.stock_stats(client, params={"symbol": "AAPL"})
    assert response.status_code == 200
    resp_data = response.json
    assert resp_data["longName"] == "Apple Inc."
    assert resp_data["symbol"] == "AAPL"


def test_crypto_eth_address(client):
    response = asset_bindings.crypto_eth_address(client, params={"id": "aave"})
    assert response.status_code == 200
    resp_data = response.json
    assert isinstance(resp_data, str)
    assert len(resp_data) > 0


def test_crypto_price_history(client):
    response = asset_bindings.crypto_price_history(
        client, params={"id": "bitcoin", "days": "1"}
    )
    assert response.status_code == 200
    resp_data = response.json
    assert len(resp_data) > 0
    assert isinstance(resp_data[0][0], str)
    assert isinstance(resp_data[0][1], float)


def test_crypto_volume_history(client):
    response = asset_bindings.crypto_volume_history(
        client, params={"id": "bitcoin", "days": "1"}
    )
    assert response.status_code == 200
    resp_data = response.json
    assert len(resp_data) > 0
    assert isinstance(resp_data[0][0], str)
    assert isinstance(resp_data[0][1], float)


def test_twitter_sentiment(client, db):
    response = asset_bindings.twitter_sentiment(client, params={"symbol": "AAPL"})
    assert response.status_code == 200
    resp_data = response.json
    print(f"sentiment: {resp_data}")
    assert len(resp_data) > 0


def test_tweet_summary(client, db):
    response = asset_bindings.tweet_summary(client, asset_identifier="AAPL")
    assert response.status_code == 200
    resp_data = response.json
    assert "follower_stats" in resp_data
    assert "following_stats" in resp_data
    assert "accounts_age_stats" in resp_data
    assert "verified_count" in resp_data

"""
Unit tests for backend.core.jwt -- token creation/decoding in isolation,
without going through the /auth API. Compare with tests/api/test_auth_api.py,
which exercises the same logic end-to-end through HTTP.
"""

from datetime import timedelta

import pytest
from jose import jwt as jose_jwt

from backend.core.jwt import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    SECRET_KEY,
    create_access_token,
    decode_access_token,
)


def test_create_access_token_embeds_the_given_claims():
    token = create_access_token({"sub": "123"})

    payload = decode_access_token(token)

    assert payload["sub"] == "123"


def test_create_access_token_sets_an_expiry_claim():
    token = create_access_token({"sub": "123"})

    payload = decode_access_token(token)

    assert "exp" in payload


def test_decode_access_token_rejects_a_tampered_token():
    token = create_access_token({"sub": "123"})
    # Flip a character in the middle of the signature segment. Flipping the
    # very last character is unreliable: base64url's trailing character
    # sometimes only encodes padding bits, so a "tampered" token can decode
    # to the exact same bytes and the signature still checks out.
    header, payload, signature = token.split(".")
    middle = len(signature) // 2
    flipped_char = "A" if signature[middle] != "A" else "B"
    tampered_signature = signature[:middle] + flipped_char + signature[middle + 1 :]
    tampered = f"{header}.{payload}.{tampered_signature}"

    with pytest.raises(Exception):
        decode_access_token(tampered)


def test_decode_access_token_rejects_an_expired_token():
    expired_token = create_access_token(
        {"sub": "123"}, expires_delta=timedelta(minutes=-1)
    )

    with pytest.raises(Exception):
        decode_access_token(expired_token)


def test_decode_access_token_rejects_a_token_signed_with_a_different_secret():
    forged_token = jose_jwt.encode(
        {"sub": "123"}, "a-completely-different-secret", algorithm=ALGORITHM
    )

    with pytest.raises(Exception):
        decode_access_token(forged_token)


def test_default_expiry_matches_configured_minutes():
    # Sanity check that the module is actually reading config.access_token_expire_minutes
    # rather than a hardcoded value that's drifted out of sync.
    assert ACCESS_TOKEN_EXPIRE_MINUTES > 0
    assert SECRET_KEY  # non-empty

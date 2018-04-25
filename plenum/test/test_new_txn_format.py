import pytest

from plenum.common.txn_util import transform_to_new_format
from plenum.common.util import SortedDict


@pytest.fixture(
    params=['all', 'sig_only', 'none_sig', 'sigs_only', 'none_sigs', 'no_protocol_vers', 'none_protocol_vers'])
def old_and_expected(request):
    old = {
        "dest": "GEzcdDLhCpGCYRHW82kjHd",
        "verkey": "~HmUWn928bnFT6Ephf65YXv",
        "role": "101",

        "type": "1",
        "protocolVersion": 1,
        "identifier": "L5AD5g65TDQr1PPHHRoiGf",
        "reqId": 1513945121191691,
        "signature": "3SyRto3MGcBy1o4UmHoDezy1TJiNHDdU9o7TjHtYcSqgtpWzejMoHDrz3dpT93Xe8QXMF2tJVCQTtGmebmS2DkLS",
        "signatures": {"L5AD5g65TDQr1PPHHRoiGf":
                           "3SyRto3MGcBy1o4UmHoDezy1TJiNHDdU9o7TjHtYcSqgtpWzejMoHDrz3dpT93Xe8QXMF2tJVCQTtGmebmS2DkLS"},
        "txnTime": 1513945121
    }
    new_expected = SortedDict({
        "reqSignature": {
            "type": "ED25519",
            "values": [{
                "from": "L5AD5g65TDQr1PPHHRoiGf",
                "value": "3SyRto3MGcBy1o4UmHoDezy1TJiNHDdU9o7TjHtYcSqgtpWzejMoHDrz3dpT93Xe8QXMF2tJVCQTtGmebmS2DkLS"
            }]
        },
        "txn": {
            "data": {
                "dest": "GEzcdDLhCpGCYRHW82kjHd",
                "role": "101",
                "verkey": "~HmUWn928bnFT6Ephf65YXv",
            },

            "metadata": {
                "from": "L5AD5g65TDQr1PPHHRoiGf",
                "reqId": 1513945121191691,
            },

            "protocolVersion": 1,
            "type": "1",
        },
        "txnMetadata": {
            "creationTime": 1513945121,
            "seqNo": 143,
        },

    })

    if request.param == 'sig_only':
        old.pop("signatures")
    if request.param == 'none_sigs':
        old["signatures"] = None
    if request.param == 'sigs_only':
        old.pop("signature")
    if request.param == 'none_sig':
        old["signature"] = None
    if request.param == 'no_protocol_vers':
        old.pop("protocolVersion")
        new_expected["txn"]["protocolVersion"] = None
    if request.param == 'none_protocol_vers':
        old["protocolVersion"] = None
        new_expected["txn"]["protocolVersion"] = None

    return old, new_expected


def test_new_txn_format(old_and_expected):
    old, new_expected = old_and_expected
    new = SortedDict(transform_to_new_format(old, 143))
    assert new == new_expected
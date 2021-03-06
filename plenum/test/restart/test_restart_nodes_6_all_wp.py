import pytest
from plenum.test.test_node import ensure_node_disconnected, checkNodesConnected
from plenum.test import waits
from plenum.test.node_request.helper import sdk_ensure_pool_functional
from plenum.common.config_helper import PNodeConfigHelper
from plenum.test.test_node import TestNode
from plenum.test.restart.test_restart_nodes import get_group, restart_nodes

nodeCount = 7


def test_restart_groups_wp(looper, txnPoolNodeSet, tconf, tdir,
                           sdk_pool_handle, sdk_wallet_client, allPluginsPath):
    tm = tconf.ToleratePrimaryDisconnection + waits.expectedPoolElectionTimeout(len(txnPoolNodeSet))

    restart_group = get_group(txnPoolNodeSet, 6, include_primary=True)

    restart_nodes(looper, txnPoolNodeSet, restart_group, tconf, tdir, allPluginsPath,
                  after_restart_timeout=tm, per_add_timeout=None)
    sdk_ensure_pool_functional(looper, txnPoolNodeSet, sdk_wallet_client, sdk_pool_handle)

def test_smoke(acct1, acct2, acct3, weth_contract):
    assert acct1.balance > 0
    assert acct2.balance > 0
    assert acct3.balance > 0
    assert weth_contract.balance == 0
    assert weth_contract.totalSupply() == 0


def test_deposit(acct1, weth_contract):
    assert weth_contract.totalSupply() == 0
    assert weth_contract.balanceOf(acct1) == 0

    tx_receipt = weth_contract.deposit(value=100, sender=acct1)

    assert weth_contract.totalSupply() == 100
    assert weth_contract.balance == 100
    assert weth_contract.balanceOf(acct1) == 100

    # test Deposit event
    logs = weth_contract.Deposit.from_receipt(tx_receipt)
    assert len(logs) == 1
    assert logs[0].event_name == "Deposit"


def test_withdraw(acct1, weth_contract):
    weth_contract.deposit(value=100, sender=acct1)
    assert weth_contract.totalSupply() == 100
    assert weth_contract.balanceOf(acct1) == 100

    tx_receipt = weth_contract.withdraw(50, sender=acct1)

    assert weth_contract.totalSupply() == 50
    assert weth_contract.balanceOf(acct1) == 50

    # test Withdrawal event
    logs = weth_contract.Withdrawal.from_receipt(tx_receipt)
    assert len(logs) == 1
    assert logs[0].event_name == "Withdrawal"


def test_approve(acct1, acct2, weth_contract):
    weth_contract.deposit(value=100, sender=acct1)

    assert weth_contract.allowance(acct1, acct2) == 0
    tx_receipt = weth_contract.approve(acct2, 25, sender=acct1)
    assert weth_contract.allowance(acct1, acct2) == 25

    # test Approval event
    logs = weth_contract.Approval.from_receipt(tx_receipt)
    assert len(logs) == 1
    assert logs[0].event_name == "Approval"


def test_transfer(acct1, acct2, weth_contract):
    weth_contract.deposit(value=100, sender=acct1)
    tx_receipt = weth_contract.transfer(acct2, 35, sender=acct1)

    assert weth_contract.balanceOf(acct1) == 65
    assert weth_contract.balanceOf(acct2) == 35

    # test Transfer event
    logs = weth_contract.Transfer.from_receipt(tx_receipt)
    assert len(logs) == 1
    assert logs[0].event_name == "Transfer"


def test_transfer_from(acct1, acct2, acct3, weth_contract):
    weth_contract.deposit(value=100, sender=acct1)
    weth_contract.approve(acct2, 50, sender=acct1)

    assert weth_contract.balanceOf(acct1) == 100
    assert weth_contract.balanceOf(acct2) == 0
    assert weth_contract.balanceOf(acct3) == 0

    tx_receipt = weth_contract.transferFrom(acct1, acct3, 15, sender=acct2)

    assert weth_contract.balanceOf(acct1) == 85
    assert weth_contract.balanceOf(acct2) == 0
    assert weth_contract.balanceOf(acct3) == 15

    # test Transfer event
    logs = weth_contract.Transfer.from_receipt(tx_receipt)
    assert len(logs) == 1
    assert logs[0].event_name == "Transfer"

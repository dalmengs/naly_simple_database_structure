import pytest
from app import DatabaseManager

databaseManager: DatabaseManager = DatabaseManager()

def test_loadUserByUsernameSucceed():
    global databaseManager
    result = databaseManager.findUserByUsername("dalmeng")
    assert result["returnCode"] in [0, 1]

def test_loadUserByUsernameInjection():
    global databaseManager
    result = databaseManager.findUserByUsername(" ")
    assert result["returnCode"] == -1

def test_loadUserByUsernameFailed():
    global databaseManager
    result = databaseManager.findUserByUsername("naly")
    assert result["returnCode"] == -1

def test_synchronization():
    global databaseManager
    result = databaseManager.syncDatabase("dalmeng")
    assert result["returnCode"] == 0

def test_synchronizationFailed():
    global databaseManager
    result = databaseManager.syncDatabase("naly")
    assert result["returnCode"] == -1

def test_synchronizationInjection():
    global databaseManager
    result = databaseManager.syncDatabase(" ")
    assert result["returnCode"] == -1
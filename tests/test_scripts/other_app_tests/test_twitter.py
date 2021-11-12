from business_components.twitter_steps import *
from utilities.helper import *
from utilities.PyAutoReadWrite import ReadWrite
import pytest


@pytest.mark.twitter_login
def test_login_twitter(driver):
    login_twitter(driver, "aswinselva03", "wrongpassword")

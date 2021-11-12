Feature: Flipkart Test for iOS
    Test flipkart for iOS and press hold


  @mobile_bdd
  Scenario Outline: I test the flipkart app for iOS and try press hold icon in home
    Given The flipkart app is open in mobile and click Search
    Then Go back and Navigate to home
    Then Check for press and hold on spotify icon
    Examples:
      |  |

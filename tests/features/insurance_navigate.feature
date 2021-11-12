Feature: Insurance quote page navigation
    Validate links in home page in header and footer

    Scenario: Validate header links in the application
        Given I am on autoQuoteHomePage
        Then I Validate the header links

    @smoke
    Scenario: Validate footer links in the application
        Given I am on autoQuoteHomePage
        Then I Validate the footer links






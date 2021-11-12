Feature: Selenium Easy Input forms demo
    Enter the input form with valid detail

    @bdd_selenium
    Scenario Outline: I enter valid details in input form page
        Given I am on selenium easy page and i navigate to input forms page
        When I enter valid <first_name> in First Name field
        And I enter valid <last_name> in Last Name field
        And I enter valid <email> in Email field
        And I enter valid <phone> in phone number field
        And I enter valid <address> in Address field
        And I enter valid <city> in city field
        And I select valid <state> in state dropdown
        And I enter valid <zip_code> in zip code field
        And I enter valid website or domain name as "https://www.cognizant.com"
        And I choose <yes_or_no> in for Do you have a hosting
        And I enter valid <project_description> in description field
        Then I submit the form
      
    Examples:
          | first_name | last_name | email            | phone        | address    | city        | state       | zip_code | yes_or_no | project_description |
          | tester     | World     | tester@gmail.com | 9087161212   | 1, plato   | Newyork     | Washington  | 90251    | yes       | waterfall method    |
          | testing    | Planet    | testing@gov.in   | 9123490812   | 1, plato   | Vegas       | Washington  | 91231    | yes       | Agile project       |
      
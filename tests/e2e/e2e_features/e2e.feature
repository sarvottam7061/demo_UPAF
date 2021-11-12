Feature: e2e fetch data and create user
    Fetch data from application and use first name to create an user

    @bdd_e2e
    Scenario: Perform e2e testing in bdd style
        Given I check the download progress
        When I fetch the name and write it in excel file
        And I read the data written and validate it
        Then  I create an user using first name
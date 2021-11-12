Feature: Insurance quote
    Generate quote for different vehicles

    @bdd
    Scenario Outline: I generate the quote for automobile insurance
        Given I am on autoQuoteHomePage
        When I navigate to enter details automobile quote page
        And I select the make value as <make>
        And I enter <ePerformance> value in Engine Performance text box
        And I enter <dom> value in Date of manufacture date picker
        And I select the number of seats as <nos>
        And I select the fuel type as <fuelType>
        And I enter <listPrice> value in list price text box
        And I enter <licensePlateNum> value in license plate number text box
        And I enter <annualMileage> value in annual mileage text box

    Examples:
        | make | ePerformance | dom        | nos | fuelType | listPrice | licensePlateNum | annualMileage |
        | BMW  | 1000         | 12/12/2020 | 6   | Diesel   | 20000     | AX2234B2        | 10000         |
        | Ford | 2000         | 10/12/2019 | 5   | Petrol   | 25000     | BX1234C4        | 15000         |







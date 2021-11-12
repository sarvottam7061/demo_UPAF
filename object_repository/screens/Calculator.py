from PyAuto.PyAutoDesktop import PyAutoWindows


class Calc(PyAutoWindows):
    locatorNine = {"title": "Nine", "auto_id": "num9Button"}
    locatorPlus = {"title": "Plus", "auto_id": "plusButton"}
    locatorEquals = {"title": "Equals", "auto_id": "equalButton"}
    locatorResult = {"auto_id": "CalculatorResults"}
    locatorSquare = {"title": "Square", "auto_id": "xpower2Button"}

    def __init__(self, app):
        super().__init__(app)  # call super class constructor
        
    def addition(self):
        self.find_element_wait(self.locatorNine).click()
        self.find_element_wait(self.locatorPlus).click()
        self.find_element_wait(self.locatorNine).click()
        self.find_element_wait(self.locatorEquals).click()
    #     self.app.type_keys('3')
    #     self.app.type_keys('*')
    #     self.app.type_keys('2')
    #     self.app.type_keys('=')
    #     print(self.get_element_text(self.locatorResult))
        return self

    def square(self):
        self.find_element_wait(self.locatorNine).click()
        self.find_element_wait(self.locatorPlus).click()
        self.find_element_wait(self.locatorNine).click()
        self.find_element_wait(self.locatorEquals).click()
        self.find_element_wait(self.locatorSquare).click()
        # print(self.get_element_text(self.locatorResult))
        # num = val.split(" ")[2]
        # print(num)
        # self.find_element_by_name("Square root").click()
        # print(self.find_element_by_accessibility_id("CalculatorResults").text)

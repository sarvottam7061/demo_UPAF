import allure

class SapGuiPom():
    locatorUser = {"sap_id": "/app/con[0]/ses[0]/wnd[0]/usr/txtRSYST-BNAME"}
    locatorPass = {"sap_id": "/app/con[0]/ses[0]/wnd[0]/usr/pwdRSYST-BCODE"}
    locatorTcode = {"sap_id": "/app/con[0]/ses[0]/wnd[0]/tbar[0]/okcd"}
    locatorOrderTyp = {"sap_id": "/app/con[0]/ses[0]/wnd[0]/usr/ctxtVBAK-AUART"}
    locatorSalesOrg = {"sap_id": "/app/con[0]/ses[0]/wnd[0]/usr/ctxtVBAK-VKORG"}
    locatorDistChanel = {"sap_id": "/app/con[0]/ses[0]/wnd[0]/usr/ctxtVBAK-VTWEG"}
    locatorDivision = {"sap_id": "/app/con[0]/ses[0]/wnd[0]/usr/ctxtVBAK-SPART"}
    locatorSoldToParty = {
        "sap_id": "/app/con[0]/ses[0]/wnd[0]/usr/subSUBSCREEN_HEADER:SAPMV45A:4021/subPART-SUB:SAPMV45A:4701/ctxtKUAGV-KUNNR"}
    locatorShipToParty = {
        "sap_id": "/app/con[0]/ses[0]/wnd[0]/usr/subSUBSCREEN_HEADER:SAPMV45A:4021/subPART-SUB:SAPMV45A:4701/ctxtKUWEV-KUNNR"}
    locatorCustRef = {"sap_id": "/app/con[0]/ses[0]/wnd[0]/usr/subSUBSCREEN_HEADER:SAPMV45A:4021/txtVBKD-BSTKD"}
    locatorMaterial = {
        "sap_id": r"/app/con[0]/ses[0]/wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\01/ssubSUBSCREEN_BODY:SAPMV45A:4400/subSUBSCREEN_TC:SAPMV45A:4900/tblSAPMV45ATCTRL_U_ERF_AUFTRAG/ctxtRV45A-MABNR[1,0]"}
    locatorOrdQuant = {
        "sap_id": r"/app/con[0]/ses[0]/wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\01/ssubSUBSCREEN_BODY:SAPMV45A:4400/subSUBSCREEN_TC:SAPMV45A:4900/tblSAPMV45ATCTRL_U_ERF_AUFTRAG/txtRV45A-KWMENG[3,0]"}
    locatorPlnt = {
        "sap_id": r"/app/con[0]/ses[0]/wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\01/ssubSUBSCREEN_BODY:SAPMV45A:4400/subSUBSCREEN_TC:SAPMV45A:4900/tblSAPMV45ATCTRL_U_ERF_AUFTRAG/ctxtVBAP-WERKS[12,0]"}
    locatorHedrDetail = {"sap_id": "/app/con[0]/ses[0]/wnd[0]/usr/subSUBSCREEN_HEADER:SAPMV45A:4021/btnBT_HEAD"}
    locatorOrderData = {"sap_id": r"/app/con[0]/ses[0]/wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\11"}
    locatorPurOrderTyp = {
        "sap_id": r"/app/con[0]/ses[0]/wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\11/ssubSUBSCREEN_BODY:SAPMV45A:4351/ctxtVBKD-BSARK"}
    locatorSales = {"sap_id": r"/app/con[0]/ses[0]/wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\01"}
    locatorOrdrReason = {
        "sap_id": r"/app/con[0]/ses[0]/wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\01/ssubSUBSCREEN_BODY:SAPMV45A:4301/cmbVBAK-AUGRU"}
    locatorEdit = {"sap_id": "/app/con[0]/ses[0]/wnd[0]/mbar/menu[1]"}
    locatorIncompLog = {"sap_id": "/app/con[0]/ses[0]/wnd[0]/mbar/menu[1]/menu[11]"}
    locatorDocComplete = {"sap_id": "/app/con[0]/ses[0]/wnd[0]/sbar/pane[0]"}
    locatorSave = {"sap_id": "/app/con[0]/ses[0]/wnd[0]/tbar[0]/btn[11]"}
    locatorStandardOrder = {"sap_id": "/app/con[0]/ses[0]/wnd[0]/sbar/pane[0]"}
    locatorExit = {"sap_id": "/app/con[0]/ses[0]/wnd[0]/tbar[0]/btn[15]"}
    locatorYes = {"sap_id": "/app/con[0]/ses[0]/wnd[1]/usr/btnSPOP-OPTION1"}

    # locatorUser = {"sap_id": "/app/con[0]/ses[0]/wnd[0]/usr/txtRSYST-BNAME"}

    def __init__(self, sap_session):
        self.sap_session = sap_session

    @allure.step("open connection")
    def open_connection(self):
        self.sap_session.open_connection("SQT")
        # self.sap_session.send_vkey(0)
        return self

    @allure.step("login to sap")
    def login_sap(self):
        self.sap_session.input_text(self.locatorUser["sap_id"], "TEST_03")
        self.sap_session.input_password(self.locatorPass["sap_id"], "Cts@1234")
        self.sap_session.send_vkey(0)
        return self

    @allure.step("entering TCode")
    def enter_tcode(self):
        self.sap_session.input_text(self.locatorTcode["sap_id"], "VA01")
        self.sap_session.send_vkey(0)
        return self

    @allure.step("create sales document")
    def create_sales_doc(self):
        self.sap_session.input_text(self.locatorOrderTyp["sap_id"], "OR")
        self.sap_session.input_text(self.locatorSalesOrg["sap_id"], "1710")
        self.sap_session.input_text(self.locatorDistChanel["sap_id"], "10")
        self.sap_session.input_text(self.locatorDivision["sap_id"], "00")
        self.sap_session.send_vkey(0)
        return self

    @allure.step("create standard order")
    def create_standard_order(self):
        self.sap_session.input_text(self.locatorSoldToParty["sap_id"], "17100008")
        self.sap_session.input_text(self.locatorShipToParty["sap_id"], "17100008")
        self.sap_session.input_text(self.locatorCustRef["sap_id"], "test_015")
        self.sap_session.send_vkey(0)
        self.sap_session.input_text(self.locatorMaterial["sap_id"], "MZ-FG-M550")
        self.sap_session.input_text(self.locatorOrdQuant["sap_id"], "10")
        self.sap_session.input_text(self.locatorPlnt["sap_id"], "1710")
        self.sap_session.send_vkey(0)
        return self

    @allure.step("display header details")
    def display_header_details(self):
        self.sap_session.click_element(self.locatorHedrDetail["sap_id"])
        self.sap_session.click_element(self.locatorOrderData["sap_id"])
        self.sap_session.input_text(self.locatorPurOrderTyp["sap_id"], "TELE")
        self.sap_session.send_vkey(0)
        self.sap_session.click_element(self.locatorSales["sap_id"])
        self.sap_session.select_from_list_by_label(self.locatorOrdrReason["sap_id"], "Fast Delivery")
        self.sap_session.click_element(self.locatorEdit["sap_id"])
        self.sap_session.click_element(self.locatorIncompLog["sap_id"])
        return self

    @allure.step("document complete")
    def get_doc_complete(self):
        self.sap_session.element_value_should_be(self.locatorDocComplete["sap_id"], "Document is complete")
        text = self.sap_session.get_value(self.locatorDocComplete["sap_id"])
        print(text)
        return self

    @allure.step("order number saved")
    def save_and_get_order_number(self):
        self.sap_session.click_element(self.locatorSave["sap_id"])
        text = self.sap_session.get_value(self.locatorStandardOrder["sap_id"])
        print(text)
        self.sap_session.click_element(self.locatorExit["sap_id"])
        self.sap_session.click_element(self.locatorExit["sap_id"])
        self.sap_session.click_element(self.locatorYes["sap_id"])
        return self
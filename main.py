import time

import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')

    button_get_taxi = (By.CSS_SELECTOR, ".button.round")
    confort_button = (By.XPATH,'//*[@id="root"]/div/div[3]/div[3]/div[2]/div[1]/div[5]')
    blanket_and_tissue_confort = (By.XPATH,'//div[@class="r-sw-label" and text()="Manta y pañuelos"]')

    phone_number_button = (By.CLASS_NAME, "np-button")
    phone_number_field = (By.ID, "phone")
    button_siguiente = (By.XPATH, '//button[text()="Siguiente"]')
    code_field = (By.XPATH, "//input[@id='code'][@class='input'][@type='text'][@placeholder='xxxx']")
    button_confirm = (By.XPATH, '//*[text()="Confirmar"]')
    phone_field_text = (By.XPATH,"//div[@class='np-text']")

    payment_method_field = (By.CSS_SELECTOR, ".pp-text")
    button_plus_card = (By.CLASS_NAME, "pp-plus-container")
    add_card_field = (By.ID, "number")
    add_code_card = (By.NAME, "code")
    agregar_tarjeta_button = (By.XPATH, '//button[text()="Agregar"]')
    cerrar_payment_button = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/button')
    tarjeta_agregada_text = (By.CLASS_NAME, "pp-value-text")

    select_mensaje_driver = (By.XPATH, '//label[@for="comment" and @class="label"]')
    mensaje_field = (By.XPATH, '//*[@id="comment"]')
    mensaje_driver_text = (By.CLASS_NAME, 'reqs-head')

    select_blanket_and_tissue = (By.CLASS_NAME, 'r-sw')
    confirm_blanket_and_tissue = (By.CSS_SELECTOR, '.r-sw > div >input')

    add_ice_cream = (By.CSS_SELECTOR, '.r-group-items>:nth-child(1)>div>.r-counter>div>.counter-plus')
    selected_two_ice_creams = (By.XPATH, "//div[@class='counter-value']")

    button_search_taxi = (By.CLASS_NAME, "smart-button-main")
    car_screen_map = (By.CLASS_NAME, "order-header-title")



    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_route(self, address_from, address_to):
        self.set_from(address_from)
        self.set_to(address_to)

    def click_get_taxi(self):
        self.driver.find_element(*self.button_get_taxi).click()
        self.driver.find_element(*self.confort_button).click()
    def blanket_and_tissue_displayed(self):
        return self.driver.find_element(*self.blanket_and_tissue_confort).is_displayed()

    def add_phone_number(self):
        self.driver.find_element(*self.phone_number_button).click()
        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(self.phone_number_field)
        )
        self.driver.find_element(*self.phone_number_field).send_keys(data.phone_number)
        self.driver.find_element(*self.button_siguiente).click()
        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(self.code_field)
        )
        self.driver.find_element(*self.code_field).send_keys(retrieve_phone_code(self.driver))
        time.sleep(2)
        self.driver.find_element(*self.button_confirm).click()

    def imput_con_numero(self):
        return self.driver.find_element(*self.phone_field_text).text

    def select_add_payment(self):
        self.driver.find_element(*self.payment_method_field).click()
        self.driver.find_element(*self.button_plus_card).click()
        card_field = WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(self.add_card_field))
        card_field.click()
        card_field.send_keys(data.card_number)
        card_field.send_keys(Keys.TAB)
        card_cvv = WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(self.add_code_card))
        card_cvv.click()
        time.sleep(1)
        card_cvv.send_keys(data.card_code)
        card_cvv.send_keys(Keys.TAB)
        self.driver.find_element(*self.agregar_tarjeta_button).click()
        self.driver.find_element(*self.cerrar_payment_button).click()
    def get_tarjeta_agregada_text(self):
        return self.driver.find_element(*self.tarjeta_agregada_text).text

    def mandar_mensaje_controlador(self):
        self.driver.find_element(*self.select_mensaje_driver).click()
        self.driver.find_element(*self.mensaje_field).send_keys(data.message_for_driver)
    def get_mensaje_para_controlador(self):
        return self.driver.find_element(*self.mensaje_field).get_property('value')

    def click_select_blanket_tissue(self):
        self.driver.find_element(*self.select_blanket_and_tissue).click()
    def get_blanket_tissue(self):
        return self.driver.find_element(*self.confirm_blanket_and_tissue).is_selected()

    def add_two_ice_creams(self):
        self.driver.find_element(*self.add_ice_cream).click()
        time.sleep(1)
        self.driver.find_element(*self.add_ice_cream).click()
        time.sleep(1)
    def set_two_ice_creams(self):
        return self.driver.find_element(*self.selected_two_ice_creams).text

    def click_search_taxi_button(self):
        self.driver.find_element(*self.button_search_taxi).click()
    def open_search_taxi_screen(self):
        return self.driver.find_element(*self.car_screen_map).is_displayed()


class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(5)

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_select_confort(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_get_taxi()
        blanket_and_tissue = routes_page.blanket_and_tissue_displayed()
        assert blanket_and_tissue == True

    def test_filled_phone_number(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.add_phone_number()
        assert routes_page.imput_con_numero() == data.phone_number

    def test_add_payment_card(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.select_add_payment()
        assert routes_page.get_tarjeta_agregada_text() == "Tarjeta"

    def test_send_message(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.mandar_mensaje_controlador()
        assert routes_page.get_mensaje_para_controlador() == data.message_for_driver

    def test_button_blanket_and_tissue(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_select_blanket_tissue()
        assert routes_page.get_blanket_tissue() == True

    def test_add_two_ice_creams(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.add_two_ice_creams()
        assert routes_page.set_two_ice_creams() == "2"

    def test_select_search_taxi(self):
        routes_page = UrbanRoutesPage(self.driver)
        self.driver.implicitly_wait(5)
        routes_page.click_search_taxi_button()
        assert routes_page.open_search_taxi_screen() == True





    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

import allure
from selene import have, by, be


@allure.title("Successful fill form")
def test_successful(setup_browser):
    browser = setup_browser
    first_name = "Alex"
    last_name = "Egorov"

    with allure.step("Open registrations form"):
        browser.open("http://demoqa.com/automation-practice-form")
        browser.element("h5").should(be.visible)
        browser.element("h5").should(have.text("Student Registration Form"))
        browser.driver.execute_script(
            "document.querySelector('footer')?.remove()"        )
        browser.driver.execute_script(
            "document.querySelector('#fixedban')?.remove()"
        )

    with allure.step("Fill form"):
        browser.element("#firstName").set_value(first_name)
        browser.element("#lastName").set_value(last_name)
        browser.element("#userEmail").set_value("alex@egorov.com")



        browser.element("#genterWrapper").element(by.text("Other")).click()

        browser.element("#userNumber").set_value("1231231230")

        browser.element("#subjectsInput").type("Maths").press_enter()

        browser.element("#hobbiesWrapper").element(by.text("Sports")).click()

        browser.element("#currentAddress").set_value("Some street 1")

        browser.element("#state").click()
        browser.element("#stateCity-wrapper").element(by.text("NCR")).click()

        browser.element("#city").click()
        browser.element("#stateCity-wrapper").element(by.text("Delhi")).click()

        browser.element("#submit").click()

    with allure.step("Check form results"):
        browser.element("#example-modal-sizes-title-lg").should(
            have.text("Thanks for submitting the form")
        )
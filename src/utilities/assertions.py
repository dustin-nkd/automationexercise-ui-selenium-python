import allure


def assert_text_contains(actual_text: str, expected_text: str, message: str, driver=None) -> None:
    """
    Assert actual_text contains expected_text
    On failure, attach expected vs actual text and screenshot to Allure
    """
    if expected_text not in actual_text:
        # 1) Attach expected vs actual
        allure.attach(f"EXPECTED:\n{expected_text}\n\nACTUAL:\n{actual_text}",
                      name="expected_vs_actual",
                      attachment_type=allure.attachment_type.TEXT)

        # 2) Attach current URL
        if driver:
            try:
                png = driver.get_screenshot_as_png()

                if png and len(png) > 1000:
                    allure.attach(png,
                                  name="assertion_failure_screenshot",
                                  attachment_type=allure.attachment_type.PNG)
                else:
                    allure.attach("Screenshot data is empty or invalid",
                                  name="screenshot_error",
                                  attachment_type=allure.attachment_type.TEXT)
            except Exception as e:
                allure.attach(str(e),
                              name="screenshot_exception",
                              attachment_type=allure.attachment_type.TEXT)

        raise AssertionError(message)
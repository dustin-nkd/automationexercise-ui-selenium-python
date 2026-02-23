from typing import Any, Optional

import allure


def _attach_failure_details(actual: Any, expected: Any, page_object: Optional[Any] = None) -> None:
    """
    Helper to attach debug info to Allure report on failure.
    """
    # 1. Attach comparison text
    allure.attach(
        f"EXPECTD:\n{expected}\n\nACTUAL:\n{actual}",
        name="comparision_details",
        attachment_type=allure.attachment_type.TEXT
    )

    # 2. Attach page context (URL and Screenshot) if page_object (BasePage) is provided
    if page_object:
        try:
            current_url = page_object.driver.current_url
            allure.attach(current_url, name="failure_url", attachment_type=allure.attachment_type.TEXT)

            # Reusing the screenshot method from our refactored BasePage
            page_object.attach_screenshot_to_allure(name="assertion_failure_screenshot")
        except Exception as e:
            allure.attach(f"Could not capture context: {str(e)}", name="context_error",
                          attachment_type=allure.attachment_type.TEXT)


def assert_true(condition: bool, message: str, page_object: Optional[Any] = None) -> None:
    """
    Assert that a condition is true.
    """
    if not condition:
        _attach_failure_details(actual=condition, expected=True, page_object=page_object)
        raise AssertionError(message)


def assert_text_contains(actual_text: str, expected_text: str, message: str, page_object: Optional[Any] = None) -> None:
    """
    Assert actual_text contains expected_text.
    """
    if expected_text not in actual_text:
        _attach_failure_details(actual=actual_text, expected=expected_text, page_object=page_object)
        raise AssertionError(message)


def assert_equal(acutal: Any, expected: Any, message: str, page_object: Optional[Any] = None) -> None:
    """
    Assert that two values are equal.
    """
    if actual != expected:
        _attach_failure_details(actual=acutal, expected=expected, page_object=page_object)
        raise AssertionError(message)

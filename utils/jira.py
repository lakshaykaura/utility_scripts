import os

from rich.console import Console
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
import utils.common as common_utils
import utils.date as date_utils

env_jira_pass = os.environ.get("JIRA_PASS")

console = Console()

JIRA_ID = "Jira Id"


def login_to_jira(driver, timeout):
    """
    Logs into a JIRA instance using provided credentials and a Selenium WebDriver.

    This function navigates to the JIRA login page, inputs the username and password into the respective fields, and submits the form. It waits until the dashboard is loaded, indicating a successful login, based on a specified timeout. The zoom level of the browser is also adjusted for better visibility of the elements during automation.

    Parameters:
    - driver (selenium.webdriver.Chrome): The Selenium WebDriver instance used to control the browser.
    - timeout (int): The maximum time, in seconds, to wait for the JIRA dashboard to be loaded after submitting the login form.

    Note: The username is hardcoded, and the password is obtained from an environment variable. Adjust these as necessary to suit your security practices.
    """
    driver.get("https://atlassian.hcehbs.org:8443/login.jsp")
    username_field = driver.find_element(By.ID, "login-form-username")
    password_field = driver.find_element(By.ID, "login-form-password")
    username_field.send_keys("lkaura")
    password_field.send_keys(env_jira_pass)
    password_field.send_keys(Keys.RETURN)
    WebDriverWait(driver, timeout).until(
        ec.presence_of_element_located((By.ID, "dashboard"))
    )
    driver.maximize_window()
    driver.execute_script("document.body.style.zoom='85%'")


def navigate_to_jira_issue_filter_page(driver, timeout):
    """
    Navigates to a specific JIRA issue filter page and switches the view to list view.

    This function opens a predefined JIRA issue filter page using its URL. After the page loads, it waits for the layout switcher button to become clickable, clicks it to open the layout options, and then selects the "List View" option from the layout choices. It waits until the issues table in list view is visible, indicating the view has successfully switched and the issues are loaded.

    Parameters:
    - driver (selenium.webdriver.Chrome): The Selenium WebDriver instance used to control the browser.
    - timeout (int): The maximum time, in seconds, to wait for each expected condition to be met during the navigation process.

    Note: The URL used in `driver.get` includes a specific filter ID (`filter=10657`). Adjust this filter ID as necessary to suit your specific JIRA setup and desired filter.
    """
    driver.get("https://atlassian.hcehbs.org:8443/issues/?filter=10657")
    layout_switcher_button = WebDriverWait(driver, timeout).until(
        ec.element_to_be_clickable((By.CSS_SELECTOR, "button#layout-switcher-button"))
    )
    layout_switcher_button.click()
    list_view_option = WebDriverWait(driver, timeout).until(
        ec.element_to_be_clickable(
            (
                By.CSS_SELECTOR,
                "div#layout-switcher-options ul li a.aui-list-item-link[data-layout-key=list-view]",
            )
        )
    )
    list_view_option.click()
    WebDriverWait(driver, timeout).until(
        ec.visibility_of_all_elements_located(
            (By.CSS_SELECTOR, "table#issuetable tbody tr td")
        )
    )


def wait_for_jira_resultset_to_refresh(driver, timeout):
    """
    Waits for the JIRA issues table to refresh by monitoring a specific class indicator.

    This function checks for the JIRA issues result set refresh by waiting for a 'browser-metrics-stale' class to be added and then removed from the issues table, indicating that the table is being refreshed. It first waits for the class to appear, signaling the start of the refresh process. If this class does not appear within the specified timeout, it assumes the table might have already been refreshed. Then, it waits for the class to disappear, which indicates that the refresh has completed and the results have been updated.

    Parameters:
    - driver (selenium.webdriver.Chrome): The Selenium WebDriver instance used for the automation.
    - timeout (int): The maximum time, in seconds, to wait for each part of the refresh process.

    Exceptions:
    - TimeoutException: If the 'browser-metrics-stale' class does not appear or disappear within the specified timeout, a message is printed to the console indicating the potential state of the refresh process.

    Note: This function uses the `console.print` method from the `rich.console` module to print status messages. Ensure that a `console` instance is available in the script.
    """
    try:
        # Wait for the 'browser-metrics-stale' class to be added to the table
        WebDriverWait(driver, timeout).until(
            ec.presence_of_element_located(
                (By.CSS_SELECTOR, "table#issuetable.browser-metrics-stale")
            )
        )
        console.print(
            "[cyan]Stale class detected, Jira is refreshing results...[/cyan]"
        )
    except TimeoutException:
        console.print(
            "[red]Stale class not detected within timeout; Jira might have already refreshed results.[/red]❌"
        )

    try:
        # Wait for the 'browser-metrics-stale' class to be removed, indicating refresh
        WebDriverWait(driver, timeout).until_not(
            ec.presence_of_element_located(
                (By.CSS_SELECTOR, "table#issuetable.browser-metrics-stale")
            )
        )
        console.print(
            "[yellow]Table refresh detected, the results have been updated...[/yellow]"
        )
    except TimeoutException:
        console.print(
            "[red]Table refresh not detected within timeout; Jira might have already refreshed results.[/red]❌"
        )


def update_jql_query_with_jira_ids(driver, jira_id_to_row_map):
    """
    Updates the JQL query in a JIRA instance with a set of JIRA IDs and executes the search.

    This function modifies the current JQL query in the JIRA issue search page to include an additional 'OR' condition, listing specific JIRA IDs obtained from `jira_id_to_row_map`. The updated query aims to filter issues by these IDs. If the original JQL query contains an 'ORDER BY' clause, it is preserved in the updated query. The function then triggers the search to apply the updated JQL query.

    Parameters:
    - driver (selenium.webdriver.Chrome): The Selenium WebDriver instance used for the automation.
    - jira_id_to_row_map (dict): A dictionary mapping JIRA IDs (str) to their corresponding row numbers in an Excel sheet. Only the keys (JIRA IDs) are used to update the JQL query.

    Note: Ensure that the JIRA web interface elements (like the JQL text area and search button) match the selectors used in this function. Adjust the selectors as necessary to align with any updates to the JIRA web interface.
    """
    jql_textarea = driver.find_element(By.ID, "advanced-search")
    current_jql = jql_textarea.get_attribute("value")

    jira_ids_str = ",".join(
        [f"'{jid}'" for jid in jira_id_to_row_map.keys() if jid is not None]
    )

    if jira_id_to_row_map:
        # Split the JQL query to separate the ORDER BY clause if it exists
        parts = current_jql.rsplit(" ORDER BY ", 1)
        if len(parts) == 2:
            # Extract the base JQL and the ORDER BY clause
            base_jql, order_by_clause = parts

            # Find the last closing parenthesis in the base JQL to insert the OR condition
            last_paren_index = base_jql.rfind(")")
            if last_paren_index != -1:
                # Insert the OR condition just before the last closing parenthesis
                updated_jql = (
                    f"{base_jql[:last_paren_index]} OR id in ({jira_ids_str}){base_jql[last_paren_index:]} "
                    f"ORDER BY {order_by_clause}"
                )
            else:
                # If no closing parenthesis is found, append the condition at the end
                updated_jql = (
                    f"{base_jql} OR id in ({jira_ids_str}) ORDER BY {order_by_clause}"
                )
        else:
            base_jql = parts[0]
            updated_jql = f"{base_jql} OR id in ({jira_ids_str})"
    else:
        updated_jql = current_jql

    jql_textarea.clear()
    jql_textarea.send_keys(updated_jql)

    search_button = driver.find_element(
        By.CSS_SELECTOR, "button.aui-button.aui-button-primary.search-button"
    )
    search_button.click()


def get_property_from_issue_html(issue, property_class, attribute=None):
    """
    Extracts a specified property's value from a JIRA issue's HTML element.

    This function attempts to locate an HTML element within a JIRA issue's web page representation by its CSS selector (`property_class`). If found, the function then extracts either the text content of the element or a specified attribute's value. This is useful for scraping specific pieces of information from JIRA issue pages, such as titles, descriptions, statuses, etc.

    Parameters:
    - issue (selenium.webdriver.remote.webelement.WebElement): The web element representing the JIRA issue, typically obtained from a list of issues on a search results page.
    - property_class (str): The CSS selector used to locate the target element within the issue's HTML.
    - attribute (str, optional): The name of the attribute from which to extract the value. If not provided, the text content of the element is extracted instead.

    Returns:
    - str: The stripped text content of the found element or the value of the specified attribute. If the element is not found or an error occurs, an empty string is returned.

    Exceptions:
    - AttributeError: If the element found does not have the requested attribute.
    - NoSuchElementException: If no element matching the CSS selector is found within the issue's HTML.
    """
    try:
        element = issue.find_element(By.CSS_SELECTOR, property_class)
        if attribute:
            return element.get_attribute(attribute).strip()
        else:
            return element.text.strip()
    except (AttributeError, NoSuchElementException):
        return ""


def fetch_and_add_issue_details_in_dataframe(issue):
    """
    Extracts detailed information from a JIRA issue's HTML and organizes it into a dictionary,
    along with a flag indicating whether an exception occurred during the process.

    This function attempts to scrape various pieces of issue-related information from the HTML
    representation of a single JIRA issue. It utilizes helper functions to extract text and attribute
    values from specified HTML elements, formatting certain data types into a standardized form.
    The extracted information is compiled into a dictionary. Additionally, the function tracks the
    success of the operation using a boolean flag that indicates whether any exceptions were encountered.

    Parameters:
    - issue (selenium.webdriver.remote.webelement.WebElement): The web element representing
      the JIRA issue, typically obtained from iterating over a list of issues on a search results page.

    Returns:
    - tuple: A 2-tuple where the first element is a dictionary containing key information extracted from
      the issue (such as JIRA ID, title, and other metadata), and the second element is a boolean flag
      (`exception_occurred`) indicating whether an exception occurred during the extraction process.

    The function initializes `exception_occurred` to False at the beginning and sets it to True if any
    exceptions are caught during the execution. This approach allows calling code to easily determine
    the success of the operation and handle any errors accordingly.
    """
    exception_occurred = False
    try:
        jira_id = get_property_from_issue_html(issue, "td.issuekey a", "data-issue-key")
        title = get_property_from_issue_html(issue, "td.summary p a")
        details = get_property_from_issue_html(issue, "td.customfield_10403")
        description = get_property_from_issue_html(issue, "td.description")
        severity = get_property_from_issue_html(issue, "td.customfield_10501")
        sprint = get_property_from_issue_html(issue, "td.customfield_10109")
        status = common_utils.get_sentence_case(
            get_property_from_issue_html(issue, "td.status span")
        )
        sdlc_status = common_utils.get_sentence_case(
            get_property_from_issue_html(issue, "td.customfield_10412 div span")
        )
        created = get_property_from_issue_html(
            issue, "td.created span time", "datetime"
        )
        assignee = get_property_from_issue_html(issue, "td.assignee span span a")
        priority = get_property_from_issue_html(issue, "td.priority image", "alt")
        reporter = get_property_from_issue_html(issue, "td.reporter span span a")
        lead = get_property_from_issue_html(issue, "td.customfield_10604")
        defect_type = get_property_from_issue_html(issue, "td.customfield_10400")
        environment = get_property_from_issue_html(issue, "td.customfield_10402")
        epic_link = get_property_from_issue_html(issue, "td.customfield_10108 a")
        if (
            (not environment or "FHI" in environment or "OPM" in environment)
            and not assignee
            and not lead
        ):
            in_queue = "N"
        else:
            in_queue = "Y"

        return {
            JIRA_ID: jira_id,
            "Title": title,
            "Details": details,
            "Description": description,
            "Severity": severity,
            "Priority": priority,
            "Sprint": sprint,
            "Defect Type": defect_type,
            "Environment": environment,
            "Epic Link": epic_link,
            "Reporter": common_utils.modify_assignee(reporter),
            "Status": status,
            "SDLC Status": sdlc_status,
            "Assignee": common_utils.modify_assignee(assignee),
            "Lead": common_utils.modify_assignee(lead),
            "Create Date": date_utils.parse_date(created),
            "InQueue": in_queue,
        }, exception_occurred
    except Exception as e:
        exception_occurred = True
        console.print(
            "[red]Error occurred while creating issue details data frame for issue: "
            + issue
            + f"{e}[/red] ❌"
        )
        return {}, exception_occurred


def extract_issue_details_from_jira(driver, timeout):
    """
    Waits for a JIRA issues result set to refresh and then extracts the issue elements from the page.

    This function first calls a custom wait function to ensure the JIRA issues table is in a refreshed state.
    It then waits for the visibility of at least one row in the issues table, indicating that search results are present.
    If the search results are successfully loaded within the specified timeout, the function proceeds to extract all
    visible issue rows from the table. If the results are not loaded within the timeout, it logs an error message and
    sets an `exception_occurred` flag to True.

    Parameters:
    - driver (selenium.webdriver.Chrome): The Selenium WebDriver instance used for automation.
    - timeout (int): The maximum time, in seconds, to wait for the issues table to refresh and for at least
      one row to become visible.

    Returns:
    - tuple: A 2-tuple containing a list of WebElement instances each representing a row in the issues table, and
      a boolean flag (`exception_occurred`) indicating whether any exceptions were encountered (e.g., if the search
      results did not become visible within the specified timeout).

    This approach enables the calling code to handle situations where the issues table might not be available or
    visible due to network issues, page load delays, or other factors, by checking the `exception_occurred` flag.
    """
    exception_occurred = False
    # Use the custom wait function
    wait_for_jira_resultset_to_refresh(driver, timeout)

    # Finally, wait for at least one row in the table to become visible
    try:
        WebDriverWait(driver, timeout).until(
            ec.visibility_of_element_located(
                (By.CSS_SELECTOR, "table#issuetable tbody tr td")
            )
        )
        console.print(
            "[green]Search results are visible, proceeding to extract issues and their details...[/green]"
        )
    except TimeoutException as e:
        exception_occurred = True
        console.print(
            f"[red]Failed to detect search results within the expected timeout. {e}[/red] ❌"
        )

    # Extract issue details
    issues = driver.find_elements(By.CSS_SELECTOR, "table#issuetable tbody tr")
    return issues, exception_occurred

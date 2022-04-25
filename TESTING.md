# Knot Art - Testing documentation
---
*This file contains the Testing section of the [full README.md file for Knot Art](README.md).*

## Table of Contents
---
- [Testing](#testing)
  * [Code Validation](#code-validation)
  * [Test Cases - user stories](#test-cases---user-stories)
  * [Features Testing](#features-testing)
  * [Other Manual Testing](#other-manual-testing)
  * [Automated Testing](#automated-testing)
  * [Fixed Bugs](#fixed-bugs)
  * [Known Bugs](#known-bugs)
  * [Supported Screens and Browsers](#supported-screens-and-browsers)

  ## Testing
---
### Code Validation
#### CSS
The [W3C CSS Validation Service](https://jigsaw.w3.org/css-validator/) was used to validate the project's custom CSS. [Each CSS file passes and the results can be viewed here](docs/code-validation/css-validation.pdf). Note: there are Warnings for the base.css file and these are explained below:
- `Same color for background-color and border-color`. I have used border colour same as background colour on some of the btns because either 1) on hover the background colour and border colour are different, so to keep the button size consistent between default and hover state and 2) in cases where two buttons are shown beside each other, one outlined and one solid colour. If the solid coloured button doesn't have a border then the buttons appear as different sizes, so keeping the border on the solid coloured button makes them consistent.
- `::-webkit-datetime-edit is a vendor extended pseudo-element`. I have used this vendor pseudo element to target the date and time 'placeholders' on the market form, in order to style them the same as other placeholder text. I understand that the vendor extensions are not programmed into the CSS validator and therefore they come up as a warning.

#### JavaScript
[JSHint](https://jshint.com/) was used to check the quality of the JavaScript code and check for errors. The errors raised were as follows:
- `Missing semicolon` errors were rectified
- `Functions declared within loops referencing an outer scoped variable may lead to confusing semantics.`. This error was raised in relation to a `for of` loop in the `handleQuantityInput()` function in script.js and in the `checkStartAndEndTimes()` function in form_validation.js in the markets app. I amended these loops to `forEach`.

There are no errors remaining and [the final results of the JSHint checks on each file can be viewed here](docs/code-validation/javascript-validation.pdf).

#### Python
[PEP8 online checker](http://pep8online.com/) was used to validate the Python code for all files created by me. Django standard files have not been validated or amended in relation to line length errors since these are standard Django files. The results of the validation for each app and for the overall project files are linked below:
- [cart app PEP8 validation results](docs/code-validation/cart-app-python-validation.pdf)
- [checkout app PEP8 validation results](docs/code-validation/checkout-app-python-validation.pdf)
- [home app PEP8 validation results](docs/code-validation/home-app-python-validation.pdf)
- [markets app PEP8 validation results](docs/code-validation/markets-app-python-validation.pdf)
- [products app PEP8 validation results](docs/code-validation/products-app-python-validation.pdf)
- [profiles app PEP8 validation results](docs/code-validation/profiles-app-python-validation.pdf)
- [project level file PEP8 validation results](docs/code-validation/project-level-files-python-validation.pdf)

### Test Cases - user stories

### Features Testing

### Other Manual Testing

### Automated Testing
#### Python tests
Automated testing was carried out on the Python code in each of the six apps. Tests were written as each feature or user story was developed in each iteration, in line with the Agile approach used for the project development. The tests were ran and the feature was not closed until the tests passed. Tests were written for models, views and forms.

On completion of the project, all tests were ran again to ensure they still passed and the results of these are shown below. The tests that were written are contained in the relevant `test_forms.py`, `test_views.py` and `test_models.py` files in each app.

- cart app automated test results - test_views
![cart app automated test results](docs/automated-testing/cart-app-automated-tests.png)

- checkout app automated test results - test_forms, test_models, test_views
![checkout app automated test results](docs/automated-testing/checkout-app-automated-tests.png)

- home app automated test results - test_views
![home app automated test results](docs/automated-testing/home-app-automated-tests.png)

- markets app automated test results - test_forms, test_models, test_views
![markets app automated test results](docs/automated-testing/markets-app-automated-tests.png)

- products app automated test results - test_forms, test_models, test_views
![products app automated test results](docs/automated-testing/products-app-automated-tests.png)

- profiles app automated test results - test_forms, test_models, test_views
![profiles app automated test results](docs/automated-testing/profiles-app-automated-tests.png)

#### Coverage
The [coverage](https://coverage.readthedocs.io/en/6.2/) tool was used after user stories had been completed, to determine the effectiveness of the tests. 

On the initial run, some of the apps were below 100% and some more tests were added as outlined below:

**- cart app:**

The initial coverage report was 99% as shown below:
![cart app coverage report](docs/automated-testing/cart-app-coverage-initital.png)

The report showed a test missing for `__init__.py` file in the `templatetags` folder:

![cart app coverage missing test](docs/automated-testing/cart-app-missing-test.png)
On investigation there should not have been any code in the `__init__.py` file, this code was already in the cart_tools.py file and had somehow been duplicated into the `__init__.py` file. Removed this code from `__init__.py` file and also wrote a test to cover off on testing the `calc_subtotal` custom templatetag. The final coverage for this app is now 100% as shown in the [Final coverage reports section below](#final-coverage-reports) 

**- profiles app:**

The initial coverage report was 99% as shown below:
![profiles app coverage report](docs/automated-testing/profiles-app-coverage-initial.png)

The report showed tests missing for `views.py`:

![profiles app coverage missing tests](docs/automated-testing/profiles-app-missing-tests.png)

Tests were added to cover off on these (invalid profile form, error message raised and test for if user has no saved markets) The final coverage for this app is now 100% as shown in the [Final coverage reports section below](#final-coverage-reports) 

**- checkout app:**

The initial coverage report was 72% as shown below:
![checkout app coverage report](docs/automated-testing/checkout-app-coverage-initial.png)

The report showed tests missing for `signals.py` `views.py`:
![checkout app coverage missing tests](docs/automated-testing/checkout-app-missing-tests.png)
Tests were added to cover off on the missing test for `signals.py`. Further tests were added for the `checkout_success` view, `cache_checkout_data` view and the get request part of the `checkout` view from `views.py`. The final coverage for this app is now 82% as shown in the [Final coverage reports section below](#final-coverage-reports). The [remaining tests in views.py](docs/automated-testing/checkout-app-remaining-missing-tests.png) need Stripe to be mocked for the post part of the `checkout` view, and for the `cache_checkout_data` view where it interacts with Stripe via the `stripe_elements.js` script. And also to test the webhooks.py and webhook_handler.py. On discussion with my mentor, this would be a future learning for me to complete, however manual testing has been completed on the Stripe webhooks and on the post part of the checkout view and cache_checkout_data view during development. 

##### Final coverage reports
As shown below, the final coverage report shows 100% coverage for the cart, home, markets, products and profiles apps. The checkout app has 82% coverage. Overall coverage is 96%.

- cart app coverage report

![cart app coverage report](docs/automated-testing/cart-app-coverage-report.png)

- checkout app coverage report

![checkout app coverage report](docs/automated-testing/checkout-app-coverage-report.png)

- home app coverage report

![home app coverage report](docs/automated-testing/home-app-coverage-report.png)

- markets app coverage report

![markets app coverage report](docs/automated-testing/markets-app-coverage-report.png)

- products app coverage report

![products app coverage report](docs/automated-testing/products-app-coverage-report.png)

- profiles app coverage report

![profiles app coverage report](docs/automated-testing/profiles-app-coverage-report.png)

- overall coverage report

![overall coverage report](docs/automated-testing/overall-coverage-report.png)

To run the coverage report to see any further details, do the following in the IDE command line:
1. install coverage: `pip3 install coverage`
2. run coverage on specific app: `coverage run --source=appname manage.py test` e.g. for the products app it would be `coverage run --source=products manage.py test` (or to run for entire project use `coverage run manage.py test`)
4. generate the report (displays report in command line): `coverage report`
5. generate an interactive html version of the report that can be viewed in the browser: `coverage html`
6. view the report: `python3 -m http.server`. Open the port 8000 when it pops up, click on `htmlcov/` lin the Directory listing and then click on the specific module to see further details.

#### JavaScript tests
Since there is only a small amount of JavaScript code used in the project, the testing carried out for these functions was manual testing only, as part of the User Stories and Features testing described above.

### Fixed Bugs
- **Issue: On cart page can add more than max allowed**
![Cart page allows more than 10 to be added bug](docs/bugs/cart-page-max-qty-bug.png)
On the Cart the Qty buttons don't allow a user to increase quantity higher than 10 (max quantity allowed), but a user can manually type in a higher number, and after pressing Update quantity, the bag updates as normal as shown above.
> Solution: The issue was because the Update quantity is handled by jQuery using the `.submit()` method, and not by a form submit button (a form submit button would trigger the HTML form validation). The `.submit()` method called on the form does not trigger constraint validation. However the `.requestSubmit()` method *does* trigger constraint validation, so the function was updated to use `.requestSubmit()` instead of `.submit()`, as shown below. I found this solution through a post on the Code Institute Slack dev-tips-library channel by [Igor Basuga](https://github.com/bravoalpha79) where he described investigating a similar bug and the solution. I had read the post and remembered it, I knew this bug was because of the form submit being prevented but I would likely have come up with a much more complicated solution had I not remembered this post!
```javascript
function submitQuantityUpdateForm() {
    if($('.update-link')) {
        $('.update-link').click(function() {
            $(this).prev('.update-form')[0].requestSubmit();
        });
    }
}

```
After this change the validation is triggered and an error is shown if the quantity is outside the range:

![Cart page allows more than 10 to be added - resolved](docs/bugs/cart-page-max-qty-fixed.png)


### Known Bugs

### Supported Screens and Browsers
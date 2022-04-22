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

### Test Cases - user stories

### Features Testing

### Other Manual Testing

### Automated Testing

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
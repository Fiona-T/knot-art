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
#### HTML
The [W3C Markup Validation Service](https://validator.w3.org/) was used to validate the HTML on every page of the project. Validation was done using url for pages that did not need a sign in, and by copying the results of 'View Page Source' into the Direct Input field of the validator for pages that require a log in.

The errors that were raised and fixes done are as follows:
- On pages that used the Custom Clearable File Input for the image upload, there was a `duplicate attribute` error, there were two id attributes on the `input` element. This arose because an id was added to the` input` element in `custom_clearable_file_input.html`, but Django auto adds an id to each input when generating the model form. I removed the id from the `custom_clearable_file_input.html`, and since this id was being used in the `fileInputShowFileName` function (to listen for a change and show the file name of the new image), updated the id in this function also.
![Duplicate id attribute html validation error](docs/code-validation/duplicate-id-html-validation-error.png)

- On pages using the breadcrumb menu, there was an error due to placement of a `span` between two `li` elements. The `span` was here to replace the Bootstrap default divider between breadcrumb items, removed this and over-rode the divider in the css instead.
![span element child of ul, html validation error](docs/code-validation/span-child-of-ul-html-validation-error.png)

- On the delete comment modal, there was an error in relation to missing a closing `p` tag. While the closing `p` tag was not missing in the typed code, the error was arising because of the `|linebreaks` Django filter, that automatically creates `p` tags. Remove the `p` tags surrounding this (as they generate by the filter) to clear this error.
![missing p tag, html validation error](docs/code-validation/missing-p-tag-html-validation-error.png)

There is one warning remaining due to using a h1 element in a section but not a direct child of a section. There are divs between the section and the h1, for layout and spacing and for consistency across pages. 

The [results of validating each HTML page can be viewed here](docs/code-validation/html-validation.pdf).

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
*Note:* testing of the user stories was carried out while each user story/feature was developed, to ensure acceptance criteria were met before the issue was closed. The below documents the user story testing that was completed at the end of the project, again grouped under the same headings as outlined in the User Stories section. 

#### General, site purpose, navigation:
- [#1](https://github.com/Fiona-T/knot-art/issues/1) As a visiting user, I can easily find out what the purpose of the website is and learn more about the site owner and the products being sold, so that I  can decide to stay and browse or not
    *  Acceptance Criteria 1:  The first thing the user should see on entering the website is an image which sets the tone of the website and a tagline explaining the purpose of the website
    *  Acceptance Criteria 2: There should be a learn more button, which will link to the information about the maker and the website
    *  Acceptance Criteria 3: There should be a 'Shop now' button which will link to the shop, the primary purpose of the website
    * Acceptance Criteria 4: Below the main image, there should be a section explaining to users what the website is for, and introducing the website owner who makes the products
  >**Result:** Pass, the above acceptance criteria are met, as shown below:
![User story - site purpose](docs/user-story-testing/site-purpose.png)

- [#2](https://github.com/Fiona-T/knot-art/issues/2) As a site user, I can navigate the site so that I can find the page I want to go to
    *  Acceptance Criteria 1:  There should be a site header which is at the top of every page on the website
    *  Acceptance Criteria 2: The logo (website name) should be prominent in the header and it should link back to the home page
    *  Acceptance Criteria 3: The header should contain navigation links to the Shop, Markets and Account, and Cart pages.
    >**Result:** Pass, above acceptance criteria are met, as shown below in the screenprint for the previous user story. Logo downsizes to a 'K' on smaller screens to allow more space for menu items. Logo links to home page. Header is present on all pages and fixed to top.

- [#3](https://github.com/Fiona-T/knot-art/issues/3) As a site user, I can find the Knot Art social media accounts, so that I can follow them on social media to keep up to date
    *  Acceptance Criteria 1:  The links to the social media accounts should be in the footer on each page, represented by their icons
    *  Acceptance Criteria 2: The links are external, so open in a new window
    *  Acceptance Criteria 3: The links are for the Facebook business page, Twitter, Instagram and LinkedIn
    >**Result:** Pass, acceptance criteria met. Footer present on all pages with social media links. Links open in new window.
    ![User story - social media links](docs/user-story-testing/social-media-links.png)

- [#4](https://github.com/Fiona-T/knot-art/issues/4) As a site user, I can sign up to the newsletter, so that I can stay informed  and stay engaged with the shop
    *  Acceptance Criteria 1:  The footer on each page should contain a form to sign up for the newsletter
    *  Acceptance Criteria 2: The form consists of one field for email address, and a button to sign up
    *  Acceptance Criteria 3:  After submitting the form, the email address submitted is added to the subscribers list in mailchimp
    >**Result:** Pass, the above acceptance criteria are met, as shown below:
    ![User story - newsletter sign up](docs/user-story-testing/newsletter-sign-up.png)

- [#5](https://github.com/Fiona-T/knot-art/issues/5) As a site user, I can see a 'Page not found' page with consistent branding to the rest of the site, when I try to access a page in error, so that I can find my way back to the website and know I have not left the website
    *  Acceptance Criteria 1:  the 404 page not found that is displayed to the user is consistent with the branding on the rest of the website
    *  Acceptance Criteria 2: the page contains the header and footer as per the rest of the website
    *  Acceptance Criteria 3: the page contains a short note to the user explaining the page wasn't found, along with links for them to get back to the main website
    >**Result:** Pass, the above acceptance criteria are met, as shown below:
    ![User story - 404 page](docs/user-story-testing/404-page.png)

- [#6](https://github.com/Fiona-T/knot-art/issues/6) As a site user, I can find the terms of use and privacy policy so that I can read these documents and have trust in the site
    *  Acceptance Criteria 1:  The links to the Terms of Use and Privacy Policy are present in the footer on each page
    *  Acceptance Criteria 2:  The links are internal so open in same window
    *  Acceptance Criteria 3: Each link contains the correct policy
    >**Result:** Pass, the above acceptance criteria are met, as shown below. The links are present in the footer as shown in previous user stories. Both links open internally as modals. There are buttons at both top and bottom to close the modal. Both documents also provide a link to read the relevant policy in a new window. 
    ![User story - Privacy Policy and Terms of Use](docs/user-story-testing/privacy-policy-terms-of-use.png)

- [#52](https://github.com/Fiona-T/knot-art/issues/52) As a user I can click on a back to top button so that I can get back to the top of the page without having to scroll
    *  Acceptance Criteria 1:  On the Shop page where products are listed, there is a back to top button fixed to bottom of the screen
    *  Acceptance Criteria 2: Clicking the button brings the user back to the top of the page
    >**Result:** Pass, the above acceptance criteria are met, as shown below. The button is present on the Shop page, and also on the Markets/My Markets page, and for mobile on the Cart page since this can be a long page on mobile. (the user story was added specifically for the Shop page as that had been developed at that stage - this feature was automatically included with the other pages when they were created, when relevant)
    ![User story - Back to top button](docs/user-story-testing/back-to-top-button.png)

- [#53](https://github.com/Fiona-T/knot-art/issues/53) As a user I can see a message confirming my actions (e.g. adding item to bag) so that I know my changes were received
    *  Acceptance Criteria 1:  when a user performs actions that interact with the site, a message is displayed confirming the action was successful, or if there were errors
    *  Acceptance Criteria 2: E.g. in the search box on Shop page, if no search items entered it generates an error message
    *  Acceptance Criteria 3: Or for adding, removing, adjusting quantity of items in the shopping cart
    >**Result:** Pass, the above acceptance criteria are met, as shown below. Messages are displayed for all user actions, either success/error/info. If there are items in the bag and the user is on the cart page or adding a product then the bag summary is shown in the message. If not, then just the message (as bag summary not relevant for other actions). Samples of messages are shown below.
    ![User story - confirmation messages](docs/user-story-testing/confirmation-messages.png)

- [#62](https://github.com/Fiona-T/knot-art/issues/62) As a user I can see a page styled the same way as the website when I get a server error or access denied so that I can find my way back to the correct page on the website
    *  Acceptance Criteria 1:  the pages displayed to the user for a 403 (permission denied), and 500 (server error) are consistent with the branding on the rest of the website
    *  Acceptance Criteria 2: the pages contain the header and footer as per the rest of the website
    *  Acceptance Criteria 3: the pages contains links for them to get back to the main website
    Note: 404 page already covered under previous user story: #5 
    >**Result:** Pass, the above acceptance criteria are met, as shown below
    ![User story - error pages](docs/user-story-testing/error-pages.png)

- [#91](https://github.com/Fiona-T/knot-art/issues/91) As a user I can quickly see which section of the website I am in from the main header so that I know which part of the website I am in and can navigate easily
    *  Acceptance Criteria 1:  The icon and text for each section of the website in the header change to a different colour when a user is on a page within that section of the website
    *  Acceptance Criteria 2: E.g. in markets, market details then Markets menu item will be a different colour
    *  Acceptance Criteria 3: For the superuser, when editing/adding a product or a market, the menu item will be Shop or Markets respectively since they are in this section of the website. (There are menu options from the Account dropdown for these pages, but they are not part of the user profile so the active menu item will be either Shop or Markets as appropriate)
    >**Result:** Pass, the above acceptance criteria are met, as shown in the screenprints for the previous user stories. The menu icon is highlighted in white when the user is on a page in that sectio of the website.

#### Shop - viewing products
- [#7](https://github.com/Fiona-T/knot-art/issues/7) As a site user, I can easily view all the products in the shop so that I can see all the available products immediately without having to sort or filter or take any action
- [#8](https://github.com/Fiona-T/knot-art/issues/8) As a site user, I can view an individual item details so that I can see the full details including the description and decide whether to buy
- [#9](https://github.com/Fiona-T/knot-art/issues/9) As a site user, I can select a specific category of product so that I can view just the items in that category to make it easier to make a decision
- [#10](https://github.com/Fiona-T/knot-art/issues/10) As a site user, I can sort the products in the shop so that I can find what I'm looking for more easily
- [#11](https://github.com/Fiona-T/knot-art/issues/11) As a site user, I can search for a product in the shop so that I can find a particular item quickly
- [#71](https://github.com/Fiona-T/knot-art/issues/71) As a user I can see the results for my filter option or search term so that I can quickly see how many products match my filter option/match my search term

#### Shop - adding to/updating the cart
- [#12](https://github.com/Fiona-T/knot-art/issues/12) As a site user, I can add an item to my cart so that I can buy it
- [#13](https://github.com/Fiona-T/knot-art/issues/13) As a site user, I can select the quantity of an item before adding to my cart, so that I can add multiple of that item at once
- [#14](https://github.com/Fiona-T/knot-art/issues/14) As a site user I can see the total amount currently in my cart at all times, so that I can keep track of how much I'll be spending
- [#15](https://github.com/Fiona-T/knot-art/issues/15) As a site user I can see the items in my cart at any time, so that I can check what I have already added to the cart
- [#16](https://github.com/Fiona-T/knot-art/issues/16) As a site user I can adjust the quantity of a particular item in the cart so that I can buy more or less of the item directly from the cart
- [#17](https://github.com/Fiona-T/knot-art/issues/17) As a site user, I can remove an item from my cart so that I do not have to buy it if I've changed my mind

#### Shop - payment and check out
- [#18](https://github.com/Fiona-T/knot-art/issues/18) As a site user, I can continue to the checkout process once I've decided on my purchase so that I can buy the items
- [#19](https://github.com/Fiona-T/knot-art/issues/19) As a site user, I can enter my delivery and payment details so that I can complete my purchase
- [#20](https://github.com/Fiona-T/knot-art/issues/20) As a site user, I can see the order summary while making payment so that I can still edit the details before payment if I made a mistake
- [#21](https://github.com/Fiona-T/knot-art/issues/21) As a registered user, I can save my delivery information when checking out so that it is saved to my profile for use with my next order
- [#22](https://github.com/Fiona-T/knot-art/issues/22) As a site user, I can see an order confirmation page so that I know that the order went through okay
- [#23](https://github.com/Fiona-T/knot-art/issues/23) As a site user, I can recieve an email confirmation of my order so that I have this confirmation for my records
- [#54](https://github.com/Fiona-T/knot-art/issues/54) As a user I can see a preview of my shopping cart when I make changes so that I can easily see the new cart
- [#57](https://github.com/Fiona-T/knot-art/issues/57) As a site owner I can ensure that an order is created once payment is made so that a customer does not make a payment, without an order being created in the database

#### Markets - viewing markets
- [#24](https://github.com/Fiona-T/knot-art/issues/24) As a site user, I can easily view all the upcoming markets so that I can plan if I want to attend one of the markets
- [#25](https://github.com/Fiona-T/knot-art/issues/25) As a site user, I can sort the markets list so that I can find what I'm looking for more easily
- [#26](https://github.com/Fiona-T/knot-art/issues/26) As a registered user, I can save a market that I want to go to, so that I don't forget about it as it will be in my profile
- [#27](https://github.com/Fiona-T/knot-art/issues/27) As a registered user, I can see if I have saved a market already when viewing the markets list, so that I know if it's already saved in my profile or not
- [#28](https://github.com/Fiona-T/knot-art/issues/28) As a registered user, I can remove a previously saved market from my profile so that it is no longer in my profile if I don't want to go to it
- [#60](https://github.com/Fiona-T/knot-art/issues/60) As a user I can select a county to filter the markets by so that I can easily see just the markets in that particular county
- [#80](https://github.com/Fiona-T/knot-art/issues/80) As a user I can see how many comments are on a market so that I can decide if I want to read them or not
- [#88](https://github.com/Fiona-T/knot-art/issues/88) As a website owner I can see how many users have saved a market so that I can get an idea of how popular it might be
- [#90](https://github.com/Fiona-T/knot-art/issues/90) As a user I can view markets that are in the past so that I can read the comments on them to get a feel for them if the market runs again

#### Markets - comments
- [#78](https://github.com/Fiona-T/knot-art/issues/78) As a registered user I can add a comment to a market so that I can share my views on a market with other users
- [#81](https://github.com/Fiona-T/knot-art/issues/81) As a user I can read all the comments on a market so that I can see other users' opinions/questions on that market
- [#84](https://github.com/Fiona-T/knot-art/issues/84) As a registered user I can edit a comment that I posted on a market so that I can correct the comment if needed
- [#85](https://github.com/Fiona-T/knot-art/issues/85) As a registered user I can delete a comment that I posted on a market so that I can remove it if I don't want others to see the comment or I posted it in error

#### User account set up, sign in and out
- [#29](https://github.com/Fiona-T/knot-art/issues/29) As a site user, I can sign up for an account, so that I can enjoy the benefits of having an account e.g. saving delivery info
- [#30](https://github.com/Fiona-T/knot-art/issues/30) As a site user, I want to receive an email confirmation when I register, so that I know my account registration was successful and secure
- [#31](https://github.com/Fiona-T/knot-art/issues/31) As a registered user, I can sign into my account so that I can access my profile
- [#32](https://github.com/Fiona-T/knot-art/issues/32) As a registered user, I can sign out of my account when finished, so that I know I am signed out securely
- [#33](https://github.com/Fiona-T/knot-art/issues/33) As a registered user, I can easily see if I am signed into my account or not, so that I know straight away if I need to sign in

#### User profile 
- [#34](https://github.com/Fiona-T/knot-art/issues/34) As a registered user, I can update my default delivery information in my profile, so that the updated details are recorded for future orders
- [#35](https://github.com/Fiona-T/knot-art/issues/35) As a registered user, I can see my previous orders in my profile, so that I can see all the orders I made and can find details of a previous order
- [#36](https://github.com/Fiona-T/knot-art/issues/36) As a registered user, I can see all the markets I saved and view their details so that I have access to this information
- [#37](https://github.com/Fiona-T/knot-art/issues/37) As a registered user, I can remove a previously saved market from my profile so that it is no longer in my profile if I don't want to go to it
- [#58](https://github.com/Fiona-T/knot-art/issues/58) As a registered user I can view details of a previous order so that I can check what was ordered and where it was delivered to
- [#61](https://github.com/Fiona-T/knot-art/issues/61) As a registered user I can sort the markets list in My Markets page so that I can find the market I'm looking for more easily
- [#74](https://github.com/Fiona-T/knot-art/issues/74) As a registered user I can filter my saved markets by county so that I can easily see just my saved markets in that particular county
- [#77](https://github.com/Fiona-T/knot-art/issues/77) As a registered user I can easily navigate within the My Account pages so that I understand what pages are available and can get to them easily and I know what page I am on

#### Admin for Shop page
- [#38](https://github.com/Fiona-T/knot-art/issues/38) As the website owner, I can view all the products in the shop, even if they are not active, so that I can see an overview of all products, and so that I can edit inactive products
- [#39](https://github.com/Fiona-T/knot-art/issues/39) As the website owner, I can add a new product to the shop, so that I can sell the product to customers
- [#40](https://github.com/Fiona-T/knot-art/issues/40) As the website owner, I can add a edit the details of a product in the shop, so that I can change the price, description etc. and customers will see the updated information
- [#41](https://github.com/Fiona-T/knot-art/issues/41) As the website owner, I can turn on or off the active flag on a product, so that I can add or remove it from appearing in the shop for customers when it is in/out of stock
- [#42](https://github.com/Fiona-T/knot-art/issues/42) As the website owner, I can delete a product, so that it will not appear in the shop if it was added in error
- [#43](https://github.com/Fiona-T/knot-art/issues/43) As a website owner I can access the Django admin site for the categories so that I can add, edit or delete categories from here and new products for these categories can be added to the shop
- [#51](https://github.com/Fiona-T/knot-art/issues/51) As a site owner I can access the Django admin site for the products so that I can view, edit, delete products from here as well as from the website
- [#56](https://github.com/Fiona-T/knot-art/issues/56) As a website owner I can see orders in the admin site so that I can access the order details and fulfil the orders
- [#66](https://github.com/Fiona-T/knot-art/issues/66) As a website owner I can add a product and the sku is created automatically so that the skus for the products are standardised and I do not have to manually add a sku
- [#70](https://github.com/Fiona-T/knot-art/issues/70) As a website owner I can have the sku of a product updated when the category is changed so that the sku of the product is reflects the new category
- [#82](https://github.com/Fiona-T/knot-art/issues/82) As a website owner I can see a label and helptext on the category dropdown in the product form so that I am clear on what to do for this field

#### Admin for Markets page
- [#44](https://github.com/Fiona-T/knot-art/issues/44) As the website owner, I can see all markets on the markets page including past ones, so that I can see an overview of all markets and see older markets as well as upcoming ones
- [#45](https://github.com/Fiona-T/knot-art/issues/45) As the website owner, I can add a new market to the markets page, so that customers are informed of the market
- [#46](https://github.com/Fiona-T/knot-art/issues/46) As the website owner, I can edit the details of a market in the markets page, so that customers will see the updated information
- [#47](https://github.com/Fiona-T/knot-art/issues/47) As the website owner, I can delete a market, so that it will not appear in the markets page if it was added in error
- [#59](https://github.com/Fiona-T/knot-art/issues/59) As a site owner I can access the Django admin site for Markets so that I can view, edit, delete markets from here as well as from the website
- [#64](https://github.com/Fiona-T/knot-art/issues/64) As a website owner I can edit the details of a past market so that I can still edit the details even though it is in the past
- [#67](https://github.com/Fiona-T/knot-art/issues/67) As a website owner I can add a new county or Dublin postcode so that I can then choose that option when adding a new market
- [#68](https://github.com/Fiona-T/knot-art/issues/68) As a website owner I can edit a county or Dublin postcode for markets so that the correct text appears for users
- [#69](https://github.com/Fiona-T/knot-art/issues/69) As a website owner I can delete a county or Dublin postcode so that it no longer appears as an option, if it was added in error
- [#89](https://github.com/Fiona-T/knot-art/issues/89) As a website owner I can view the comments on a market in the admin site so that I can edit or delete users' comments from here if needed for moderation purposes

#### Admin for User Profiles
- [#63](https://github.com/Fiona-T/knot-art/issues/63) As a site owner I can access the Django admin site for Profiles so that I can view user profiles and user's saved market lists

#### Marketing/SEO
- [#48](https://github.com/Fiona-T/knot-art/issues/48) As the website owner, I want my website to contain relevant keywords so that users searching for these keywords will be more likely to find my website in web search results
- [#49](https://github.com/Fiona-T/knot-art/issues/49) As the website owner I have a link to the Facebook business page on the website so that customers or visitors to the website can follow the facebook page and I can generate more business through the facebook page
- [#50](https://github.com/Fiona-T/knot-art/issues/50) As the website owner I have relevant keywords included in the webpage metadata so that it helps improve SEO so that users searching for these keywords can find my website
- [#86](https://github.com/Fiona-T/knot-art/issues/86) As a website owner I can have a sitemap.xml and robots.txt file created for the website so that search engines can crawl the essential pages of the site and therefore users can find the site when searching key terms in search engine searches

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
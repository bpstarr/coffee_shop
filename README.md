# My Camo Cafe #

Camo cafe is the coffee shop's online website where customers can buy coffee.The employees can finish orders and edit menu items. The backend was built with Python and Flask, while the frontend was built with the bootstrap framework and AJAX to make it more responsive.

### Features ###

* Implemented responsive-design using bootstrap to enhance the user experience on different size screens. This includes responsive tables and navigation bar.

* Set up user registration and login with validations, also used password encryption for added protection on passwords. Validators are set up with flashed messages if there are errors.

* Set up three versions of the same website with different features based on if an employee,customer or no one is logged in to the website.

* Added the stripe API for easy payment with a customers credit card.

* A file upload was excuted for the employees to add menu pictures. A static file was used to save the image and the filename was saved to the database, which saves space.

* Customers can access the menu to see how much the price would change based on the size and/or quanitity of coffee they are looking at with the AJAX functionality.

* Employees can see when items are added to the menu with autorefreshing functionality from AJAX. When they fulfill the order an email is sent to the customer telling them that their order is ready to be picked up.

### Demo ###

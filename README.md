# Camo Cafe #

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

#### Customer Side ####

##### *Showing landing page #####

![ezgif com-gif-maker (4)](https://user-images.githubusercontent.com/87786124/152700401-e2cb7a83-0fe9-4f3b-8d12-f56a31853981.gif)

##### *Showing validators and login #####

![ezgif com-gif-maker (5)](https://user-images.githubusercontent.com/87786124/152700455-afdd0bb2-d403-4728-abd9-8a4322f34450.gif)

##### *Showing AJAX on price and quantity updates, showing cart and updating cart #####

![ezgif com-gif-maker (6)](https://user-images.githubusercontent.com/87786124/152700528-3f4613ab-965a-4bd8-800f-db8ceda073ea.gif)

##### * Showing the stripe API for credit cart payment and finishing order #####

![ezgif com-gif-maker (7)](https://user-images.githubusercontent.com/87786124/152700595-af9514b3-9cf9-43d1-a4de-9e4fc2fd240a.gif)

#### Employee Side ####

##### * Adding a Menu Item ######

![ezgif com-gif-maker (8)](https://user-images.githubusercontent.com/87786124/152709110-e8db5ef5-c2b3-4ca7-a488-297072f0132e.gif)

##### * Editing Menu and Size Price #####

![ezgif com-gif-maker (9)](https://user-images.githubusercontent.com/87786124/152709199-2b447c59-8620-4895-a6dd-298537364392.gif)

##### * Deleting Menu Item and Fulfilling Order #####

![ezgif com-gif-maker (10)](https://user-images.githubusercontent.com/87786124/152709260-f7e55a8e-8264-44c5-90ab-54dbcb2bc4bf.gif)

##### * Fulfilling Order and showing Stripe Dashboard after payment #####

![ezgif com-gif-maker (11)](https://user-images.githubusercontent.com/87786124/152709416-8bbac2f9-fc6c-444f-8ca4-0b24bcfb3638.gif)

##### * Showing Email from Employee to Customer on Mailtrap #####

![ezgif com-gif-maker (12)](https://user-images.githubusercontent.com/87786124/152709526-63491682-f9b7-4bbb-8a00-48fd50760bfe.gif)

























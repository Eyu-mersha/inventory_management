Project Title: Inventory Management API

   The application to be built is an inventory management api that helps company owners to efficiently manage and track their stock levels. It enables them to  manage the flow of resources, including both incoming and outgoing inventory,Keep real-time updates of stock quantities for each item in the inventory and track the addition of new stock and the removal of stock, store and retrieve detailed information about products such as descriptions, pricing, and categories,trigger notifications when stock levels are low and generate reports on stock history.

Requirements 

Django==5.1.3
django-bootstrap4==24.4
django-crispy-forms==2.3
django-environ==0.11.2
django-filter==24.3
django-registration-redux==2.13
djangorestframework==3.15.2
mysql==0.0.3
mysql-connector-python==9.1.0
mysqlclient==2.2.6

Core features and functionalities
 
Category and Product or Item Creation
Product or Item Update
Category and Product or Item Deletion
Product or Item Fetching
Product or Item issuance 
Product or Item restock
User Registration
User Login
User Logout
View List Items 
View Items History
Search by Category
Search by Item
Search by Price Range
Search by Date 
Update Restock Level
Low stock alert
Export Report  to csv


API Endpoints to Implement 
/accounts/login/ - user login endpoint
/accounts/logout/ - user logout endpoint
/list_items/ - endpoint to view all stock items 
/add_items/ - endpoint to add stock item
/list_history/ - endpoint to view recent stock history
/add_catagory/- endpoint to add category
/stock_detail/id/ - endpoint to see stock item detail
/issue_items/id/ - endpoint to issue a stock 
/receive_items/id/ - endpoint to restock a stock item
/reorder_level/id/ - endpoint to adjust restock level
/update_items/id/ -  endpoint to update stock item detail
/delete_items/id/ - endpoint to delete a stock item 





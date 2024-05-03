# Vendor_management

This is a Vendor Management System API built using Django REST Framework.
**Clone the repository:**

```bash
git clone <repository-url>
cd <repository-folder>

virtualenv vmsenv
source vmsenv/bin/activate

pip install -r requirements.txt


python manage.py makemigrations
python manage.py migrate

python manage.py createsuperuser

python manage.py runserver


API Endpoints
Vendor List/Create
URL: /api/vendors/
HTTP Method: GET (List), POST (Create)
Vendor Detail/Update/Delete
URL: /api/vendors/<int:pk>/
HTTP Method: GET (Retrieve), PUT/PATCH (Update), DELETE (Delete)
Vendor Performance
URL: /api/vendors/<int:vendor_id>/performance/
HTTP Method: GET
Description: Retrieves the calculated performance metrics for a specific vendor.
Acknowledge Purchase Order
URL: /api/purchase_orders/<int:po_id>/acknowledge/
HTTP Method: POST
Description: Acknowledge a purchase order and update acknowledgment date, triggering recalculation of average response time.


python manage.py test

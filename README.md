# Tire Change Booking


<img src="https://gooserave.eu/media/tire_change_booking/main_page.png" alt="main page" width="600">
<img src="https://gooserave.eu/media/tire_change_booking/booking_page.png" alt="booking page" width="600">

The backend is built using **Django** and the frontend using **Vue.js**.

By default, the frontend expects the backend to run on **localhost**, port **8000**. This can be changed by editing `/frontend/src/store/slots.js`.

These are the steps to start the backend and frontend in non-production mode:

### Backend:

```bash
cd backend

# Set up and activate a virtual environment
python -m venv .venv
source .venv/bin/activate # On Linux
# venv\Scripts\activate # On Windows

# Install dependencies
pip install -r requirements.txt

# Run the development server
python manage.py runserver
```

### Frontend:
```bash
cd frontend
npm install
npm run dev
```

For running tests, please use the following [config file](https://raw.githubusercontent.com/ArkadSt/tire_change_booking/refs/heads/main/backend/workshops.yaml) (already there when you clone the repository) and make sure that [workshops](https://github.com/Surmus/tire-change-workshop) are running. Then go to the `backend` folder and run:
```bash
python3 manage.py test
```


# Tire Change Booking
The backend is build using **Django** and frontend using **Vue.js**.

By default, frontend expects backend to run on **localhost**, port **8000**. This can be changed by editing `/frontend/src/store/slots.js`

These are the steps to start backend and frontend in non-production mode.

Backend:
```
cd backend
pip install -r requirements.txt
python3 manage.py runserver
```

Frontend:
```
cd frontend
npm install
npm run dev
```

For running tests please use the following [config file](https://raw.githubusercontent.com/ArkadSt/tire_change_booking/refs/heads/main/backend/workshops.yaml) and make sure that [workshops](https://github.com/Surmus/tire-change-workshop) are running.



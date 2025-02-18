<script setup>
import Slot from '@/components/Slot.vue';
import {ref, onMounted, watch, computed} from 'vue';
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'
import { useSlotStore } from '@/store/slots';

const store = useSlotStore();

const host = "http://localhost:8000"
const workshops = ref([])
const checked_workshops = computed(() => workshops.value.filter(workshop => workshop.selected))
const available_vehicle_types = ref([])
const checked_vehicle_types = computed(() => available_vehicle_types.value.filter(vehicle_type => vehicle_type.selected))
function extractDate(datetime){
    console.log(datetime)
	return datetime.split("T")[0]
}

const current_date = new Date()
const date_from = ref(current_date.toISOString())

const future_date = new Date()
future_date.setFullYear(future_date.getFullYear()+1)

const date_until = ref(future_date.toISOString())

const fetchWorkshops = async () => {
	await fetch(`${host}/api/workshops`)
        .then((response) => response.json())
        .then((data) => (workshops.value = data))
        .catch((err) => console.log(err.message));
    for (let workshop of workshops.value){
        workshop.selected = true
        for (let vehicle_type of workshop.vehicle_types){
            if (!available_vehicle_types.value.some(available_vehicle_type => available_vehicle_type.name === vehicle_type)){
                available_vehicle_types.value.push({"name": vehicle_type, "selected": true})
            }
        }
        workshop.vehicle_types = workshop.vehicle_types.map(vehicle_type => ({"name": vehicle_type, "selected": true}))
    }
}

const fetchSlots = async (workshop) => {
    await fetch(`${host}/api/times/?workshop=${workshop}&from=${extractDate(date_from.value)}&until=${extractDate(date_until.value)}`)
        .then((response) => response.json())
        .then((data) => store.slots.value.push(...data))
        .catch((err) => console.log(err.message));
}

const filterSlotsByVehicleType = () => {
    return store.slots.value.filter(slot => checked_vehicle_types.value.some(vehicle_type => slot.workshop.vehicle_types.includes(vehicle_type.name)))
}

const getAllSlots = async () => {
    store.slots.value = []
    for (let workshop of checked_workshops.value) {
        await fetchSlots(workshop.id);
    }
    store.slots.value = filterSlotsByVehicleType()
    console.log(store.slots.value)
}

onMounted(async ()=>{
    await fetchWorkshops()
    await getAllSlots()
})
const applyFilters = ( async () => {
    await getAllSlots()
    console.log("Slots updated")
})
</script>

<template>
    <div class="container mx-auto p-4">
        <div class="flex">
            <div class="w-1/4 pr-4">
                <div class="sticky top-4">
                    <h2 class="text-xl font-semibold mb-2">Filters:</h2>
                    <h3 class="text-lg font-medium mb-1">Time range</h3>
                    <label for="from" class="block mb-1">From:</label>
                    <VueDatePicker id="from" v-model="date_from" format="dd/MM/yyyy" class="mb-2 p-2 rounded w-full" :enable-time-picker="false" utc="preserve" />

                    <label for="until" class="block mb-1">Until:</label>
                    <VueDatePicker id="until" v-model="date_until" format="dd/MM/yyyy" class="mb-4 p-2 rounded w-full" :enable-time-picker="false" utc="preserve" />

                    <h3 class="text-lg font-medium mb-1">Workshops</h3>
                    <ul class="mb-4">
                        <li v-for="workshop in workshops" :key="workshop.id" class="mb-1">
                            <input type="checkbox" :id="workshop.id" v-model="workshop.selected" class="mr-2" />
                            <label :for="workshop.id">{{ workshop.name }}</label>
                        </li>
                    </ul>

                    <h3 class="text-lg font-medium mb-1">Vehicle types</h3>
                    <ul class="mb-4">
                        <li v-for="vehicle_type in available_vehicle_types" :key="vehicle_type.name" class="mb-1">
                            <input type="checkbox" :id="vehicle_type.name" v-model="vehicle_type.selected" class="mr-2" />
                            <label :for="vehicle_type.name">{{ vehicle_type.name }}</label>
                        </li>
                    </ul>
                    <button @click="applyFilters" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">Apply Filters</button>
                </div>
            </div>
            <div class="w-3/4">
                <h1 class="text-2xl font-bold mb-4 text-center">Available slots</h1>
                <ul class="slots grid grid-cols-1 gap-4">
                    <li class="post p-4 rounded" v-for="slot in store.slots.value" :key="slot.workshop.id + slot.id">
                        <Slot :slot="slot" />
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>
  
  <style scoped>
  /* Add any additional scoped styles here if needed */
  </style>
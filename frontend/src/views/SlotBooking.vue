<script setup>
import { ref, onMounted, computed, onBeforeMount} from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useSlotStore } from '@/store/slots';

const store = useSlotStore();
const router = useRouter();
const props = defineProps({
  id: String,
  workshop: String
});
const slot = ref(null);
const host = "http://localhost:8000";
const name = ref('');
const email = ref('');
const phone = ref('');
const message = ref('');
const errorMessage = ref('');

onBeforeMount(()=>{
    if (store.slots.value){
        slot.value = store.slots.value.find((s) => {
    console.log(s.id, props.id, s.workshop.id, props.workshop, String(s.id) == props.id, s.workshop.id == props.workshop, s.id == props.id && s.workshop.id === props.workshop);
    return s.id == props.id && s.workshop.id === props.workshop;
  });
    }else {
        router.push({ name: 'home' });
    }
})

const confirmBooking = async () => {
  try {
    const contactInfo = `Name: ${name.value}, Email: ${email.value}, Phone: ${phone.value}`;
    const response = await fetch(`${host}/api/book/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        workshop: slot.value.workshop.id,
        booking_id: slot.value.id,
        contact_info: contactInfo,
      }),
    });

    if (response.status === 200) {
      message.value = 'Booking confirmed successfully!';
      errorMessage.value = '';
    } else if (response.status === 422) {
      errorMessage.value = 'The time has already been booked.';
      message.value = '';
    } else if (response.status === 400) {
      const data = await response.json();
      errorMessage.value = data.error;
      message.value = '';
    } else if (response.status === 500) {
      errorMessage.value = 'Internal server error.';
      message.value = '';
    }
  } catch (error) {
    errorMessage.value = 'An unexpected error occurred.';
    message.value = '';
  }
};
</script>

<template>
  <div v-if="slot" class="max-w-4xl mx-auto bg-white rounded-2xl shadow-lg p-6 space-y-4">
    <h2 class="text-2xl font-semibold text-gray-800 mb-4">Booking Information</h2>
    <div class="space-y-2">
      <p class="text-gray-600">Workshop: {{ slot.workshop.name }}</p>
      <p class="text-gray-600">Address: {{ slot.workshop.address }}</p>
      <p class="text-gray-600">Time: {{ new Date(slot.time).toLocaleString('et-EE') }}</p>
      <p class="text-gray-600">Supported Vehicles: {{ slot.workshop.vehicle_types.join(', ') }}</p>
    </div>
    <div class="space-y-4 mt-4">
      <h3 class="text-xl font-semibold text-gray-800">Contact Information</h3>
      <div>
        <label for="name" class="block text-gray-700">Name</label>
        <input id="name" v-model="name" type="text" class="mt-1 block w-full p-2 border rounded" />
      </div>
      <div>
        <label for="email" class="block text-gray-700">Email</label>
        <input id="email" v-model="email" type="email" class="mt-1 block w-full p-2 border rounded" />
      </div>
      <div>
        <label for="phone" class="block text-gray-700">Phone</label>
        <input id="phone" v-model="phone" type="tel" class="mt-1 block w-full p-2 border rounded" />
      </div>
      <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" @click="confirmBooking">Confirm Booking</button>
    </div>
    <div v-if="message" class="mt-4 text-green-600">{{ message }}</div>
    <div v-if="errorMessage" class="mt-4 text-red-600">{{ errorMessage }}</div>
  </div>
</template>
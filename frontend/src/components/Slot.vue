<script setup>
import {ref} from 'vue';
import { useRouter } from 'vue-router';

const props = defineProps({
  slot: Object
});

const router = useRouter();

const bookSlot = () => {
    router.push({name: 'slot-booking', params: {workshop: props.slot.workshop.id, id: props.slot.id}});
};


</script>

<template>
  <div class="max-w-4xl mx-auto bg-white rounded-2xl shadow-lg p-6 space-y-4 flex flex-row items-center">
    <div class="flex-1">
      <h2 class="text-xl font-semibold text-gray-800">{{ slot.workshop.name }}</h2>
      <p class="text-gray-600">Address: {{ slot.workshop.address }}</p>
      <p class="text-gray-600">Time: {{ new Date(slot.time).toLocaleString('et-EE') }}</p>
      <p class="text-gray-600">Supported Vehicles: {{ slot.workshop.vehicle_types.join(', ') }}</p>
    </div>
    <div>
      <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" @click="bookSlot">Book</button>
    </div>
  </div>
</template>
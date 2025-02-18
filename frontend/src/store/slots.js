import { defineStore } from "pinia";
import { ref } from 'vue';

export const useSlotStore = defineStore("slots", () => {
    const host = "http://localhost:8000"
    const slots = ref([]);

    return { host, slots };
});
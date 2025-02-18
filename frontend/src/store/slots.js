import { defineStore } from "pinia";
import { ref } from 'vue';

export const useSlotStore = defineStore("slots", () => {

    const slots = ref([]);

    return { slots };
});
import { reactive } from 'vue';

const eventBus = reactive({});

export const on = (event, callback) => {
  if (!eventBus[event]) {
    eventBus[event] = [];
  }
  eventBus[event].push(callback);
};

export const off = (event, callback) => {
  if (eventBus[event]) {
    eventBus[event] = eventBus[event].filter(cb => cb !== callback);
  }
};

export const emit = (event, payload) => {
  if (eventBus[event]) {
    eventBus[event].forEach(callback => callback(payload));
  }
};
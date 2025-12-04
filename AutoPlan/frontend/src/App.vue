<template>
  <div id="app">
    <div style="display:flex; gap:20px; align-items:center; margin-bottom:10px">
      <button @click="loadSaved" :disabled="loading">
        {{ loading ? 'Laddar...' : 'Hämta sparat schema' }}
      </button>
      <span style="opacity:0.7">
        (Tog fram det senaste schemat sparat i backend/db/latest_schedule.json)
      </span>
    </div>

    <ScheduleView :initialSchedule="schedule" />

    <ChatBox @schedule-updated="updateSchedule" @loading-changed="setLoading" />

    <div style="margin-top:16px; min-height:24px">
      <span v-if="loading">⏳ Genererar schema...</span>
      <span v-else-if="lastMessage" style="opacity:0.8">{{ lastMessage }}</span>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import ScheduleView from './components/ScheduleView.vue';
import ChatBox from './components/ChatBox.vue';
import { fetchLatestSchedule } from './services/api.js';

export default {
  components: { ScheduleView, ChatBox },
  setup() {
    const schedule = ref({ week1: [], week2: [], week3: [], week4: [], week5: [] });
    const loading = ref(false);
    const lastMessage = ref('');

    const updateSchedule = (newSchedule) => {
      schedule.value = newSchedule;
      loading.value = false;
      lastMessage.value = 'Nytt schema genererat.';
    };

    const setLoading = (value) => {
      loading.value = value;
      if (value) {
        lastMessage.value = '';
      }
    };

    const loadSaved = async () => {
      try {
        loading.value = true;
        lastMessage.value = '';
        const data = await fetchLatestSchedule();
        schedule.value = data;
        lastMessage.value = 'Sparat schema hämtat.';
      } catch (e) {
        lastMessage.value = 'Kunde inte hämta sparat schema.';
      } finally {
        loading.value = false;
      }
    };

    return { schedule, updateSchedule, loadSaved, loading, lastMessage, setLoading };
  }
};
</script>
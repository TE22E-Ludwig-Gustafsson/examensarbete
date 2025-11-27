<template>
  <div id="app">
    <div style="display:flex; gap:20px; align-items:center; margin-bottom:10px">
      <button @click="loadSaved">Hämta sparat schema</button>
      <span style="opacity:0.7">(Tog fram det senaste schemat sparat i backend/db/latest_schedule.json)</span>
    </div>

    <ScheduleView :initialSchedule="schedule" />
    <ChatBox @schedule-updated="updateSchedule" />

    <div v-if="rawSchedule" style="margin-top:20px">
      <h3>Senast mottagna (raw JSON)</h3>
      <pre style="background:#fafafa;border:1px solid #eee;padding:10px">{{ rawSchedule }}</pre>
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

    const rawSchedule = ref('');

    const updateSchedule = (newSchedule) => {
      schedule.value = newSchedule;
      try {
        rawSchedule.value = JSON.stringify(newSchedule, null, 2);
      } catch (e) {
        rawSchedule.value = String(newSchedule);
      }
    };

    const loadSaved = async () => {
      try {
        const data = await fetchLatestSchedule();
        schedule.value = data;
        rawSchedule.value = JSON.stringify(data, null, 2);
      } catch (e) {
        rawSchedule.value = 'Kunde inte hämta sparat schema';
      }
    };

    return { schedule, updateSchedule, loadSaved, rawSchedule };
  }
};
</script>

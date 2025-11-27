<template>
  <div id="app">
    <ScheduleView :initialSchedule="schedule" />
    <ChatBox @schedule-updated="updateSchedule" />
  </div>
</template>

<script>
import { ref } from 'vue';
import ScheduleView from './components/ScheduleView.vue';
import ChatBox from './components/ChatBox.vue';

export default {
  components: { ScheduleView, ChatBox },
  setup() {
    const schedule = ref({ week1: [], week2: [], week3: [], week4: [], week5: [] });

    const updateSchedule = (newSchedule) => {
      schedule.value = newSchedule;
    };

    return { schedule, updateSchedule };
  }
};
</script>

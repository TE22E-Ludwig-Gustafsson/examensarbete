<template>
    <div>
        <textarea v-model="userText" placeholder="Skriv här..."></textarea>
        <button @click="sendText">Skicka</button>
    </div>
</template>
<script>
import { ref } from 'vue';
import { parseTextToSchedule } from '../services/api.js';

export default {
    setup(props, { emit }) {
        const userText = ref('');

        const sendText = async () => {
            if (!userText.value) return;
            const schedule = await parseTextToSchedule(userText.value);
            emit('schedule-updated', schedule);
            userText.value = '';
        };

        return { userText, sendText };
    }
};
</script>
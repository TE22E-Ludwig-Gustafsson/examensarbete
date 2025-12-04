<template>
    <div>
        <textarea
            v-model="userText"
            placeholder="Skriv här..."
            rows="4"
            style="width:100%;"
    ></textarea>
        <button
            @click="sendText"
            :disabled="loading || !userText.trim()"
            style="margin-top:8px;"
        >
            {{ loading ? 'Genererar...' : 'Skicka' }}
        </button>
    </div>
</template>
<script>
import { ref } from 'vue';
import { parseSchedule } from '../services/api.js';

export default {
    emits: ['schedule-updated', 'loading-changed'],
    setup(props, { emit }) {
        const userText = ref('');
        const loading = ref(false);

        const sendText = async () => {
            const text = userText.value.trim();
            if (!text || loading.value) return;

            loading.value = true;
            emit('loading-changed', true);

            try {
                const schedule = await parseSchedule(text);
                emit('schedule-updated', schedule);
                userText.value = '';
            } catch (e) {
                // Här kan du lägga till felhantering om du vill
            } finally {
                loading.value = false;
                emit('loading-changed', false);
            }
        };

        return { userText, sendText, loading };
    }
};
</script>
<template>
    <div class="chatbox">
        <textarea
            v-model="userText"
            placeholder="Skriv här..."
            rows="4"
            class="chatbox-textarea"
        ></textarea>
        <button
            @click="sendText"
            :disabled="loading || !userText.trim()"
            class="chatbox-button"
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

            } finally {
                loading.value = false;
                emit('loading-changed', false);
            }
        };

        return { userText, sendText, loading };
    }
};
</script>

<style scoped>
.chatbox {
    max-width: 600px;
    margin: 16px auto;
    display: flex;
    flex-direction: column;
}

.chatbox-textarea {
    width: 100%;
    padding: 8px;
    border-radius: 4px;
    border: 1px solid #ccc;
    font-family: inherit;
    font-size: 14px;
    resize: vertical;
}

.chatbox-button {
    margin-top: 8px;
    align-self: flex-end;
    padding: 6px 14px;
    border: none;
    border-radius: 4px;
    background-color: #1976d2;
    color: #fff;
    font-size: 14px;
    cursor: pointer;
}

.chatbox-button:disabled {
    opacity: 0.7;
    cursor: default;
}
</style>
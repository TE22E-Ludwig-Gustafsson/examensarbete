<template>
    <div>
        <h2>Schema (5 veckor)</h2>
        <table border="1" cellpadding="5" cellspacing="0">
            <thead>
                <tr>
                    <th>Vecka</th>
                    <th>Dag</th>
                    <th>Start</th>
                    <th>Slut</th>
                    <th>Uppgift</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(item, index) in schedule" :key="index">
                    <td>{{ item.week }}</td>
                    <td>{{ item.day }}</td>
                    <td>{{ item.start }}</td>
                    <td>{{ item.end }}</td>
                    <td>{{ item.task }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { getSchedule } from '../services/api';

export default {
    name: 'ScheduleView',
    setup() {
        const schedule = ref([]);

        onMounted(async () => {
            schedule.value = await getSchedule();
        });

        return { schedule };
    }
};
</script>

<style scoped>
table {
    width: 100%;
    border-collapse: collapse;
}

th,
td {
    text-align: center;
}
</style>

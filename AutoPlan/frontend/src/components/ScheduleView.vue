<template>
    <div>
        <h2>Schema</h2>
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
                <tr v-for="(week, wIndex) in Object.keys(schedule)" :key="wIndex">
                    <td v-for="(item, iIndex) in schedule[week]" :key="iIndex">
                        {{ week }} | {{ item.day }} | {{ item.start }} | {{ item.end }} | {{ item.task }}
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
import { ref, onMounted } from 'vue';

export default {
    props: ['initialSchedule'],
    setup(props) {
        const schedule = ref(props.initialSchedule || { week1: [], week2: [], week3: [], week4: [], week5: [] });
        return { schedule };
    }
};
</script>
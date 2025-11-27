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
                        <!-- Flatten schedule object into rows so each item gets its own table row and column -->
                        <tr v-for="(row, index) in (scheduleRows || [])" :key="index">
                            <td>{{ row.week }}</td>
                            <td>{{ row.day }}</td>
                            <td>{{ row.start }}</td>
                            <td>{{ row.end }}</td>
                            <td>{{ row.task }}</td>
                        </tr>

                        <!-- Show friendly empty state when there are no items -->
                        <tr v-if="!(scheduleRows && scheduleRows.length)">
                            <td colspan="5" style="text-align:center; opacity:0.7">Inget uppdaterar i schemat</td>
                        </tr>
                    </tbody>
        </table>
    </div>
</template>

<script>
import { computed } from 'vue';

export default {
    props: ['initialSchedule'],
    setup(props) {

        const defaultSchedule = { week1: [], week2: [], week3: [], week4: [], week5: [] };
        const schedule = computed(() => props.initialSchedule || defaultSchedule);

        const scheduleRows = computed(() => {
            const rows = [];
            const s = schedule.value ?? {};

            if (Array.isArray(s)) {
                for (const item of s) {
                    const wk = item && (item.week ?? item.weekNumber ?? item.weekNo);
                    const weekLabel = wk !== undefined && wk !== null && wk !== '' ? `Vecka ${wk}` : '';
                    rows.push({
                        week: weekLabel,
                        day: item?.day ?? '',
                        start: item?.start ?? '',
                        end: item?.end ?? '',
                        task: item?.task ?? ''
                    });
                }
                return rows;
            }

            // If schedule is an object keyed by week (e.g., { week1: [ ... ] })
            for (const [weekKey, items] of Object.entries(s)) {
                const weekLabel = String(weekKey).replace(/^week\s*/i, 'Vecka ');
                if (Array.isArray(items)) {
                    for (const item of items) {
                        rows.push({
                            week: weekLabel,
                            day: item?.day ?? '',
                            start: item?.start ?? '',
                            end: item?.end ?? '',
                            task: item?.task ?? ''
                        });
                    }
                }
            }

            return rows;
        });

        return { schedule, scheduleRows };
    }
};
</script>
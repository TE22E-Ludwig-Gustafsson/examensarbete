import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api/schedule";

export const getSchedule = async () => {
  // Mock-data för Sprint 1
  return [
    { week: 1, day: "Måndag", task: "", start: "", end: "" },
    { week: 1, day: "Tisdag", task: "", start: "", end: "" },
    { week: 1, day: "Onsdag", task: "", start: "", end: "" },
    { week: 1, day: "Torsdag", task: "", start: "", end: "" },
    { week: 1, day: "Fredag", task: "", start: "", end: "" },
  ];
};

export const parseTextToSchedule = async (text) => {
  const response = await axios.post(`${API_URL}/parse`, { text });
  return response.data; // Returnerar JSON-schema från backend
};

export const fetchLatestSchedule = async () => {
  const response = await axios.get(`${API_URL}/latest`);
  return response.data;
};

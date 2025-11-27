import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api';

export const getSchedule = async () => {
  // Mock-data för Sprint 1
  return [
    { week: 1, day: "Måndag", task: "", start: "", end: "" },
    { week: 1, day: "Tisdag", task: "", start: "", end: "" }
  ];
};

export const parseTextToSchedule = async (text) => {
  // Mock-response
  return { status: "not implemented" };
};

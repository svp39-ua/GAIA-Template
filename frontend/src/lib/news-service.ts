// [Feature: News Management] [Story: NM-ADM-001] [Ticket: NM-ADM-001-FE-T03]
import axios from 'axios';

// Create axios instance with base URL (proxy will handle /api)
const api = axios.create({
    baseURL: '/api/v1',
    headers: {
        'Content-Type': 'application/json',
    },
});

export interface NewsCreatePayload {
    title: string;
    summary?: string;
    content?: string;
    scope: 'GENERAL' | 'INTERNAL';
    cover_url?: string;
}

export const createNews = async (data: NewsCreatePayload) => {
    // Mock Auth Header for now
    const response = await api.post('/news', data, {
        headers: {
            Authorization: 'Bearer mock-admin-token'
        }
    });
    return response.data;
};

import axios from 'axios';

const apiClient = axios.create({
    baseURL: '',
    timeout: 1000,
    headers: { 'Content-Type': 'application/json' }
});

export const UpdateURL = (newURL) => {
    apiClient.baseURL = newURL
}

export const genQuiz = async (data) => {
    const resposne = await apiClient.post('/multichoices/generate', data)
    return resposne.data    
}

export const getLLM = async () => {
    const resposne = await axios.get('/backends')
    return resposne.data
}
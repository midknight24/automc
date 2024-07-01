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
    try {
        const resposne = await apiClient.post('/multichoices/generate', data)
        return resposne.data    
    } catch(err) {
        console.log(err)
    }
}

export const getLLM = async () => {
    try {
        const resposne = await axios.get('/backends')
        return resposne.data
    } catch(err) {
        console.log(err)
    }
}